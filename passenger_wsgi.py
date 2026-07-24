import sys
import os

# Add the current directory (project root) to Python's system path
# This allows test.py to find database, data, pack, and utils modules seamlessly!
sys.path.insert(0, os.path.dirname(__file__))

# Import the Flask app object from test.py and alias it as 'application'
from test import app as application
