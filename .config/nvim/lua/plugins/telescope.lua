-- Fuzzy finder
return {
  "nvim-telescope/telescope.nvim",
  dependencies = {
    "nvim-lua/plenary.nvim",
    {
      "nvim-telescope/telescope-fzf-native.nvim",
      build = "make",
    },
  },
  config = function()
    local telescope = require("telescope")
    local telescopeConfig = require("telescope.config")

    -- Make Telescope behave more like an IDE:
    -- - search hidden files (e.g. .env, .github)
    -- - but still ignore .git
    local vimgrep_arguments = { unpack(telescopeConfig.values.vimgrep_arguments) }
    table.insert(vimgrep_arguments, "--hidden")
    table.insert(vimgrep_arguments, "--glob")
    table.insert(vimgrep_arguments, "!.git/*")

    local find_files_command = nil
    if vim.fn.executable("rg") == 1 then
      find_files_command = { "rg", "--files", "--hidden", "--glob", "!.git/*" }
    elseif vim.fn.executable("fd") == 1 then
      -- fd is usually faster for file listing
      find_files_command = { "fd", "--type", "f", "--hidden", "--exclude", ".git" }
    end

    telescope.setup({
      defaults = {
        vimgrep_arguments = vimgrep_arguments,
        file_ignore_patterns = { "node_modules", ".git/" },
      },
      pickers = {
        find_files = {
          hidden = true,
          find_command = find_files_command,
        },
      },
    })
    telescope.load_extension("fzf")

    -- Keymaps
    local map = vim.keymap.set

    -- Standard leader keymaps
    map("n", "<leader>ff", "<cmd>Telescope find_files<cr>", { desc = "Find files" })
    map("n", "<leader>fg", "<cmd>Telescope live_grep<cr>", { desc = "Live grep (search text)" })
    map("n", "<leader>fb", "<cmd>Telescope buffers<cr>", { desc = "Find buffers" })
    map("n", "<leader>fh", "<cmd>Telescope help_tags<cr>", { desc = "Find help" })
    map("n", "<leader>fr", "<cmd>Telescope oldfiles<cr>", { desc = "Recent files" })
    map("n", "<leader>fw", "<cmd>Telescope grep_string<cr>", { desc = "Find word under cursor" })

    -- Git pickers (easy branch switching without LazyGit)
    -- Both work:
    --   <leader>gb  (easy)
    --   <leader>gB  (Shift+B)
    map("n", "<leader>gb", "<cmd>Telescope git_branches<cr>", { desc = "Git branches (switch)" })
    map("n", "<leader>gB", "<cmd>Telescope git_branches<cr>", { desc = "Git branches (switch)" })
    map("n", "<leader>gs", "<cmd>Telescope git_status<cr>", { desc = "Git status" })
    map("n", "<leader>gc", "<cmd>Telescope git_commits<cr>", { desc = "Git commits" })
    map("n", "<leader>gC", "<cmd>Telescope git_bcommits<cr>", { desc = "Git commits (buffer)" })

    -- VSCode-style Ctrl keymaps (reliable in all terminals)
    map("n", "<C-p>", "<cmd>Telescope find_files<cr>", { desc = "Find files (Ctrl+P)" })
    map("n", "<C-S-f>", "<cmd>Telescope live_grep<cr>", { desc = "Live grep (Ctrl+Shift+F)" })
  end,
}
