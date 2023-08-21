# -*- coding:utf-8 -*-

from optparse import OptionParser


def get(version, port=None, logfile='./logs/run%s.log', backupCount=30, master=False, debug=False, web=False):
	"""
	@summary: 获取启动参数
	@param {string} version: 查看版本号时的返回值
	@param {int} port: 默认的端口号
	@param {string} logfile: 默认的日志文件路径及文件名
	@param {int} backupCount: 默认的日志文件保留天数
	@param {bool} master: 是否主进程
	@param {bool} debug: 是否调试模式
	@param {bool} web: 是否是查询话单和收支明细
	@return {object}:
		# 如果启动命令行没有传这些参数则返回默认值
		options.port: 启动时设置的端口号
		options.logfile: 启动时设置的日志文件路径和文件名
		options.backupCount: 启动时设置的日志文件保留天数de
		options.master: 启动时设置的这进程是否主进程
		options.debug: 启动时设置的是否调试模式
		options.web: 启动时用户查询话单和收支明细
	"""
	parser = OptionParser(usage="usage: python %prog [options] filename", version=version)
	parser.add_option("-p", "--port", action="store", type="int", dest="port", default=port, help="Listen Port")
	parser.add_option("-f", "--logfile", action="store", type="string", dest="logfile", default=logfile, help="LogFile Path and Name. default=./logs/run_%s.log" % (port))
	parser.add_option("-n", "--backupCount", action="store", type="int", dest="backupCount", default=backupCount, help="LogFile BackUp Number")
	parser.add_option("-m", "--master", action="store_true", dest="master", default=master, help="master process")

	# 是否为debug模式
	parser.add_option("-d", "--debug", action="store_true", dest="debug", default=debug, help="debug mode")
	# 项目名称
	parser.add_option("-P", "--project", action="store", type="string", dest="project", default="PlatformName", help="platform name")
	# 游戏名称
	parser.add_option("-g", "--gamename", action="store", type="string", dest="gamename", default="LandLord", help="predefine game name")
	# 房间ID
	parser.add_option("-r", "--roomId", action="store", type="int", dest="room_id", default=1, help="predefine game room id")

	options = parser.parse_args()[0]

	# 日志文件名加上端口号
	if '%s' in options.logfile:
		if options.port is not None:
			options.logfile = options.logfile % ("_" + str(options.port))
		else:
			options.logfile = options.logfile % ("")

	return options
