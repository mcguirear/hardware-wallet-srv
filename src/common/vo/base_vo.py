# -*- coding: utf-8 -*-
import json
from decimal import Decimal
from datetime import datetime
from datetime import date, time


class BaseFloat(float):
	def __init__(self, value):
		self._value = value
	
	def __repr__(self):
		return str(self._value)


class BaseJsonEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, datetime):
			return obj.strftime('%Y-%m-%d %H:%M:%S')
		elif isinstance(obj, date):
			return obj.strftime('%Y-%m-%d')
		elif isinstance(obj, Decimal):
			# return str(obj)
			return BaseFloat(obj)
		elif isinstance(obj, time):
			return obj.strftime("%H:%M:%S")
		else:
			return json.JSONEncoder.default(self, obj)


def copy_vo(source, target):
	data = target.__dict__
	for (k, v) in data.items():
		if hasattr(source, k):
			setattr(target, k, getattr(source, k))


def obj_to_dict(obj):
	dic = {}
	for field in dir(obj):
		val = getattr(obj, field)
		if not field.startswith("__") and not callable(val) and not field.startswith("_"):
			dic[field] = val
	return dic


class BaseVO(object):
	def to_dict(self, **kwargs):
		deep = kwargs.get("deep", False)
		skip_none = kwargs.get("skip_none", False)
		skip_empty = kwargs.get("skip_empty", False)
		dic = {}
		for field in dir(self):
			val = getattr(self, field)
			if not field.startswith("__") and not callable(val) and not field.startswith("_"):
				if isinstance(val, BaseVO):
					dic[field] = val.to_dict(deep=deep)
				else:
					if skip_none and val is None:
						continue
					if skip_empty and not val:
						continue
					dic[field] = val
		return dic
	
	def init(self, data):
		if not data:
			return
		if isinstance(data, str):
			data = json.loads(data)
		if not isinstance(data, dict):
			return
		for k, v in data.items():
			if hasattr(self, k):
				setattr(self, k, v)
	
	def serialize(self):
		return json.dumps(self.to_dict(deep=True), cls=BaseJsonEncoder, ensure_ascii=False)
	
	def __repr__(self) -> str:
		return self.serialize()


class BaseLoginUserVo(BaseVO):
	
	def __init__(self):
		self.id = ""


class AdminUserVo(BaseLoginUserVo):
	
	def __init__(self):
		super().__init__()
		self.id = 0
		self.username = ""
		self.role_id = 0
		self.nickname = ""
		self.email = ""
		self.email_valid = ""
		self.phone = ""
		self.is_superuser = 0
		self.is_staff = 0
		self.is_active = 0
		self.sex = ""
		self.parent_id = 0
		self.role_name = ""
		self.data_perm_type = 0
		self.sub_users = []
		self.create_time = ""
