local M = {}

-- Determine plugin root path
local script_path = debug.getinfo(1, "S").source:sub(2)
local plugin_root = vim.fn.fnamemodify(script_path, ':h:h:h')

-- Default configuration
local config = {
  notes_path = vim.fn.expand('~/orgfiles'), -- Path to your notes
  parser_script = plugin_root .. '/parser/parse.py',
  gui_script = plugin_root .. '/gui/main.py',
  python_path = nil, -- Will be set via setup
  cache_file = vim.fn.stdpath('cache') .. '/neographnotes_cache.json',
  ignore_patterns = { 'journal', 'todo.org' }, -- Ignored files and folders
}

---
-- Plugin setup function. Called from lazy.nvim
-- @param opts Table with user options
function M.setup(opts)
  -- Merge default settings with user-provided ones
  config = vim.tbl_deep_extend('force', config, opts or {})

  -- Create a user command that can be called from Neovim
  vim.api.nvim_create_user_command('NeoGraphNotes', M.open, {
    desc = 'Open the NeoGraphNotes graph'
  })
end

---
-- Function to open the graph
function M.open()
  -- DEBUG: Print script paths
  vim.notify("DEBUG parser_script: " .. tostring(config.parser_script), vim.log.levels.INFO)
  vim.notify("DEBUG gui_script: " .. tostring(config.gui_script), vim.log.levels.INFO)

  if not config.python_path then
    vim.notify('NeoGraphNotes: python_path is not configured! Please set it in the setup() function.', vim.log.levels.ERROR)
    return
  end

  vim.notify('NeoGraphNotes: Scanning notes...')
  
  -- 1. Execute the parser script to generate the cache
  local parser_command = {
    config.python_path,
    config.parser_script,
    config.notes_path,
    config.cache_file
  }
  if config.ignore_patterns and #config.ignore_patterns > 0 then
    vim.list_extend(parser_command, config.ignore_patterns)
  end
  local parser_job = vim.fn.jobstart(parser_command)

  local job_result = vim.fn.jobwait({parser_job})

  if job_result[1] == -1 or (vim.v.shell_error and vim.v.shell_error ~= 0) then
    vim.notify('NeoGraphNotes: Error while parsing notes!', vim.log.levels.ERROR)
    return
  end

  vim.notify('NeoGraphNotes: Notes scanned successfully.')

  -- 2. Run the GUI in a separate process
  vim.notify('NeoGraphNotes: Starting GUI...')
  vim.fn.jobstart({
      config.python_path,
      config.gui_script,
      config.cache_file,
      vim.v.servername
  }, {
      on_stdout = function(_, data) 
          if data and data[1] ~= '' then
              vim.schedule(function() 
                  vim.api.nvim_echo({{'NeoGraphNotes GUI (stdout):', 'Comment'}}, true, {})
                  vim.api.nvim_echo({{'  ' .. table.concat(data, '\n')}}, true, {})
              end)
          end
      end,
      on_stderr = function(_, data) 
          if data and data[1] ~= '' then
              vim.schedule(function() 
                  vim.api.nvim_echo({{'NeoGraphNotes GUI (stderr):', 'ErrorMsg'}}, true, {})
                  vim.api.nvim_echo({{'  ' .. table.concat(data, '\n')}}, true, {})
              end)
          end
      end,
      on_exit = function(_, code, _) 
          vim.schedule(function() 
              vim.api.nvim_echo({{'NeoGraphNotes GUI: ', 'Comment'}, {'Process finished with code ' .. code, 'None'}}, true, {})
          end)
      end,
      detached = true
  })

  vim.notify('NeoGraphNotes: Opening graph in a separate window...')
end

return M
