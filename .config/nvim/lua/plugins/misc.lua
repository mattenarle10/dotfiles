-- Other useful plugins
return {
  -- Auto pairs
  {
    "windwp/nvim-autopairs",
    event = "InsertEnter",
    config = true,
  },

  -- Comment toggle
  {
    "numToStr/Comment.nvim",
    config = true,
  },

  -- Status line
  {
    "nvim-lualine/lualine.nvim",
    dependencies = { "nvim-tree/nvim-web-devicons" },
    config = function()
      require("lualine").setup({
        options = {
          theme = "auto",
          transparent = true,
        },
        sections = {
          lualine_a = {},
          lualine_b = {
            {
              "branch",
              icon = "",
            },
            {
              "diff",
              symbols = { added = " ", modified = " ", removed = " " },
            },
          },
          lualine_c = {
            {
              "filename",
              path = 1,  -- Show relative path
            },
          },
          lualine_x = {
            {
              "diagnostics",
              sources = { "nvim_lsp" },
              symbols = { error = " ", warn = " ", info = " ", hint = " " },
            },
          },
          lualine_y = { "filetype" },
          lualine_z = { "location", "progress" },
        },
      })
    end,
  },

  -- Which-key (shows keybindings)
  {
    "folke/which-key.nvim",
    event = "VeryLazy",
    config = function()
      require("which-key").setup()
    end,
  },

  -- Surround text objects
  {
    "kylechui/nvim-surround",
    event = "VeryLazy",
    config = true,
  },

  -- Better diagnostics and quickfix
  {
    "folke/trouble.nvim",
    dependencies = { "nvim-tree/nvim-web-devicons" },
    cmd = "Trouble",
    keys = {
      { "<leader>xx", "<cmd>Trouble diagnostics toggle<cr>", desc = "Diagnostics (Trouble)" },
      { "<leader>xX", "<cmd>Trouble diagnostics toggle filter.buf=0<cr>", desc = "Buffer Diagnostics (Trouble)" },
      { "<leader>xl", "<cmd>Trouble lsp toggle focus=false win.position=right<cr>", desc = "LSP Definitions / references / ... (Trouble)" },
      { "<leader>xq", "<cmd>Trouble qflist toggle<cr>", desc = "Quickfix List (Trouble)" },
    },
    opts = {},
  },

  -- Fast navigation with 2-char search
  {
    "folke/flash.nvim",
    event = "VeryLazy",
    opts = {},
    keys = {
      { "s", mode = { "n", "x", "o" }, function() require("flash").jump() end, desc = "Flash" },
      { "S", mode = { "n", "x", "o" }, function() require("flash").treesitter() end, desc = "Flash Treesitter" },
      { "r", mode = "o", function() require("flash").remote() end, desc = "Remote Flash" },
      { "R", mode = { "o", "x" }, function() require("flash").treesitter_search() end, desc = "Treesitter Search" },
    },
  },

  -- Indent guides
  {
    "lukas-reineke/indent-blankline.nvim",
    main = "ibl",
    event = "VeryLazy",
    opts = {
      indent = {
        char = "│",
      },
      scope = {
        enabled = true,
        show_start = false,
        show_end = false,
      },
    },
  },

  -- Quick file navigation
  {
    "ThePrimeagen/harpoon",
    branch = "harpoon2",
    dependencies = { "nvim-lua/plenary.nvim" },
    config = function()
      local harpoon = require("harpoon")
      harpoon:setup()

      vim.keymap.set("n", "<leader>a", function() harpoon:list():add() end, { desc = "Harpoon add file" })
      vim.keymap.set("n", "<C-e>", function() harpoon.ui:toggle_quick_menu(harpoon:list()) end, { desc = "Harpoon menu" })
      vim.keymap.set("n", "<leader>1", function() harpoon:list():select(1) end, { desc = "Harpoon file 1" })
      vim.keymap.set("n", "<leader>2", function() harpoon:list():select(2) end, { desc = "Harpoon file 2" })
      vim.keymap.set("n", "<leader>3", function() harpoon:list():select(3) end, { desc = "Harpoon file 3" })
      vim.keymap.set("n", "<leader>4", function() harpoon:list():select(4) end, { desc = "Harpoon file 4" })
    end,
  },

  -- Auto-detect indentation
  {
    "tpope/vim-sleuth",
  },
}
