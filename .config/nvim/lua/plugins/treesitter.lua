-- Better syntax highlighting
return {
  "nvim-treesitter/nvim-treesitter",
  build = ":TSUpdate",
  config = function()
    require("nvim-treesitter.configs").setup({
      ensure_installed = {
        "lua", "vim", "vimdoc",
        "javascript", "typescript", "tsx",
        "python", "rust", "go",
        "html", "css", "json", "yaml",
        "markdown", "markdown_inline",
        "bash",
      },
      highlight = { enable = true },
      indent = { enable = true },
    })
  end,
}
