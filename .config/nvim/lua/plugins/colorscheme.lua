return {
  {
    "catppuccin/nvim",
    name = "catppuccin",
    lazy = false,
    priority = 1000,
    config = function()
      local royal = "#3b82f6"
      local royal_soft = "#93c5fd"
      local panel = "#172033"
      local panel_light = "#22345a"

      require("catppuccin").setup({
        flavour = "mocha", -- latte, frappe, macchiato, mocha
        transparent_background = true,  -- Enable transparency to match Ghostty
        color_overrides = {
          mocha = {
            blue = royal_soft,
            sapphire = royal,
          },
        },
        styles = {
          comments = { "italic" },
          conditionals = {},
        },
        integrations = {
          telescope = true,
          neotree = true,
          treesitter = true,
          which_key = true,
          gitsigns = true,
        },
        custom_highlights = function(colors)
          return {
            CursorLine = { bg = panel },
            CursorLineNr = { fg = royal_soft, style = { "bold" } },
            LineNr = { fg = colors.overlay0 },
            WinSeparator = { fg = royal },
            FloatBorder = { fg = royal, bg = "NONE" },
            NormalFloat = { bg = "NONE" },
            Pmenu = { bg = panel, fg = colors.text },
            PmenuSel = { bg = royal, fg = colors.text, style = { "bold" } },
            TelescopeBorder = { fg = royal, bg = "NONE" },
            TelescopeSelection = { bg = panel_light, fg = colors.text, style = { "bold" } },
            NeoTreeDirectoryName = { fg = royal_soft },
            NeoTreeDirectoryIcon = { fg = royal_soft },
          }
        end,
      })
      vim.cmd([[colorscheme catppuccin-mocha]])

      -- Extra transparency for backgrounds
      vim.api.nvim_set_hl(0, "Normal", { bg = "none" })
      vim.api.nvim_set_hl(0, "NormalFloat", { bg = "none" })
      vim.api.nvim_set_hl(0, "NormalNC", { bg = "none" })
    end,
  },
}
