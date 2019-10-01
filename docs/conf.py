from stenotype import __version__


# -- Project information -----------------------------------------------------
project = 'stenotype'
copyright = '2019, Arne'
author = 'Arne Recknagel'
release = __version__


# -- General configuration ---------------------------------------------------
templates_path = ['_templates']
extensions = [
    # builtin modules
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.coverage",
    "sphinx.ext.githubpages",

    # installed modules
    "sphinxcontrib.contentui",
    "sphinx_rtd_theme",
]


# -- Autodoc configuration ---------------------------------------------------
autodoc_member_order = "bysource"


# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']
html_logo = '_static/typewriter-48.png'
