#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import uuid
from hashlib import md5

from xlib import xlog
from db.db_redis import getRedis
from common.vo.base_vo import AdminUserVo, BaseLoginUserVo
from common.json_util import XJsonEncoder

logger = xlog.getLogger()


class RedisSession:
	
	def __init__(self, group, timeout):
		# token过期时间（单位：分）
		self.TOKEN_TIME_OUT = timeout
		
		self.HALL_SESSION_KEY = "%s:user_token:%%s" % (group,)
		self.HALL_SESSION_UID_KEY = "%s:user_uid2token:%%s" % (group,)
		pass
	
	def create(self, user):
		"""
		创建session,保证用户信息到Session中
		:type user: BaseLoginUserVo
		:return:
		"""
		uid = user.id
		user_info = json.dumps(user.to_dict(), cls=XJsonEncoder)
		t = 60 * self.TOKEN_TIME_OUT
		token = md5(("%s%s" % (uuid.uuid4(), uid)).encode("utf-8")).hexdigest()
		aKey = self.HALL_SESSION_KEY % (token,)
		r = getRedis()
		r.setex(aKey, t, user_info)
		
		# 设置 uid 对 token 的关系
		aKey = self.HALL_SESSION_UID_KEY % (uid,)
		r.setex(aKey, t, token)
		
		logger.info("创建uid[%s]对应的token为[%s]" % (uid, token))
		return token
	
	def setExpireTime(self, token, second):
		"""
		设置token有效期
		:param token:
		:param second:
		:return:
		"""
		aKey = self.HALL_SESSION_KEY % (token,)
		r = getRedis()
		r.expire(aKey, second)  # 设置有效期
	
	def getToken(self, uid):
		"""
		根据uid获取token
		:param uid:
		:return:
		"""
		r = getRedis()
		aKey = self.HALL_SESSION_UID_KEY % (uid,)
		token = r.get(aKey)
		if token: return token
		return None
	
	def delete(self, token):
		"""
		删除Token
		:param token:
		:return:
		"""
		try:
			aKey = self.HALL_SESSION_KEY % (token,)
			data = getRedis().get(aKey)
			if not data:
				return
				
			# 删除token
			getRedis().delete(aKey)
			# 删除uid与token的关系
			userVo = BaseLoginUserVo()
			userVo.init(data)
			aKey = self.HALL_SESSION_UID_KEY % (userVo.id,)
			getRedis().delete(aKey)
		except Exception:
			logger.exception("")
	
	def checkToken(self, token):
		if not token:
			return False
		aKey = self.HALL_SESSION_KEY % (token,)
		if getRedis().ttl(aKey) >0 :
			return True
		return False
	
	def setAdminUser(self, token, user):
		"""
		:type token: str
		:type user: BaseVO
		"""
		aKey = self.HALL_SESSION_KEY % (token,)
		data = json.dumps(user.to_dict(), cls=XJsonEncoder)
		getRedis().set(aKey, data)
	
	def getAdminUser(self, token):
		"""
		:rtype AdminUserVo
		"""
		aKey = self.HALL_SESSION_KEY % (token,)
		data = getRedis().get(aKey)
		user = AdminUserVo()
		user.init(data)
		return user
	
	def ttl(self, token):
		"""
		查看剩余过期时间（秒）
		:param token:
		:return:
		"""
		aKey = self.HALL_SESSION_KEY % (token,)
		return getRedis().ttl(aKey)
	
	def pttl(self, token):
		"""
		查看剩余过期时间（毫秒）
		:param token:
		:return:
		"""
		aKey = self.HALL_SESSION_KEY % (token,)
		return getRedis().pttl(aKey)
