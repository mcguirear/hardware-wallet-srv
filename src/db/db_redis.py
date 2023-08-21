#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
import config

CACHE_REDIS = None
""":type :redis.Redis"""


def createRedis(host, passwd, port, db=0):
	"""
	初始化redis句柄
	:rtype : redis.Redis
	:param host:
	:param passwd:
	:param port: 端口
	:param db: 数据库索引
	:return: redis句柄
	"""
	con_pool = redis.ConnectionPool(host=host, password=passwd, port=port, db=db, decode_responses=True)
	redis_handler = redis.Redis(connection_pool=con_pool)
	redis_handler.ping()
	return redis_handler


def initRedis():
	global CACHE_REDIS
	_config = config.DB_CONFIG_LIST["CACHE_REDIS"]
	CACHE_REDIS = createRedis(_config["host"], _config["passwd"], _config["port"], _config["db"])


def getRedis():
	""" 返回初始化后Redis的实例
	:return:  返回初始化后Redis的实例
	:rtype redis.Redis
	"""
	return CACHE_REDIS
