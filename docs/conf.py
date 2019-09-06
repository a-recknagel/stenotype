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


# -- Options for HTML output -------------------------------------------------
html_static_path = ['_static']
html_logo = '_static/construction-64.png'
