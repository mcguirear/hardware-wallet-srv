# -*- coding: utf-8 -*-
"""
infura的ETH节点接口文档：
https://docs.infura.io/infura/

"""

from decimal import Decimal

import eth_utils
import web3.main
from hexbytes import HexBytes
from web3 import Web3, HTTPProvider
from web3.datastructures import AttributeDict
from web3.main import is_address, is_checksum_address, to_checksum_address, from_wei, to_wei, to_hex

import config
from app.wallet.services import ether_scan_service
from app.wallet.services.web3_base_service import Web3BaseService, CCY_ETH, TransactionLog, getCcyPrice
from common.vo.base_vo import obj_to_dict
import blockcypher
from error_info_config import ErrKey
from xlib import xlog, xnumber

logger = xlog.getLogger()


def calcFee(gas, gasPrice):
	return from_wei(gas * gasPrice, 'ether')


class Web3ETHBaseService(Web3BaseService):
	
	def __init__(self):
		super().__init__()
	
	def getBalance(self, address):
		address = address.lower()
		if not is_address(address):
			return config.getErrInfo(ErrKey.ParamErr, "to_address invalid")
		if not is_checksum_address(address):
			address = to_checksum_address(address)
		
		connection = Web3(HTTPProvider(config.ETH_ENDPOINT))
		balance = connection.eth.get_balance(address)
		balance = from_wei(balance, 'ether')
		logger.info(f"余额:{balance}, {type(balance)}")
		price = getCcyPrice(CCY_ETH)
		balance_usd = xnumber.round_half_down_dec(balance * price, 2)
		info = {
			"ccy": CCY_ETH,
			"balance": balance,
			"balance_usd": balance_usd,
			"price": price,
		}
		return config.getErrInfo(ErrKey.OK, data=info)
	
	def validateAddress(self, address):
		"""
		验证地址
		:param address:
		:return:
		"""
		isvalid = is_address(address)
		if isvalid:
			address = eth_utils.to_checksum_address(address)
		info = {
			"valid": isvalid,
			"address": address
		}
		return config.getErrInfo(ErrKey.OK, data=info)
	
	def sendRawTransaction(self, rawData):
		"""
		发送交易
		:param rawData:
		:return:
		"""
		connection = Web3(HTTPProvider(config.ETH_ENDPOINT))
		ret_data = connection.eth.send_raw_transaction(rawData)
		logger.info("[ETH]发送交易[%s],结果:%s" % (rawData, ret_data))
		tx_id = ret_data.hex()
		info = {
			"tx_id": tx_id
		}
		return config.getErrInfo(ErrKey.OK, data=info)
	
	def estimateFee(self, from_address, to_address):
		"""
		查询eth得到gasPrice和nonce
		:param from_address: 必须，转出地址
		:param to_address: 可选，转入地址
		:return:
		"""
		from_address = from_address.lower()
		if not is_address(from_address):
			return config.getErrInfo(ErrKey.ParamErr, "from_address invalid")
		if to_address:
			to_address = to_address.lower()
			if not is_address(to_address):
				return config.getErrInfo(ErrKey.ParamErr, "to_address invalid")
			if not is_checksum_address(to_address):
				to_address = to_checksum_address(to_address)
		
		if not is_checksum_address(from_address):
			from_address = to_checksum_address(from_address)
		connection = Web3(HTTPProvider(config.ETH_ENDPOINT))
		# gas_price = connection.eth.gas_price
		# max_priority_fee = connection.eth.max_priority_fee
		nonce = connection.eth.get_transaction_count(from_address)
		trans = {
			'from': from_address
		}
		if to_address: trans['to'] = to_address
		# if value: trans['value'] = to_wei(value, "ether")
		gas = connection.eth.estimate_gas(trans)
		logger.info("估算交易[%s]需要的Gas[%s]" % (trans, gas))
		
		resp = blockcypher.get_blockchain_fee_estimates("eth", api_key=config.G_BLOCKCYPHER_API_KEY)
		high = resp.get("high_fee_per_kb")
		medium = resp.get("medium_fee_per_kb")
		low = resp.get("low_fee_per_kb")
		
		info = {
			"nonce": nonce,
			"gas": gas,
			"high": high,
			"medium": medium,
			"low": low,
		}
		return config.getErrInfo(ErrKey.OK, data=info)
	
	def getTransactions(self, page, number, address):
		"""
		查询交易记录
		:param page:
		:param number:
		:param address:
		:return:
		"""
		low_address = address.lower()
		regular_address = low_address
		if not is_address(low_address):
			return config.getErrInfo(ErrKey.ParamErr, "address error")
		if not is_checksum_address(low_address):
			regular_address = to_checksum_address(low_address)
		
		result = ether_scan_service.get_transfer_list(0, page, number, regular_address)
		log_list = []
		for item in result:
			tx_id = item.get("hash")
			gas = int(item.get("gas"))
			gasPrice = int(item.get("gasPrice"))
			fee = calcFee(gas, gasPrice)
			value = from_wei(int(item.get("value")), "ether")
			timestamp = int(item.get("timeStamp"))
			
			from_address = item.get("from")
			from_address = from_address.lower()
			log = TransactionLog()
			log.tx_id = tx_id
			log.from_address = from_address
			log.to_address = item.get("to")
			log.value = value
			log.fee = fee
			log.ccy = CCY_ETH
			log.timestamp = timestamp
			log.block_number = item.get("blockNumber")
			log.trans_type = 1 if from_address == low_address else 2
			log.detail_url = "https://etherscan.io/tx/%s" % (tx_id,)
			log_list.append(log.to_dict())
		
		return config.getErrInfo(ErrKey.OK, data=log_list)
	
	def getTransactionDetail(self, txId, address):
		"""
		查询交易详情
		:param txId:
		:param address: 查询用户的钱包地址，用于判断是转入还是转出
		:return:
		"""
		low_address = address.lower()
		if not is_address(low_address):
			return config.getErrInfo(ErrKey.ParamErr, "address error")
		
		connection = Web3(HTTPProvider(config.ETH_ENDPOINT))
		resp = connection.eth.get_transaction(txId)  # type: AttributeDict
		logger.info(f"[{CCY_ETH}]查询[{txId}]交易详情: {resp}")
		txId = resp.get("hash").hex()
		from_address = str(resp.get("from"))
		from_address = from_address.lower()
		to_address = str(resp.get("to"))
		blockNumber = resp.get("blockNumber")
		# blockHash = resp.get("blockHash")
		gas = resp.get("gas")
		gasPrice = resp.get("gasPrice")
		fee = calcFee(gas, gasPrice)
		value = resp.get("value")
		value = from_wei(value, 'ether')
		
		blockInfo = connection.eth.get_block(blockNumber, False)
		# logger.info(f"[{CCY_ETH}]查询[{blockNumber}]块详情: {blockInfo}")
		timestamp = blockInfo.get("timestamp")  # 时间戳
		receiptInfo = connection.eth.get_transaction_receipt(txId)
		# logger.info(f"[{CCY_ETH}]查询[{txId}] receipt 详情: {receiptInfo}")
		
		log = TransactionLog()
		log.tx_id = txId
		log.from_address = address
		log.to_address = to_address
		log.value = value
		log.fee = fee
		log.ccy = CCY_ETH
		log.timestamp = timestamp
		log.block_number = blockNumber
		log.trans_type = 1 if from_address == low_address else 2
		log.detail_url = "https://etherscan.io/tx/%s" % (txId,)
		
		info = log.to_dict()
		return config.getErrInfo(ErrKey.OK, data=info)
