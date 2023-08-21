# -*- coding: utf-8 -*-
import enum


class BaseIntEnum(object):
	
	def __init__(self, v):
		self._v = v
	
	def __str__(self):
		l = dir(self)
		for attr in l:
			if attr.startswith("__"):
				continue
			v = getattr(self, attr)
			if isinstance(v, int):
				if v == self._v:
					return attr
		return "-"


class EUserDataPermType(object):
	"""
	管理后台用户的数据权限类别
	"""
	Self = 0  # 只可查看自己创建的数据
	SelfAndSub = 1  # 可查看自己和下级用户创建的数据
	All = 2  # 可查看全部数据


class ESystemName(object):
	"""
	系统名称定义
	"""
	Admin = "admin"
	Channel = "channel"


class ERoleName(object):
	"""
	角色名称定义
	"""
	Admin = "admin"
	Channel = "channel"


class EUserActiveStatus(BaseIntEnum):
	"""
	用户状态类型
	"""
	Enable = 1  # 可用
	Disable = 2  # 禁用
