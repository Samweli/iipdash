# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys
from pathlib import Path

import django

import sphinx_rtd_theme  # noqa: F401

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iipdash.settings")
django.setup()


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "IIP Dashboard"
copyright = """2024, Tehamalab"""
author = "Tehamalab"
release = "0.1.0"

# Document options for latex_documents, man_pages, texinfo etc
doc_name = "iipdash"
doc_title = "IIP Dashboard Documentation"
doc_description = "Integrated Infrastructure Planning (IIP) Dashboard"


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.napoleon",  # Supports Google and NumPy docstrings
    "sphinx.ext.autodoc",  # Extracts docstrings
    "sphinx.ext.viewcode",  # Links to source code
    # 'sphinx.ext.intersphinx',  # Links to other projects (optional)
    # 'sphinx.ext.autosummary',  # Generates summary tables
    "sphinxcontrib.spelling",  # Checks the spelling errors, typos etc
    "sphinx_rtd_theme",  # ReadTheDocs-style theme
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix of source filenames.
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# The master toctree document.
master_doc = "index"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "*_test.py", "**/migrations/*"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for Spelling checker -------------------------------------------------
# https://sphinxcontrib-spelling.readthedocs.io/en/latest/customize.html

# String specifying the language, as understood by PyEnchant and enchant.
spelling_lang = "en_US"

# String specifying a file containing a list of words known to be spelled
# correctly but that do not appear in the language dictionary selected by
# `spelling_lang`. The file should contain one word per line.
#
spelling_word_list_filename = "spelling_wordlist.txt"

# Boolean controlling whether a misspelling is emitted as a sphinx warning
# or as an info message.
spelling_warning = True


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


# -- Options for HTMLHelp output ---------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "iipdashdoc"


# -- Options for autodoc output ---------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#configuration

# Define the order in which automodule and autoclass members are listed
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#confval-autodoc_member_order
autodoc_member_order = "bysource"


# -- Options for LaTeX output ------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass
# [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        f"{doc_name}.tex",
        doc_title,
        author,
        "manual",
    ),
]


# -- Options for manual page output ------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (
        master_doc,
        doc_name,
        doc_title,
        [author],
        1,
    ),
]


# -- Options for Texinfo output ----------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        doc_name,
        doc_title,
        author,
        doc_name,
        doc_description,
        "Miscellaneous",
    ),
]
