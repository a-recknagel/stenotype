from stenotype import __version__


# -- Project information -----------------------------------------------------
project = 'stenotype'
copyright = '2019, auxmoney GmbH'
author = 'Arne Recknagel'
release = __version__


# -- General configuration ---------------------------------------------------
templates_path = ['_templates']
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]


# -- Autodoc configuration ---------------------------------------------------
autodoc_member_order = "bysource"


# -- Options for HTML output -------------------------------------------------
html_static_path = ['_static']
html_logo = '_static/typewriter-48.png'
