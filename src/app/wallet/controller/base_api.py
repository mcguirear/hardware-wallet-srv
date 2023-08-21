# -*- coding: utf-8 -*-

import os
import json
import hashlib
from flask import request, make_response

import config
from app.wallet import app_config
from app.wallet.app_sio import app
from app.wallet.app_authorize import deal_handler, AppSession

from error_info_config import ErrKey

from xlib import xlog

logger = xlog.getLogger()


@app.route('/')
def wallet_index():
	info = {'version': app_config.VERSION, 'name': app_config.SYSTEM_NAME}
	return json.dumps(info, indent=2, ensure_ascii=False)