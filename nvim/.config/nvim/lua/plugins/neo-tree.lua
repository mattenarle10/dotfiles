-- File explorer
return {
  "nvim-neo-tree/neo-tree.nvim",
  branch = "v3.x",
  dependencies = {
    "nvim-lua/plenary.nvim",
    "nvim-tree/nvim-web-devicons",
    "MunifTanjim/nui.nvim",
  },
  config = function()
    require("neo-tree").setup({
      close_if_last_window = true,
      window = {
        width = 30,
      },
      filesystem = {
        follow_current_file = {
          enabled = true,
        },
        use_libuv_file_watcher = true,
      },
    })

    -- Keymaps
    vim.keymap.set("n", "<leader>e", "<cmd>Neotree toggle<cr>", { desc = "Toggle file explorer" })
    vim.keymap.set("n", "<leader>o", "<cmd>Neotree focus<cr>", { desc = "Focus file explorer" })
  end,
}
