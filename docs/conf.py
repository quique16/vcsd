import os
import sys

# Add project root to sys.path for autodoc
sys.path.insert(0, os.path.abspath('..'))

project = 'VisioCrypt'
extensions = ['sphinx.ext.autodoc']
templates_path = ['_templates']
exclude_patterns = []

html_theme = 'alabaster'

autodoc_member_order = 'bysource'
