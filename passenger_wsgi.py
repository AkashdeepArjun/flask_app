

import sys
import os

# Set current directory as working directory
sys.path.insert(0, os.path.dirname(__file__))

# Add cPanel virtual environment site-packages
venv_path = '/home/oa1746zqwkl4/virtualenv/flask_app/3.11/lib/python3.11/site-packages'
if os.path.exists(venv_path):
    sys.path.insert(0, venv_path)

# Import your Flask app instance (assuming your Flask code is in app.py and defined as app = Flask(__name__))
from app import app as application