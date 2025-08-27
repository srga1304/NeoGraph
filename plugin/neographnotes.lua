
-- Определяем пользовательскую команду :NeoGraphOpen
vim.api.nvim_create_user_command(
  'NeoGraphOpen',
  function()
    -- Вызываем основную функцию плагина
    require('neographnotes').open()
  end,
  {
    nargs = 0,
    desc = 'Открыть граф заметок NeoGraphNotes',
  }
)
