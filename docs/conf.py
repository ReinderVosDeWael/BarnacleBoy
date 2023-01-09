# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "BarnacleBoy"
copyright = "2023, Reinder Vos de Wael"
author = "Reinder Vos de Wael"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinxdoc"
html_static_path = ["_static"]

# Autoapi configuration
extensions.append("autoapi.extension")
autoapi_type = "python"
autoapi_dirs = ["../barnacleboy"]

# Nb-sphinx configuration
extensions.append("nbsphinx")
