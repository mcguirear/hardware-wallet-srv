# -*- coding: utf-8 -*-
import json
from decimal import Decimal

import config
from app.wallet.services import blockchain_info_service
from common.vo.base_vo import BaseVO
from error_info_config import ErrKey
from db.db_redis import getRedis

CCY_BTC = "BTC"
CCY_ETH = "ETH"
CCY_LIST = (CCY_BTC, CCY_ETH)


def getPrice(ccy):
	"""
	获取价格
	:param ccy: 币种，多个可以用','分隔
	:return:
	"""
	ccy_str = str(ccy).upper()
	if not ccy_str:
		return config.getErrInfo(ErrKey.OK, data=[])
	
	ccy_array = ccy_str.split(",")
	aKey = "wallet_exchange_price"
	r = getRedis()
	cache_data = r.get(aKey)
	if cache_data:
		cache_data_dict = json.loads(cache_data)
	else:
		resp = blockchain_info_service.get_exchange_tickers()
		cache_data_dict = dict()
		for item in resp:
			symbol = item.get("symbol")
			price = item.get("last_trade_price")
			cache_data_dict[symbol] = price
		cache_data = json.dumps(cache_data_dict)
		r.setex(aKey, 10, cache_data)
	
	resp_data = dict()
	for ccy in ccy_array:
		symbol = f"{ccy}-USD"
		price = cache_data_dict.get(symbol, 0)
		resp_data[ccy] = price
	
	return config.getErrInfo(ErrKey.OK, data=resp_data)


def getCcyPrice(ccy):
	resp = getPrice(ccy)
	price = 0
	if resp.get("c", -1) == 0:
		price = resp.get("data").get(ccy, 0)
	return Decimal(price)


class TransactionLog(BaseVO):
	
	def __init__(self):
		self.tx_id = ""
		self.from_address = ""
		self.to_address = ""
		self.value = 0
		self.fee = 0
		self.ccy = ""
		self.timestamp = 0
		self.trans_type = 0  # 1=转出，2=转入
		self.block_number = 0
		self.detail_url = ""


class Web3BaseService(object):
	
	def __init__(self):
		pass
	
	def getBalance(self, address):
		"""
		查询余额
		:return:
		"""
		info = {
			"balance": 0
		}
		return config.getErrInfo(ErrKey.OK, data=info)
	
	def validateAddress(self, address):
		"""
		验证地址
		:param address:
		:return:
		"""
		info = {
			"valid": True,
			"address": address
		}
		return config.getErrInfo(ErrKey.OK, data=info)
	
	def sendRawTransaction(self, rawData):
		"""
		发送交易
		:param rawData:
		:return:
		"""
		info = {
			"txid": ""
		}
		return config.getErrInfo(ErrKey.OK, data=info)
	
	def estimateFee(self, from_address, to_address):
		"""
		查询币种默认矿工费
		:param from_address: 转出地址
		:param to_address: 转入地址
		:return:
		"""
		info = {
			"fee": "",
			"gasPrice": "",
			"nonce": "",
		}
		return config.getErrInfo(ErrKey.OK, data=info)
	
	def getTransactions(self, page, number, address):
		"""
		查询交易记录
		"""
		info = [
		
		]
		return config.getErrInfo(ErrKey.OK, data=info)
	
	def getTransactionDetail(self, txId, address):
		"""
		查询交易详情
		:param txId:
		:param address: 查询用户的钱包地址，用于判断是转入还是转出
		:return:
		"""
		info = {
		
		}
		return config.getErrInfo(ErrKey.OK, data=info)
	
	def getUTXOs(self, address, value):
		"""
		BTC获取UTXO列表
		:param address:
		:param value:
		:return:
		"""
		return config.getErrInfo(ErrKey.OK, data=[])
