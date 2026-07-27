import os
import sys

# Tell Passenger explicitly which Python virtualenv to use
INTERP = os.path.expanduser('~/virtualenv/flask_app/3.11/bin/python')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, os.path.dirname(__file__))

from test import app as application
#lol