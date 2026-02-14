# Learning Your Nvim Lua Configuration

A step-by-step guide to understand everything we added.

## 📁 File Structure Overview

```
.config/nvim/
├── init.lua                    # Entry point - loads everything
└── lua/
    ├── config/                 # Core configurations
    │   ├── options.lua        # Vim settings (line numbers, tabs, etc.)
    │   ├── keymaps.lua        # All keyboard shortcuts
    │   └── lazy.lua           # Plugin manager setup
    └── plugins/                # Plugin configurations
        ├── colorscheme.lua    # Theme (tokyonight)
        ├── neo-tree.lua       # File explorer
        ├── telescope.lua      # Fuzzy finder
        ├── treesitter.lua     # Syntax highlighting
        ├── lsp.lua            # Language servers
        ├── completion.lua     # Autocomplete
        ├── lazygit.lua        # Git integration
        └── misc.lua           # Other plugins
```

## 🎯 Learning Path

### Step 1: Understand init.lua (5 mins)
**File:** `.config/nvim/init.lua`

This is the entry point. It does 3 things:
1. **Bootstraps lazy.nvim** (plugin manager) - downloads it if not installed
2. **Sets leader key** to Space - this is your main shortcut key
3. **Loads your configs** - options, keymaps, and plugins

**Try:**
```bash
nvim ~/.dotfiles/.config/nvim/init.lua
```

### Step 2: Learn Options (10 mins)
**File:** `.config/nvim/lua/config/options.lua`

This sets how nvim behaves. Key settings:
- `vim.o.number = true` - Show line numbers
- `vim.o.clipboard = "unnamedplus"` - Use system clipboard
- `vim.o.tabstop = 2` - 2 spaces for tabs
- `vim.o.splitright = true` - New splits open right

**Experiment:**
1. Open the file: `nvim ~/.dotfiles/.config/nvim/lua/config/options.lua`
2. Change `tabstop` from 2 to 4
3. Restart nvim and see the difference
4. Change it back

### Step 3: Master Keymaps (15 mins)
**File:** `.config/nvim/lua/config/keymaps.lua`

This is THE most important file. All shortcuts are here.

**Key concepts:**
```lua
map("n", "<leader>w", "<cmd>w<cr>", { desc = "Save file" })
```
- `"n"` = Normal mode
- `"<leader>w"` = Space + w
- `"<cmd>w<cr>"` = Run :w command
- `desc` = Description (shows in which-key)

**Practice these keybindings NOW:**
1. Open nvim
2. Press `Space` and wait - which-key will show you options
3. Try:
   - `Space + w` - Save
   - `Space + e` - File explorer
   - `Space + ff` - Find files
   - `Space + gg` - Git UI

### Step 4: Understanding Plugins (20 mins)

#### Plugin Structure
Each plugin file looks like:
```lua
return {
  "author/plugin-name",
  config = function()
    -- Setup code here
  end,
}
```

#### Start with Colorscheme (simplest)
**File:** `.config/nvim/lua/plugins/colorscheme.lua`

```lua
return {
  "folke/tokyonight.nvim",  -- Plugin from GitHub
  lazy = false,              -- Load immediately
  priority = 1000,           -- Load before other plugins
  config = function()
    vim.cmd([[colorscheme tokyonight-night]])  -- Apply theme
  end,
}
```

**Try changing themes:**
1. Open the file
2. Change `tokyonight-night` to `tokyonight-storm`
3. Restart nvim
4. See the different blue!

#### File Explorer (neo-tree)
**File:** `.config/nvim/lua/plugins/neo-tree.lua`

Key parts:
- `require("neo-tree").setup({...})` - Configure the plugin
- `vim.keymap.set(...)` - Add keybindings

**Practice:**
1. Open nvim
2. Press `Space + e` - File tree opens
3. Navigate with `j/k` (up/down)
4. Press `Enter` to open file
5. Press `Space + e` again to close

#### Fuzzy Finder (telescope)
**File:** `.config/nvim/lua/plugins/telescope.lua`

This is your search tool.

**Try all these:**
1. `Space + ff` - Find files by name *(includes hidden files)*
2. `Space + fg` - Live grep (search text in all files) *(includes hidden files)*
3. `Space + fw` - Find word under cursor
4. `Space + fb` - Find open buffers
5. `Space + fr` - Recent files

**Git pickers (no LazyGit needed):**
- `Space + gb` - Switch branches
- `Space + gs` - Git status
- `Space + gc` - Git commits

**Inside telescope:**
- Type to filter results
- `Ctrl + n/p` - Move up/down
- `Enter` - Open file

### Step 5: LSP (Language Servers) (20 mins)
**File:** `.config/nvim/lua/plugins/lsp.lua`

This gives you IDE features:
- Autocomplete
- Go to definition
- Error checking

**Key components:**
1. **Mason** - Installs language servers
2. **lspconfig** - Configures them
3. **Keymaps** - How to use LSP features

**Try it:**
1. Open a JS/Python/Lua file
2. Hover over a function - press `K` (capital K)
3. Put cursor on a variable - press `gd` (go to definition)
4. Press `Space + rn` - rename variable everywhere

**Install more language servers:**
```vim
:Mason
```
Navigate and press `i` to install servers for your languages.

### Step 6: Git Integration (10 mins)
**File:** `.config/nvim/lua/plugins/lazygit.lua`

Super simple - just one keybinding:
- `Space + gg` - Opens LazyGit TUI

**Practice:**
1. Open nvim in a git repo
2. Press `Space + gg`
3. You see: files, commits, branches
4. Press `q` to quit

**LazyGit basics:**
- `Tab` - Switch panels
- `Space` - Stage file
- `c` - Commit
- `P` - Push
- `?` - Help

## 🎓 Advanced Learning

### Customize Your Own Plugin

Want to add a new plugin? Create a new file:

```bash
nvim ~/.dotfiles/.config/nvim/lua/plugins/my-plugin.lua
```

Example - add a todo list plugin:
```lua
return {
  "folke/todo-comments.nvim",
  config = function()
    require("todo-comments").setup()
  end,
}
```

Save, restart nvim, and it auto-installs!

### Modify Keybindings

Open `.config/nvim/lua/config/keymaps.lua` and add:
```lua
map("n", "<leader>t", "<cmd>TodoTelescope<cr>", { desc = "Find todos" })
```

Now `Space + t` shows all TODO comments!

## ✂️ Text Selection & Yanking (Copying)

Your config has `clipboard = "unnamedplus"` so everything you yank goes to system clipboard!

### Visual Selection (Highlighting)
| Keys | Action |
|------|--------|
| `v` | Start character selection |
| `V` | Select whole line |
| `Ctrl+v` | Block/column select |
| `viw` | Select word |
| `vib` | Select inside `()` |
| `viB` | Select inside `{}` |
| `vi"` | Select inside quotes |
| `vip` | Select paragraph |
| `vit` | Select inside HTML tag |
| `S` | Flash Treesitter - smart select code blocks |

### Yank (Copy)
| Keys | Action |
|------|--------|
| `y` | Yank selection (copies to system clipboard) |
| `yy` | Yank whole line |
| `yiw` | Yank word |
| `yi"` | Yank inside quotes |
| `yip` | Yank paragraph |
| `yap` | Yank paragraph including whitespace |

### Surround (nvim-surround)
| Keys | Action |
|------|--------|
| `ysiw"` | Surround word with quotes |
| `ds"` | Delete surrounding quotes |
| `cs"'` | Change `"` to `'` |

## 🔥 Pro Tips

1. **Which-key is your friend** - Press `Space` and wait to see all shortcuts
2. **Read plugin READMEs** - Each plugin has docs on GitHub
3. **Start simple** - Don't customize everything at once
4. **Learn Lua basics** - It's easy! Check: https://learnxinyminutes.com/docs/lua/

## 📚 Resources

- **Lua in Y minutes**: https://learnxinyminutes.com/docs/lua/
- **Neovim docs**: `:help` in nvim
- **LazyVim docs**: https://www.lazyvim.org/
- **Plugin search**: https://dotfyle.com/neovim/plugins

## 🎯 Next Steps

1. Use nvim for 1 week with current config
2. Note what annoys you
3. Then customize to fix those annoyances
4. Add plugins one at a time

Don't try to learn everything at once!
