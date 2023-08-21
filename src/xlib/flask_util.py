#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

import flask


def is_ip(ip):
	u"""
	@summary: 检查ip地址是否正确
	@param {string} ip: 要检查的ip地址
	@return {boolean}:  如果输入的是正确的ip地址则返回 True, 否则返回 False
	"""
	if not ip or not isinstance(ip, str):
		return False
	return len([i for i in ip.split('.') if i.isdigit() and (0 <= int(i) <= 255) and (not i.startswith('0') or len(i) == 1)]) == 4


def is_local_ip(ip):
	u"""
	@summary: 检查ip地址是否局域网地址
	@param {string} ip: 要检查的ip地址
	@return {bool}:  如果输入的是局域网内的ip地址则返回 True, 否则返回 False (IP格式错误返回 False)
	"""
	if not is_ip(ip):
		return False
	# 127 开头,本机或者同一IP段
	if ip.startswith('127.'):
		return True
	# 局域网ip: 10.0.0.0-10.255.255.255 / 192.168.0.0-192.168.255.255
	if ip.startswith('10.') or ip.startswith('192.168.'):
		return True
	# 局域网ip: 172.16.0.0-172.31.255.255
	if ip.startswith('172.') and (16 <= int(ip.split('.')[1]) <= 31):
		return True
	# 除上述之外都是外网地址
	return False


def get_real_ip(request):
	"""
	获取接收的请求过来的ip地址
	:param request: flask的request
	:return 发请求过来的IP地址
	:type request: flask.request
	:rtype :str
	"""

	headers = request.headers
	client_ip = ''
	ipList = headers.get("X-Forwarded-For", "")
	# 可能有代理, 没有“.”的肯定不是IPv4格式
	if ipList and '.' in ipList:
		if is_ip(ipList) and not is_local_ip(ipList):
			client_ip = ipList
		# 包含多个ip地址
		elif "," in ipList:
			ipList = ipList.strip().replace(' ', '').split(",")
			for ip in ipList:
				if is_ip(ip) and not is_local_ip(ip):
					client_ip = ip
					break
	if not client_ip:
		client_ip = headers.get("X-Real-Ip", "")
	if not client_ip:
		client_ip = headers.get("Remote-Addr", "")
		if "," in client_ip:
			ipList = client_ip.strip().replace(' ', '').split(",")
			client_ip = ''  # 先清空 client_ip, 避免里面的值都不对
			for ip in ipList:
				if is_ip(ip) and not is_local_ip(ip):
					client_ip = ip
					break
	if not client_ip:
		client_ip = request.remote_addr
		if "," in client_ip:
			ipList = client_ip.strip().replace(' ', '').split(",")
			client_ip = ipList[0]  # 先赋值一个,避免完全获取不到的情况(无奈之举,这时还获取不到就没法获取了)
			for ip in ipList:
				if is_ip(ip) and not is_local_ip(ip):
					client_ip = ip
					break
	return client_ip
