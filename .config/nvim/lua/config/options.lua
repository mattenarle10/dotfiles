-- General settings
vim.o.number = true          -- Show line numbers (your original setting!)
vim.o.relativenumber = true  -- Relative line numbers for easy jumping
vim.o.mouse = "a"            -- Enable mouse support
vim.o.clipboard = "unnamedplus" -- Use system clipboard
vim.o.ignorecase = true      -- Ignore case in search
vim.o.smartcase = true       -- Unless uppercase is used
vim.o.expandtab = true       -- Use spaces instead of tabs
vim.o.shiftwidth = 2         -- 2 spaces for indentation
vim.o.tabstop = 2            -- 2 spaces for tab
vim.o.smartindent = true     -- Smart indentation
vim.o.wrap = false           -- Don't wrap lines
vim.o.cursorline = true      -- Highlight current line
vim.o.termguicolors = true   -- True color support
vim.o.signcolumn = "yes"     -- Always show sign column
vim.o.updatetime = 250       -- Faster completion
vim.o.timeoutlen = 300       -- Faster key sequence completion
vim.o.cmdheight = 0          -- Hide command line when not in use (no bottom space)
vim.o.undofile = true        -- Persistent undo
vim.o.swapfile = false       -- No swap files
vim.o.backup = false         -- No backup files
vim.o.splitright = true      -- Vertical splits to the right
vim.o.splitbelow = true      -- Horizontal splits below

-- Auto-reload files when changed externally (for Claude Code integration!)
vim.o.autoread = true        -- Auto-reload files changed outside nvim
vim.api.nvim_create_autocmd({ "FocusGained", "BufEnter", "CursorHold" }, {
  pattern = "*",
  command = "checktime",
})

-- Disable netrw (we use neo-tree instead)
vim.g.loaded_netrw = 1
vim.g.loaded_netrwPlugin = 1
