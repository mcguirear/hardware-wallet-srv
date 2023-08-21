#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

import os
import logging.config
from logging import Logger

# 定义三种日志输出格式 开始
# standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d] [%(levelname)s][%(message)s]'  # 其中name为getlogger指定的名字
standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][%(filename)s:%(lineno)d] [%(levelname)s][%(message)s]'  # 其中name为getlogger指定的名字

simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'

id_simple_format = '[%(levelname)s][%(asctime)s] %(message)s'

# 定义日志输出格式 结束
current_dir = os.path.dirname(os.path.abspath(__file__))  # log文件的目录


def initLogger(aDir, aFilename, debug=True):
	# 如果不存在定义的日志目录就创建一个
	aDir = os.path.abspath(aDir)
	if not os.path.exists(aDir):
		os.makedirs(aDir)
	# log文件的全路径
	logfile_path = os.path.join(aDir, aFilename)
	
	# log配置字典
	LOGGING_DIC = {
		'version': 1,
		'disable_existing_loggers': False,
		'formatters': {
			'standard': {
				'format': standard_format
			},
			'simple': {
				'format': simple_format
			},
		},
		'filters': {},
		'handlers': {
			# 打印到终端的日志
			'console': {
				'level': 'DEBUG',
				'class': 'logging.StreamHandler',  # 打印到屏幕
				'formatter': 'standard'
			},
			# 打印到文件的日志,收集info及以上的日志
			'default': {
				'level': 'DEBUG',
				'class': 'logging.handlers.TimedRotatingFileHandler',  # 保存到文件
				'formatter': 'standard',
				'filename': logfile_path,  # 日志文件
				"when": 'D',  # “H”: Hours  “D”: Days  “W”: Week day (0=Monday)
				"interval": 1,  # 间隔时间 表示每天产生一个日志文件；
				'backupCount': 30,
				'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
			},
		},
		'loggers': {
			# logging.getLogger(__name__)拿到的logger配置
			'': {
				'handlers': ['default', 'console'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
				'level': 'INFO',
				'propagate': True,  # 向上（更高level的logger）传递
			},
			'engineio': {
				'handlers': ['default', 'console'],
				'level': 'WARN',
				'propagate': False,
			},
			'socketio': {
				'handlers': ['default', 'console'],
				'level': 'INFO',
				'propagate': False,
			},
			'socketIO-client-2': {
				'handlers': ['default', 'console'],
				'level': 'INFO',
				'propagate': False,
			}
		},
	}
	if not debug:
		# 不是debug状态，去掉控制打印
		loggers = LOGGING_DIC.get("loggers")
		for name, conf in loggers.items():
			handlers = conf.get("handlers")
			if handlers and "console" in handlers:
				handlers.remove("console")
	
	logging.config.dictConfig(LOGGING_DIC)
	# engineioLogger = getLogger("engineio")
	# engineioLogger.info("ABCDEF")
	return True


def getLogger(name=None):
	"""
	:param name:
	:return:
	:rtype :Logger
	"""
	if not name:
		name = __name__
	return logging.getLogger(name)  # 生成一个log实例
