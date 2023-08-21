#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import time
import json
import functools
import hashlib

from flask import request, make_response, current_app
from werkzeug.wrappers import Response

from common.json_util import XJsonEncoder
from common.vo.base_vo import BaseLoginUserVo
from db.db_redis import getRedis
from xlib.flask_util import get_real_ip

from common.XSession import RedisSession
from app.wallet import app_config
from xlib import xlog

logger = xlog.getLogger()

G_AppSession = None
""":rtype :RedisSession"""


class LoginUserVo(BaseLoginUserVo):
	
	def __init__(self):
		super().__init__()
		self.id = ""
		self.uid = ""
		self.nickname = ""
		self.head_img = ""
		self.pv = ""
		self.ip = ""


def initSession(group):
	global G_AppSession
	G_AppSession = RedisSession(group, 30 * 10)
	""":rtype :RedisSession"""
	return G_AppSession


def AppSession():
	"""
	:return:
	:rtype : RedisSession
	"""
	return G_AppSession


def getLoginUser(token):
	"""
	通过token获取缓存的登录用户信息
	:rtype LoginUserVo
	"""
	aKey = AppSession().HALL_SESSION_KEY % (token,)
	data = getRedis().get(aKey)
	user = LoginUserVo()
	user.init(data)
	return user


def build_sign(data, key):
	sign_str = "%s%s" % (data, key)  # 增加key参数
	my_sign = hashlib.md5(sign_str.encode("utf-8")).hexdigest()
	logger.info("待签名字符串[%s]，生成的签名为[%s]" % (sign_str, my_sign))
	return my_sign


def inner_deal(func, vkwargs, *args, **kwargs):
	try:
		arguments = request.args.to_dict()
		arguments2 = request.form.to_dict()
		arguments3 = None
		try:
			arguments3 = request.get_json()
		except:
			pass
		# logger.info("method:%s, arguments:%s,arguments2:%s,request.data:%s,arguments3:%s,mimetype:%s,data:%s" % (request.method, arguments, arguments2, request.data, request.mimetype, arguments3, data))
		arguments.update(arguments2)
		if arguments3:
			arguments.update(arguments3)
		
		ip = get_real_ip(request)
		# 判断是否校验签名
		if vkwargs.get("check_sign"):
			data = request.get_data(True, True)
			sign = request.headers.get("x-sign")
			if not sign:
				# 没有sign参数
				logger.info("参数错误：sign为空，参数[%s]" % (arguments,))
				return config.getErrInfo("ParamErr", "sign为空")
			if not data:
				logger.info("参数错误：data为空，参数[%s]" % (arguments,))
				return config.getErrInfo("ParamErr", "data为空")
			
			c_sign = build_sign(data, config.WALLET_APP_KEY)
			if c_sign != sign:
				# 签名不对
				logger.info("参数错误：sign错误，参数[%s]" % (arguments,))
				return config.getErrInfo("AuthErr")
		
		# 判断是否需要校验token
		if vkwargs.get("check_token"):
			token = arguments.get("token")
			if not token:  # 如参数中没有传token, 从cookie中取
				token = request.cookies.get("token")
				if token:
					arguments["token"] = token
			
			if not token:  # 如参数中没有传token,参数从header中取
				token = request.headers.get("X-Token")
				if token:
					arguments["token"] = token
			
			if not token:
				logger.info(u"参数错误：token[%s]为空，参数[%s]" % (token, arguments))
				return config.getErrInfo("TokenErr")
			
			if not AppSession().checkToken(token):
				# token失效
				logger.info(u"Token错误：使用的token[%s]已经失效，参数[%s]" % (token, arguments))
				return config.getErrInfo("TokenErr")
			userVo = getLoginUser(token)
			if not userVo:
				return config.getErrInfo("TokenErr")
			arguments["_uid"] = str(userVo.id)
		
		start_time = time.time() * 1000
		respData = func(arguments, ip=ip, handler=request, **kwargs)
		used_time = int((time.time() * 1000) - start_time)
		logger.info("请求[%s]用时[%sms]，输入参数[%s]" % (request.path, used_time, arguments))
		return respData
	except Exception as ex:
		logger.exception(str(ex))
	return config.getErrInfo("SystemErr")


def deal_handler(**vkwargs):
	def wrapper(func):
		@functools.wraps(func)
		def _wrapper(*args, **kwargs):
			logger.info("method: %s,func:%s, vkwargs:%s,args:%s,kwargs:%s" % (
				request.method.upper(), func, vkwargs, args, kwargs))
			if "OPTIONS" == request.method.upper():
				resp = make_response("")
				resp.headers['Access-Control-Allow-Origin'] = app_config.ACCESS_CONTROL_ALLOW_ORIGIN
				resp.headers['Access-Control-Allow-Credentials'] = 'true'
				resp.headers['Access-Control-Allow-Headers'] = 'X-Requested-With, X-Token, Content-Type'
				resp.headers['Access-Control-Allow-Methods'] = 'OPTIONS, POST, GET'
				# resp.headers['Access-Control-Max-Age'] = "1000"
				resp.headers['Access-Control-Max-Age'] = '0'
				return resp
			
			start_time = time.time() * 1000
			respData = inner_deal(func, vkwargs, *args, **kwargs)
			used_time = int(time.time() * 1000 - start_time)
			if isinstance(respData, Response):
				resp = respData
			elif isinstance(respData, str):
				resp = make_response(respData)
				
				if len(respData) < 512:
					logger.info("请求[%s]用时[%sms]，返回[%s]" % (request.path, used_time, respData))
				else:
					logger.info("请求[%s]用时[%sms]，返回内容长度大于512" % (request.path, used_time,))
			
			elif isinstance(respData, dict):
				respData = json.dumps(respData, cls=XJsonEncoder, ensure_ascii=False)
				if len(respData) < 512:
					logger.info("请求[%s]用时[%sms]，返回[%s]" % (request.path, used_time, respData))
				else:
					logger.info("请求[%s]用时[%sms]，返回内容长度大于512" % (request.path, used_time,))
				
				resp = make_response(respData)
				resp.headers['Content-type'] = 'application/json;charset=utf-8'
			else:
				resp = make_response(str(respData))
			
			# 跨域设置
			resp.headers['Access-Control-Allow-Origin'] = app_config.ACCESS_CONTROL_ALLOW_ORIGIN
			resp.headers['Access-Control-Allow-Credentials'] = 'true'
			resp.headers['Access-Control-Allow-Headers'] = 'X-Requested-With, X-Token, Content-Type'
			resp.headers['Access-Control-Allow-Methods'] = 'OPTIONS, POST, GET'
			resp.headers['Access-Control-Max-Age'] = '0'
			return resp
		
		return _wrapper
	
	return wrapper
