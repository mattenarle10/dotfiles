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
    telescope.setup({
      defaults = {
        file_ignore_patterns = { "node_modules", ".git/" },
      },
    })
    telescope.load_extension("fzf")

    -- Keymaps
    local map = vim.keymap.set
    map("n", "<leader>ff", "<cmd>Telescope find_files<cr>", { desc = "Find files" })
    map("n", "<leader>fg", "<cmd>Telescope live_grep<cr>", { desc = "Find text" })
    map("n", "<leader>fb", "<cmd>Telescope buffers<cr>", { desc = "Find buffers" })
    map("n", "<leader>fh", "<cmd>Telescope help_tags<cr>", { desc = "Find help" })
    map("n", "<leader>fr", "<cmd>Telescope oldfiles<cr>", { desc = "Recent files" })
  end,
}
