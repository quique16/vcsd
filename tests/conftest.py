import os
import sys

# Ensure the src directory is on sys.path so that 'visiocrypt' can be imported
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_DIR = os.path.join(ROOT_DIR, 'src')
for path in (SRC_DIR, ROOT_DIR):
    if path not in sys.path:
        sys.path.insert(0, path)
