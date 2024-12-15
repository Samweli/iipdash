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
from sphinx.application import Sphinx
from sphinx.ext import autodoc
from sphinx.util import logging
from sphinx.util.typing import ExtensionMetadata

logger = logging.getLogger(__name__)

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
    "sphinx.ext.intersphinx",  # Link to other project docs (e.g, Django)
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
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "*_test.py",
    "**/migrations/*",
]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for intersphinx extension -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html

# This config value contains the locations and names of other projects that
# should be linked to in this documentation.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "django": (
        "https://docs.djangoproject.com/en/stable/",
        "https://docs.djangoproject.com/en/stable/_objects/",
    ),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}


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


# -- Extensions ----------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#event-autodoc-skip-member


def skip_members(
    app: Sphinx,
    what: str,
    name: str,
    obj: object,
    skip: bool | None,
    options: autodoc.Options,
) -> bool | None:
    """
    Hook for the `autodoc-skip-member` event to include or exclude certain members.

    This function decides whether a member (e.g., method, attribute) of a
    class or module should be skipped from documentation. Members are excluded
    based on specific rules, such as being in a predefined exclusion list or
    having specific naming conventions.

    Args:
        app (Sphinx):
            The Sphinx application object.

        what (str):
            The type of the object which the docstring belongs
            to (e.g., "module", "class", "method", "attribute").

        name (str):
            The fully qualified name of the object.

        obj (object):
            The member object itself (e.g., function, method, attribute).

        skip (bool | None):
            A boolean indicating if autodoc will skip this member if the user
            handler does not override the decision

        options (autodoc.Options):
            The options given to the directive: an object with attributes
            `inherited_members`, `undoc_members`, `show_inheritance`
            and `no-index` that are true if the flag option of same name was
            given to the auto directive

    Returns:
        bool:
            - `True` if the member should be skipped.
            - `False` if the member should be included.

    See Also:
        https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#event-autodoc-skip-member
    """
    DJANGO_EXCLUDE_MODULES = [
        # models.Model fields, which are picked from class attributes
        "django.db.models.query_utils",
        "django.db.models.fields.related_descriptors",
    ]
    DJANGO_EXCLUDE_NAMES = [
        # apps.users.models.User
        "get_next_by_date_joined",
        "get_previous_by_date_joined",
        # BaseModelAdmin
        "declared_fieldsets",
        # "fieldsets",
        "media",
    ]

    member_cls = type(obj)
    member_module = member_cls.__module__

    ignored_name = name in DJANGO_EXCLUDE_NAMES
    ignored_module = what == "class" and member_module in DJANGO_EXCLUDE_MODULES
    if ignored_name or ignored_module:
        skip = True
    return skip


def setup(app: Sphinx) -> ExtensionMetadata:
    """
    Allow this module to be used as Sphinx extension.

    It connects :func:`skip_member` function to the
    sphinx events :event:`autodoc-skip-member` allowing dynamic control over
    which members are included or excluded from the documentation.

    Args:

        app (sphinx.application.Sphinx):
            The Sphinx application object.

    Returns:
        ExtensionMetadata:
            The metadata returned by this extension.

    See Also:
        https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#event-autodoc-skip-member
    """
    app.connect("autodoc-skip-member", skip_members)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
