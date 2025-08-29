# NeoGraphNotes

A Neovim plugin to visualize your notes as a beautiful, interactive, and physics-based graph, inspired by Obsidian. Turn your collection of linked notes into a "second brain" that you can see and explore.

![Placeholder for GIF](https://via.placeholder.com/800x400.png?text=NeoGraphNotes+In+Action)
*(Feel free to replace this placeholder with a GIF of the plugin!)*

## Features

-   **Interactive Graph:** Generates a force-directed graph from your `.md` and `.org` notes.
-   **Link Detection:** Automatically detects `[[wiki-style]]` links to build connections between your notes.
-   **Obsidian-like Experience:** A default visual style and physics model that mimics the beloved Obsidian graph view.
-   **Dynamic Node Sizing:** Nodes with more connections appear larger, giving you an at-a-glance view of the most central ideas in your knowledge base.
-   **Highly Customizable:** Easily tweak the graph's appearance and physics through a simple configuration table.
-   **Fast & Efficient:** Caches the parsed graph structure for near-instantaneous reloads.

## Requirements

-   Neovim >= 0.7
-   Python 3.x
-   Python packages:
    -   `PyQt5`
    -   `PyQtWebEngine`
    -   `pyvis`
    -   `networkx`

You can install the required Python packages using pip:
```bash
pip install PyQt5 PyQtWebEngine pyvis networkx
```

## Installation

You can install NeoGraphNotes using your favorite plugin manager.

### lazy.nvim

```lua
{
  'your-github-username/NeoGraphNotes',
  config = function()
    require('neographnotes').setup({
      -- Your custom configuration goes here
    })
  end,
}
```
*(Please replace `your-github-username/NeoGraphNotes` with the actual repository path once you upload it.)*

## Configuration

You can configure the plugin by passing a table to the `setup` function.

Here is the default configuration:
```lua
-- Default configuration
local config = {
  -- Path to your notes directory.
  notes_path = vim.fn.expand('~/orgfiles'),

  -- Path to the Python executable in your virtual environment.
  -- This is a **required** setting.
  python_path = nil,

  -- A list of file and directory names to ignore during parsing.
  ignore_patterns = { 'journal', 'todo.org' },

  -- (Internal paths, usually no need to change)
  parser_script = '...',
  gui_script = '...',
  cache_file = '...',
}
```

### Example Setup

Here is an example of how you might configure the plugin in your `init.lua`:

```lua
require('neographnotes').setup({
  -- REQUIRED: Set the path to the Python interpreter that has the
  -- required packages installed.
  python_path = '/home/user/my-neovim-env/bin/python',

  -- OPTIONAL: Change the path to your notes directory.
  notes_path = '~/Documents/MyNotes',

  -- OPTIONAL: Add more patterns to ignore.
  ignore_patterns = { 'journal', 'todo.org', 'daily-notes' },
})
```

## Usage

To open the graph view, simply run the following command in Neovim:

```
:NeoGraphOpen
```

This will scan your notes, generate the graph, and open it in a separate window.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
