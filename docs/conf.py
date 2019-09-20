from stenotype import __version__


# -- Project information -----------------------------------------------------
project = 'stenotype'
copyright = '2019, Arne'
author = 'Arne Recknagel'
release = __version__


# -- General configuration ---------------------------------------------------
templates_path = ['_templates']
extensions = [
    "pallets_sphinx_themes",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.coverage",
    "sphinx.ext.githubpages",
]


# -- Autodoc configuration ---------------------------------------------------
autodoc_member_order = "bysource"


# -- Options for HTML output -------------------------------------------------
html_theme = "flask"  # one of [flask, jinja, werkzeug, click]
html_static_path = ['_static']
html_logo = '_static/typewriter-48.png'
