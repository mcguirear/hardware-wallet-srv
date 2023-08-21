# -*- coding: utf-8 -*-

import config
# import json
# from datetime import datetime
# from app.investor.app_authorize import AppSession
from app.wallet.services import blockchain_info_service, web3_base_service
from app.wallet.services.web3_base_service import CCY_ETH, CCY_BTC, CCY_LIST, Web3BaseService
from app.wallet.services.web3_eth_service import Web3ETHBaseService
from app.wallet.services.web3_btc_service import Web3BTCBaseService

from db.db_redis import getRedis
from error_info_config import ErrKey

from xlib import xlog

logger = xlog.getLogger()

ServiceDict = {
	CCY_ETH: Web3ETHBaseService(),
	CCY_BTC: Web3BTCBaseService()
}


def getService(ccy):
	"""
	:param ccy:
	:rtype: Web3BaseService
	"""
	return ServiceDict.get(ccy)


def getPrice(arguments, **kwargs):
	"""
	获取价格
	:param arguments:
	:param kwargs:
	:return:
	"""
	try:
		ccy = str(arguments.get("ccy", "")).upper()
		return web3_base_service.getPrice(ccy)
	except Exception as ex:
		logger.exception("")
		return config.getErrInfo(ErrKey.SystemErr, str(ex))


def getBalance(arguments, **kwargs):
	"""
	查询余额
	:return:
	"""
	ccy = str(arguments.get("ccy", "")).upper()
	address = arguments.get("address")
	if ccy not in CCY_LIST:
		return config.getErrInfo(ErrKey.ParamErr, "ccy error")
	if not address:
		return config.getErrInfo(ErrKey.ParamErr, "address error")
	try:
		service = getService(ccy)
		return service.getBalance(address)
	except Exception as ex:
		logger.exception("")
		return config.getErrInfo(ErrKey.SystemErr, str(ex))


def validateAddress(arguments, **kwargs):
	"""
	验证地址
	:return:
	"""
	ccy = str(arguments.get("ccy", "")).upper()
	address = arguments.get("address")
	if ccy not in CCY_LIST:
		return config.getErrInfo(ErrKey.ParamErr, "ccy error")
	if not address:
		return config.getErrInfo(ErrKey.ParamErr, "address error")
	try:
		service = getService(ccy)
		return service.validateAddress(address)
	except Exception as ex:
		logger.exception("")
		return config.getErrInfo(ErrKey.SystemErr, str(ex))


def sendRawTransaction(arguments, **kwargs):
	"""
	发送交易
	:return:
	"""
	ccy = str(arguments.get("ccy", "")).upper()
	rawData = arguments.get("rawData")
	if ccy not in CCY_LIST:
		return config.getErrInfo(ErrKey.ParamErr, "ccy error")
	if not rawData:
		return config.getErrInfo(ErrKey.ParamErr, "rawData error")
	try:
		service = getService(ccy)
		return service.sendRawTransaction(rawData)
	except Exception as ex:
		logger.exception("")
		return config.getErrInfo(ErrKey.SystemErr, str(ex))


def estimateFee(arguments, **kwargs):
	"""
	查询币种默认矿工费
	:return:
	"""
	ccy = str(arguments.get("ccy", "")).upper()
	from_address = arguments.get("from_address")
	to_address = arguments.get("to_address")
	if ccy not in CCY_LIST:
		return config.getErrInfo(ErrKey.ParamErr, "ccy error")
	if not from_address:
		return config.getErrInfo(ErrKey.ParamErr, "from_address error")
	try:
		service = getService(ccy)
		return service.estimateFee(from_address, to_address)
	except Exception as ex:
		logger.exception("")
		return config.getErrInfo(ErrKey.SystemErr, str(ex))


def getTransactions(arguments, **kwargs):
	"""
	查询交易记录
	:return:
	"""
	ccy = str(arguments.get("ccy", "")).upper()
	page = arguments.get("page", 1)
	number = arguments.get("number")
	address = arguments.get("address")
	if ccy not in CCY_LIST:
		return config.getErrInfo(ErrKey.ParamErr, "ccy error")
	page = int(page)
	if page <= 0:
		return config.getErrInfo(ErrKey.ParamErr, "page error")
	if not number:
		return config.getErrInfo(ErrKey.ParamErr, "number error")
	number = int(number)
	if not address:
		return config.getErrInfo(ErrKey.ParamErr, "address error")
	try:
		service = getService(ccy)
		return service.getTransactions(page, number, address)
	except Exception as ex:
		logger.exception("")
		return config.getErrInfo(ErrKey.SystemErr, str(ex))


def getTransactionDetail(arguments, **kwargs):
	"""
	查询交易记录详情
	:return:
	"""
	ccy = str(arguments.get("ccy", "")).upper()
	txId = arguments.get("txId")
	address = arguments.get("address", "")
	if ccy not in CCY_LIST:
		return config.getErrInfo(ErrKey.ParamErr, "ccy error")
	if not txId:
		return config.getErrInfo(ErrKey.ParamErr, "txId error")
	try:
		service = getService(ccy)
		return service.getTransactionDetail(txId, address)
	except Exception as ex:
		logger.exception("")
		return config.getErrInfo(ErrKey.SystemErr, str(ex))


def getUTXOs(arguments, **kwargs):
	"""
	BTC获取UTXO列表
	:return:
	"""
	ccy = str(arguments.get("ccy", "")).upper()
	address = arguments.get("address", "")
	value = arguments.get("value")
	if ccy not in CCY_LIST:
		return config.getErrInfo(ErrKey.ParamErr, "ccy error")
	if not address:
		return config.getErrInfo(ErrKey.ParamErr, "address error")
	try:
		value = float(value)
		service = getService(ccy)
		return service.getUTXOs(address, value)
	except Exception as ex:
		logger.exception("")
		return config.getErrInfo(ErrKey.SystemErr, str(ex))
