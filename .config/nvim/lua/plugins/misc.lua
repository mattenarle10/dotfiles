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
      local function repo_root()
        local root = vim.fn.systemlist("git rev-parse --show-toplevel")[1]
        if vim.v.shell_error == 0 and root and root ~= "" then
          return root
        end
        return vim.loop.cwd()
      end

      local function file_exists(path)
        return vim.uv.fs_stat(path) ~= nil
      end

      local function command_output(command)
        if vim.fn.executable(command[1]) ~= 1 then
          return nil
        end

        local output = vim.fn.systemlist(command)[1]
        if vim.v.shell_error ~= 0 or not output or output == "" then
          return nil
        end

        return output
      end

      local function repo_runtime()
        local root = repo_root()
        local runtimes = {}

        if file_exists(root .. "/package.json") or file_exists(root .. "/.nvmrc") or file_exists(root .. "/.node-version") then
          local node = command_output({ "node", "--version" })
          if node then
            table.insert(runtimes, " " .. node:gsub("^v", ""))
          end
        end

        if file_exists(root .. "/requirements.txt") or file_exists(root .. "/pyproject.toml") or file_exists(root .. "/uv.lock") then
          local python = command_output({ "python3", "--version" })
          if python then
            table.insert(runtimes, " " .. python:gsub("^Python ", ""))
          end
        end

        if file_exists(root .. "/Cargo.toml") then
          local rust = command_output({ "rustc", "--version" })
          if rust then
            table.insert(runtimes, " " .. (rust:match("rustc%s+([^%s]+)") or rust))
          end
        end

        if file_exists(root .. "/go.mod") then
          local go = command_output({ "go", "version" })
          if go then
            table.insert(runtimes, " " .. (go:match("go version go([^%s]+)") or go))
          end
        end

        if file_exists(root .. "/pom.xml") or file_exists(root .. "/build.gradle") or file_exists(root .. "/build.gradle.kts") then
          local java = command_output({ "java", "-version" })
          if java then
            table.insert(runtimes, " " .. (java:match('"([^"]+)"') or java))
          end
        end

        return table.concat(runtimes, " ")
      end

      local colors = {
        bg = "NONE",
        fg = "#cdd6f4",
        muted = "#a6adc8",
        panel = "#111827",
        royal = "#2563eb",
        royal_soft = "#60a5fa",
        red = "#f38ba8",
        yellow = "#f9e2af",
      }

      require("lualine").setup({
        options = {
          theme = {
            normal = {
              a = { fg = colors.fg, bg = colors.royal, gui = "bold" },
              b = { fg = colors.fg, bg = colors.panel },
              c = { fg = colors.muted, bg = colors.bg },
            },
            insert = {
              a = { fg = colors.fg, bg = colors.royal_soft, gui = "bold" },
              b = { fg = colors.fg, bg = colors.panel },
              c = { fg = colors.muted, bg = colors.bg },
            },
            visual = {
              a = { fg = colors.fg, bg = "#4338ca", gui = "bold" },
              b = { fg = colors.fg, bg = colors.panel },
              c = { fg = colors.muted, bg = colors.bg },
            },
            replace = {
              a = { fg = colors.panel, bg = colors.red, gui = "bold" },
              b = { fg = colors.fg, bg = colors.panel },
              c = { fg = colors.muted, bg = colors.bg },
            },
            command = {
              a = { fg = colors.panel, bg = colors.yellow, gui = "bold" },
              b = { fg = colors.fg, bg = colors.panel },
              c = { fg = colors.muted, bg = colors.bg },
            },
            inactive = {
              a = { fg = colors.muted, bg = colors.bg },
              b = { fg = colors.muted, bg = colors.bg },
              c = { fg = colors.muted, bg = colors.bg },
            },
          },
          transparent = true,
          component_separators = { left = "", right = "" },
          section_separators = { left = "", right = "" },
        },
        sections = {
          lualine_a = {
            {
              "mode",
              fmt = function(mode)
                return mode:sub(1, 1)
              end,
            },
          },
          lualine_b = {
            {
              "branch",
              icon = "",
            },
            {
              "diff",
              symbols = { added = "+", modified = "~", removed = "-" },
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
              repo_runtime,
              color = { fg = colors.royal_soft, bg = colors.bg, gui = "bold" },
            },
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
