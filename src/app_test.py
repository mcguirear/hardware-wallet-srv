#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ---  标准库  ---
import json
import sys
import logging
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

from xlib import xparser
from xlib import xlog
from db import db_redis

from sqlalchemy.engine import Result


SYSTEM_NAME = "test"
VERSION = "1.0.0"
LISTEN_PORT = "9090"

db_redis.initRedis()


def readFile(filename):
    f = open(filename, 'r', encoding='utf-8')
    content = f.read()
    f.close()
    return content



if __name__ == '__main__':
    # 获取命令行参数
    options = xparser.get(version="%s v%s" % (SYSTEM_NAME, VERSION), port=LISTEN_PORT)
    # 初始日志
    xlog.initLogger("../logs/%s/" % (SYSTEM_NAME,), "%s.log" % (SYSTEM_NAME,), True)
    logger = xlog.getLogger()
    logger.info("初始日志配置完成")
    logger.setLevel(logging.DEBUG)


    pass
