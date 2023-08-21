#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

import random
import logging
import hashlib

logger = logging.getLogger()


def generateMD5(data):
	return hashlib.md5(data).hexdigest()


def generatePwd():
	"""
	生成8位随机密码的md5值
	:return: 随机密码
	:rtype str
	"""
	Min = 10000000
	Max = 99999999
	pwd = random.randint(Min, Max)
	# 生成md5值
	pwd = hashlib.md5("%s" % (pwd,)).hexdigest()
	return pwd


def generateRandDeskId():
	u"""
	生成随机的房间Id
	:return: 随机密码
	:rtype str
	"""
	Min = 100000
	Max = 999999
	pwd = random.randint(Min, Max)
	return pwd


def buildFileMd5(filename):
	"""
	读取文件的md5
	:param filename:
	:return:
	"""
	f = open(filename, 'rb')
	md5_obj = hashlib.md5()
	buf = f.read()
	logger.info(u"文件buf大小[%s]" % (len(buf),))
	md5_obj.update(buf)
	hash_code = md5_obj.hexdigest()
	f.close()
	md5 = str(hash_code).lower()
	return md5


def __to_str(value):
	if isinstance(value, long):
		return str(value)
	if isinstance(value, int):
		return str(value)
	return value


def aCmp(a, b):
	"""
	:type a: str
	:type b: str
	:return:
	"""
	a = a.lower()
	b = b.lower()

	if a > b:
		return 1
	if a < b:
		return -1
	return 0


def createSign(param, sign_key):
	keys = list(param.keys())
	keys.sort()  # 排序
	sign_str = ""
	for key in keys:
		if key == "sign":
			continue
		value = param.get(key)
		sign_str = "%s&%s=%s" % (sign_str, key, value)

	sign_str = "%s&key=%s" % (sign_str, sign_key)  # 增加key参数
	sign_str = sign_str[1:]  # 去掉第一个&
	my_sign = hashlib.md5(sign_str.encode("utf-8")).hexdigest()
	# logger.info(u"待签名字符串[%s]，生成的签名为[%s]" % (sign_str, my_sign))
	return my_sign


def createSignNoEmpty(param, sign_key):
	keys = param.keys()
	keys.sort(cmp=aCmp)  # 排序
	sign_str = u""
	for key in keys:
		if key == "sign":
			continue
		value = param.get(key)
		if isinstance(value, (str, unicode)) and value == "":
			continue
		sign_str = u"%s&%s=%s" % (sign_str, key, value)

	sign_str = u"%s&key=%s" % (sign_str, sign_key)  # 增加key参数
	sign_str = sign_str[1:]  # 去掉第一个&
	my_sign = hashlib.md5(sign_str.encode("utf-8")).hexdigest()
	# my_sign = md5(sign_str).hexdigest()
	logger.info(u"待签名字符串[%s]，生成的签名为[%s]" % (sign_str, my_sign))
	return my_sign


def format_str(ves):
	'''
	格式化IP: 02.03.10
	'''
	res = []
	s = ves.split(".")
	for i in s:
		if not i.isdigit():  # 非数字为错误
			j = '00'
		elif int(i) < 10:
			j = '%02d' % int(i)
		else:
			j = i
		res.append(j)
	if len(res) < 3:
		res.extend(['00', '00', '00'])
	return ".".join(res[:3])


def cmpVersionStr(v1, v2):
	"""
	比较版本号
	@param v1:
	@param v2:
	@return:
	"""
	v1 = format_str(v1)
	v2 = format_str(v2)
	if (v1 >= v2):
		return True
	return False


from math import radians, atan, tan, acos, cos, sin


def computeDistance(Lat_A, Lng_A, Lat_B, Lng_B):
	""" 计算2点之间的距离
	极半径长度：6,356.8千米
	赤道半径长度：6,378.2千米
	:param Lat_A:
	:param Lng_A:
	:param Lat_B:
	:param Lng_B:
	:return: 返回两点之间的距离（米）
	"""
	ra = 6378.140 * 1000  # 赤道半径 （单位：米）
	rb = 6356.755 * 1000  # 极半径 （单位：米）
	flatten = (ra - rb) / ra  # 地球偏率
	rad_lat_A = radians(Lat_A)
	rad_lng_A = radians(Lng_A)
	rad_lat_B = radians(Lat_B)
	rad_lng_B = radians(Lng_B)
	pA = atan(rb / ra * tan(rad_lat_A))
	pB = atan(rb / ra * tan(rad_lat_B))
	xx = acos(sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(rad_lng_A - rad_lng_B))
	c1 = (sin(xx) - xx) * (sin(pA) + sin(pB)) ** 2 / cos(xx / 2) ** 2
	c2 = (sin(xx) + xx) * (sin(pA) - sin(pB)) ** 2 / sin(xx / 2) ** 2
	dr = flatten / 8 * (c1 - c2)
	distance = ra * (xx + dr)
	return distance


def get_ip():
	"""
	随机一个ip地址
	:return:
	"""
	A = random.randint(10, 256)
	B = random.randint(10, 256)
	C = random.randint(10, 256)
	D = random.randint(10, 256)
	ip = "%d.%d.%d.%d" % (A, B, C, D)
	return ip


# for i in range(1000):
# 	logger.info(u"%s" % (createRandomName(),))

def calEightNum():
	array_list = random.sample(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 8)
	num_str = "".join(array_list)
	num = int(num_str)
	if num < 10000000:
		num *= 10
	return num
