# -*- coding: utf-8 -*-
import importlib
import json
from datetime import datetime, date, time
from decimal import Decimal

from common.vo.base_vo import BaseVO

from xlib import xlog

logger = xlog.getLogger()


class fakeFloat(float):
	def __init__(self, value):
		self._value = value
	
	def __repr__(self):
		return str(self._value)


class XJsonEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, datetime):
			return obj.strftime('%Y-%m-%d %H:%M:%S')
		elif isinstance(obj, date):
			return obj.strftime('%Y-%m-%d')
		elif isinstance(obj, Decimal):
			# return str(obj)
			return fakeFloat(obj)
		elif isinstance(obj, time):
			return obj.strftime("%H:%M:%S")
		else:
			return json.JSONEncoder.default(self, obj)


def getFieldClass(field_name, field):
	t = type(field)
	obj_name = t.__name__
	obj_module = type(field).__module__
	m = importlib.import_module(obj_module, obj_name)
	# print("字段: %s，归属包：%s， 类型：%s" % (field_name, obj_module, obj_name))
	obj_class = getattr(m, obj_name)
	return obj_class


def __parseObject(data, cls):
	"""

	:return:
	"""
	if isinstance(data, (list, tuple, set)):
		instance_list = list()
		for row_data in data:
			instance = cls()
			for k, v in row_data.items():
				if not hasattr(instance, k):
					continue
				field = getattr(instance, k)
				if field is None:
					setattr(instance, k, v)
					continue
				type_name = type(field).__name__
				if type_name in ("int", "float", "bool", "complex", "str", 'dict'):
					setattr(instance, k, v)
				else:
					val = __parseObject(v, cls=getFieldClass(k, field))
					setattr(instance, k, val)
			instance_list.append(instance)
		return instance_list
	if isinstance(data, dict):
		instance = cls()
		for k, v in data.items():
			if not hasattr(instance, k):
				continue
			field = getattr(instance, k)
			if field is None:
				setattr(instance, k, v)
				continue
			type_name = type(field).__name__
			# print("field:%s, value:%s, type:%s, type_name:%s" % (field, v, type(field), type_name))
			if type_name in ("int", "float", "bool", "complex", "str", 'dict'):
				setattr(instance, k, v)
			else:
				val = __parseObject(v, cls=getFieldClass(k, field))
				setattr(instance, k, val)
		return instance
	return data


def parseObject(data: str, cls):
	if isinstance(data, str):
		data = json.loads(data)
	return __parseObject(data, cls)


def __copy_dict_field(out_dic, field, val, skip_none=False, skip_empty=False):
	if field.startswith("__"):
		return
	if field.startswith("_"):
		return
	if callable(val):
		# print("函数:%s,%s" % (field, val,))
		return
	if skip_none and val is None:
		return
	if skip_empty and not val:
		return
	if not val:
		out_dic[field] = val
		return
	
	if isinstance(val, (int, float, bool, complex, str, dict, Decimal, datetime, date, time)):
		out_dic[field] = val
		return
	if isinstance(val, (list, tuple, set)):
		val_list = []
		for row_data in val:
			row_val = toDict(row_data, skip_none, skip_empty)
			val_list.append(row_val)
		out_dic[field] = val_list
	else:
		out_dic[field] = toDict(val)


def toDict(obj, skip_none=False, skip_empty=False, **kwargs):
	if isinstance(obj, (str, int, float, datetime, date, time)):
		return obj
	
	if isinstance(obj, Decimal):
		return fakeFloat(obj)
	
	if isinstance(obj, (list, tuple, set)):
		val_list = []
		for row_data in obj:
			row_val = toDict(row_data, skip_none, skip_empty)
			val_list.append(row_val)
		return val_list
	
	if isinstance(obj, dict):
		dic = dict()
		for k, v in obj.items():
			if isinstance(obj, (list, tuple, set)):
				dic[k] = toDict(v, skip_none, skip_empty)
			else:
				__copy_dict_field(dic, k, v, skip_none, skip_empty)
		return dic
	
	dic = dict()
	for field in dir(obj):
		val = getattr(obj, field)
		# print("field[%s]=%s,type: %s" % (field, val, type(val)))
		if isinstance(obj, (list, tuple, set)):
			dic[field] = toDict(val, skip_none, skip_empty)
		else:
			__copy_dict_field(dic, field, val, skip_none, skip_empty)
	return dic


def toJSONString(obj, **kwargs):
	data = toDict(obj, **kwargs)
	return json.dumps(data, cls=XJsonEncoder, **kwargs)
