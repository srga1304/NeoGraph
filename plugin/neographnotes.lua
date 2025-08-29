-- Define the :NeoGraphOpen user command
vim.api.nvim_create_user_command(
  'NeoGraphOpen',
  function()
    -- Call the main plugin function
    require('neographnotes').open()
  end,
  {
    nargs = 0,
    desc = 'Open the NeoGraphNotes graph',
  }
)
