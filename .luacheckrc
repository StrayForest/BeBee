-- Keep project lint behavior explicit and compatible with Defold's documented defaults.
unused_args = false
max_line_length = false
ignore = {
    "611", -- line contains only whitespace; repository standards checker owns whitespace
    "612", -- trailing whitespace; repository standards checker owns whitespace
    "614", -- trailing whitespace in comments; repository standards checker owns whitespace
}
