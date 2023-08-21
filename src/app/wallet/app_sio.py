# -*- coding: utf-8 -*-
"""
"""

import config
from urllib.parse import quote_plus as urlquote
from flask import Flask
from flask_socketio import SocketIO
from app.wallet import app_config

from xlib import xlog

logger = xlog.getLogger()

app = Flask(__name__, root_path=app_config.APP_DIR)
app.debug = False