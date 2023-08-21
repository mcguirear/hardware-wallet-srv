# -*- coding: utf-8 -*-
"""
定时任务
"""

# import random
# import json
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from dateutil.relativedelta import relativedelta


from xlib.BaseFunction import callLater
from xlib import xlog

logger = xlog.getLogger()


def initServerInfo():

	pass


def allInOneCronTask():
	# 每天凌晨同步前一天的数据
	now_time = datetime.now()
	now_day = datetime.strptime(now_time.strftime('%Y-%m-%d'), '%Y-%m-%d')
	yesterday = now_day + relativedelta(days=-1, minute=0, second=0, microsecond=0)
	return


def startCron(isMaster):
	if not isMaster:
		return
	initServerInfo()
	
	scheduler = BackgroundScheduler()
	callLater(2, allInOneCronTask)
	# callLater(1, investor_service.sync_rate_info)
	# # 每间隔2秒定时同步汇率信息
	# scheduler.add_job(investor_service.sync_rate_info, 'interval', seconds=4, max_instances=4)
	# 每日凌晨任务
	scheduler.add_job(allInOneCronTask, 'cron', hour=0, minute=1, second=0)
	scheduler.start()
	pass
