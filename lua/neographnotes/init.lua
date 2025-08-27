
local M = {}

-- Конфигурация (в будущем можно вынести в setup функцию)
local config = {
  notes_path = vim.fn.expand('~/orgfiles'), -- Path to your notes
  cache_file = vim.fn.stdpath('cache') .. '/neographnotes_cache.json',
  parser_script = vim.fn.expand('$HOME/nvimPlug/NeoGraphNotes/parser/parse.py'),
  gui_script = vim.fn.expand('$HOME/nvimPlug/NeoGraphNotes/gui/main.py'),
}

-- Функция для открытия графа
function M.open()
  -- 1. Выполняем скрипт парсера для генерации кэша
  --    В реальной реализации это может быть более сложный вызов (Rust/C++ бинарник)
  local python_executable = vim.fn.expand('$HOME/nvimPlug/NeoGraphNotes/venv/bin/python3')
  local parser_job = vim.fn.jobstart({
    python_executable,
    config.parser_script, 
    config.notes_path, 
    config.cache_file
  })

  vim.fn.jobwait({parser_job})

  if vim.v.shell_error ~= 0 then
    vim.notify('NeoGraphNotes: Ошибка при парсинге заметок!', vim.log.levels.ERROR)
    return
  end

  vim.notify('NeoGraphNotes: Заметки успешно просканированы.')

  -- 2. Запускаем GUI в отдельном процессе
  vim.notify('NeoGraphNotes: Python executable: ' .. python_executable)
  vim.notify('NeoGraphNotes: GUI script: ' .. config.gui_script)

  vim.notify('NeoGraphNotes: Запускаем GUI с отладкой...')
  vim.fn.jobstart({
      python_executable,
      config.gui_script,
      config.cache_file,
      vim.v.servername
  }, {
      on_stdout = function(_, data) 
          if data then
              vim.schedule(function() 
                  vim.api.nvim_echo({{'NeoGraphNotes GUI (stdout):', 'Comment'}}, true, {})
                  vim.api.nvim_echo({{'  ' .. table.concat(data, '\n')}}, true, {})
              end)
          end
      end,
      on_stderr = function(_, data) 
          if data then
              vim.schedule(function() 
                  vim.api.nvim_echo({{'NeoGraphNotes GUI (stderr):', 'ErrorMsg'}}, true, {})
                  vim.api.nvim_echo({{'  ' .. table.concat(data, '\n')}}, true, {})
              end)
          end
      end,
      on_exit = function(_, code, _) 
          vim.schedule(function() 
              vim.api.nvim_echo({{'NeoGraphNotes GUI: ', 'Comment'}, {'Процесс завершился с кодом ' .. code, 'None'}}, true, {})
          end)
      end,
      detached = true
  })

  vim.notify('NeoGraphNotes: Граф открывается в отдельном окне...')
end

return M
