import os
import sys

# Add project root and src directory to sys.path for autodoc
project_root = os.path.abspath('..')
sys.path.insert(0, os.path.join(project_root, 'src'))

project = 'Visiocrypt'
extensions = ['sphinx.ext.autodoc']
templates_path = ['_templates']
exclude_patterns = []

html_theme = 'alabaster'

autodoc_member_order = 'bysource'
