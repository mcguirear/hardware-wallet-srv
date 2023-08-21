#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ---  标准库  ---
import sys
import logging

from gevent import monkey
from gevent import pywsgi

from app.wallet import app_config

from xlib import xparser
from xlib import xlog
from db import db_redis

if sys.platform != "win32":
	monkey.patch_all()

if __name__ == '__main__':
	# 获取命令行参数
	options = xparser.get(version="%s v%s" % (app_config.SYSTEM_NAME, app_config.VERSION), port=app_config.LISTEN_PORT)
	app_config.DEBUG = options.debug
	app_config.LISTEN_PORT = options.port
	# 初始日志
	xlog.initLogger("../logs/%s/" % (app_config.SYSTEM_NAME,), "%s.log" % (app_config.SYSTEM_NAME,), app_config.DEBUG)
	logger = xlog.getLogger()
	logger.info(u"初始日志配置完成")
	logger.setLevel(logging.DEBUG)
	
	from app.wallet.app_sio import app
	from app.wallet import app_config
	from app.wallet import app_authorize
	
	# 初始redis
	db_redis.initRedis()
	# 初始化session管理
	app_authorize.initSession(app_config.SYSTEM_NAME)
	
	from app.wallet import app_cron
	
	# 开始定时任务
	app_cron.startCron(options.master)
	
	# 导入接口
	from app.wallet.controller import base_api
	from app.wallet.controller import wallet_api
	
	# 启动服务
	logger.info(u"开始启动[%s]服务监听端口[%s] debug[%s] master[%s] " % (app_config.SYSTEM_NAME, app_config.LISTEN_PORT, options.debug, options.master))
	http = pywsgi.WSGIServer(('0.0.0.0', app_config.LISTEN_PORT), app)
	http.serve_forever()
