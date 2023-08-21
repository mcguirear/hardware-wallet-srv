#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
应用配置
"""
import os

# 系统名称
SYSTEM_NAME = "wallet"

# 版本号
VERSION = "1.0.0"

# 默认监听端口
LISTEN_PORT = 7970

# DEBUG开关设置
DEBUG = True

# 服务器外网地址
HOST_IP = "127.0.0.1"

# 当前路径
APP_DIR = os.path.dirname(__file__).replace("\\", "/")

# 开发模式
DEV_MODE_FLAG = False

# 跨域的域名
ACCESS_CONTROL_ALLOW_ORIGIN = "*"


CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))