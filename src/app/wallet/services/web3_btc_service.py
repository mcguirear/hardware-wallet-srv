# -*- coding: utf-8 -*-
import json
import blockcypher
from decimal import Decimal
import config
from error_info_config import ErrKey

from app.wallet.services import blockchain_info_service, bit_coin_tool
from app.wallet.services.web3_base_service import Web3BaseService, TransactionLog, CCY_BTC, getCcyPrice

from common.json_util import XJsonEncoder
from xlib import xlog, xnumber

logger = xlog.getLogger()

coin_symbol = "btc"
coin_unit = 100000000


def toTransactionLog(resp, address):
	tx_id = resp.get("hash")
	input_list = resp.get("inputs")
	out_list = resp.get("out")
	fee = resp.get("fee")
	timestamp = resp.get("time")
	block_index = resp.get("block_index")
	
	sender_set = set()
	for item in input_list:
		prev_out = item.get("prev_out")
		addr = prev_out.get("addr")
		sender_set.add(addr)
	
	if address in sender_set:  # 自己的地址在发出的地址中，表示转出
		trans_type = 1  # 1=转出
	else:
		trans_type = 2  # 2=转入
	
	from_address_list = set()
	to_address_list = set()
	total_value = 0
	if trans_type == 1:  # 转出
		for item in out_list:
			addr = item.get("addr")
			value = item.get("value")
			if addr != address:
				total_value = total_value + value
				to_address_list.add(addr)
	else:  # 转入
		# out的中地址为自己的才是转入数量
		for item in out_list:
			addr = item.get("addr")
			value = item.get("value")
			if addr == address:
				total_value = total_value + value
		# inputs中的为转出的地址
		for item in input_list:
			prev_out = item.get("prev_out")
			addr = prev_out.get("addr")
			from_address_list.add(addr)
	
	value = Decimal(Decimal(total_value) / Decimal(coin_unit))
	fee = Decimal(Decimal(fee) / Decimal(coin_unit))
	from_address_list = list(from_address_list)
	to_address_list = list(to_address_list)
	from_address_str = ",".join(from_address_list)
	to_address_str = ",".join(to_address_list)
	log = TransactionLog()
	log.tx_id = resp.get("hash")
	log.value = value
	log.fee = fee
	log.ccy = CCY_BTC
	log.timestamp = timestamp
	log.trans_type = trans_type  # 1=转出，2=转入
	if trans_type == 2:  # 转入
		log.from_address = from_address_list[0] if from_address_list else ""
		log.to_address = address
	else:  # 转出
		log.from_address = address
		log.to_address = to_address_list[0] if to_address_list else ""
	
	log.block_number = block_index
	log.detail_url = "https://blockchair.com/bitcoin/transaction/%s" % (tx_id,)
	return log


class Web3BTCBaseService(Web3BaseService):
	
	def __init__(self):
		super().__init__()
	
	def getBalance(self, address):
		# resp = blockcypher.get_address_overview(address, coin_symbol, config.G_BLOCKCYPHER_API_KEY)
		balance = blockchain_info_service.get_balance(address)
		price = getCcyPrice(CCY_BTC)
		balance_usd = xnumber.round_half_down_dec(balance * price, 2)
		info = {
			"ccy": CCY_BTC,
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
		valid = bit_coin_tool.is_address(address)
		info = {
			"valid": valid,
			"address": address
		}
		return config.getErrInfo(ErrKey.OK, data=info)
	
	def getUTXOs(self, address, value):
		"""
		查询 未被消费 的转账记录
		:param address: 转出地址
		:param value: 要转出币的数量
		:return:
		"""
		if value < 0:
			return config.getErrInfo(ErrKey, "value error")
		
		limit_value = int(value * coin_unit)
		confirmed_balance = blockcypher.get_confirmed_balance(address)
		logger.info(f"查询[{address}]余额：{confirmed_balance}]")
		if limit_value > confirmed_balance:
			return config.getErrInfo(ErrKey.ParamErr, "Insufficient Balance")
		
		before_bh = None
		after_bh = None
		resp = blockcypher.get_address_details(address, coin_symbol='btc', txn_limit=1000, api_key=config.G_BLOCKCYPHER_API_KEY, before_bh=before_bh, after_bh=after_bh, unspent_only=True, confirmations=6, include_script=True)
		txrefs = resp.get("txrefs", [])
		txrefs.sort(key=lambda u: u["block_height"], reverse=False)
		
		# logger.info("查询[%s]未被消费的转账记录: %s" % (address, json.dumps(resp, indent=2, cls=XJsonEncoder),))
		logger.info("查询[%s]未被消费的转账记录数量: %s" % (address, len(txrefs),))
		utxo_list = []
		utxo_total_value = 0
		for item in txrefs:
			tx_hash = item.get("tx_hash")
			block_height = item.get("block_height")
			vout = item.get("tx_output_n")
			amount = item.get("value")
			script = item.get("script")
			utxo_total_value += amount
			logger.info(f"合并交易块[{item}]的数量[{amount}]= 总数量[{utxo_total_value}]")
			info = {
				"txHash": tx_hash,
				"vout": vout,
				"amount": amount,
				"address": address,
				"scriptPubKey": script,
				"blockHeight": block_height,
			}
			utxo_list.append(info)
			if utxo_total_value >= limit_value:
				break
		logger.info(f"[BTC]从[{address}]转出[{value}->[{limit_value}]合并[{len(utxo_list)}]未被消费的交易块后总数量[{utxo_total_value}]]")
		resp_data = {
			"confirmed_balance": confirmed_balance,
			"utxo_list": utxo_list,
			"utxo_total_value": utxo_total_value,
		}
		if utxo_total_value < limit_value:
			return config.getErrInfo(ErrKey.ParamErr, "Some Block in Confirming,Insufficient Balance", data=resp_data)
		return config.getErrInfo(ErrKey.OK, data=resp_data)
	
	def sendRawTransaction(self, rawData):
		"""
		发送交易
		返回数据样例
		{'error': 'Error validating transaction: insufficient priority and fee for relay.'}
		
		result = {
			'tx': {
				'block_height': -1,
				'block_index': -1,
				'hash': '5f2447236de480e6ec2b45e95a56a147561b0365eca95da104ccd8e9bffdcf19',
				'addresses': ['1GzYfLfE5dTVWFk4i4cCAxE4nUyVLcwc2M', '3CMizhsxEVYvgYwFf9RG52vyx89XHG3Jsa'],
				'total': 370000, 'fees': 26856,
				'size': 189,
				'vsize': 189,
				'preference': 'high',
				'relayed_by': '218.255.3.60',
				'received': '2023-04-12T06:12:33.752406961Z',
				'ver': 1,
				'double_spend': False,
				'vin_sz': 1,
				'vout_sz': 1,
				'confirmations': 0,
				'inputs': [
					{
						'prev_hash': 'b2fb03b29174a39a6a71b94b1c8abfc01bc9a22f5c37bfbfb8c12e9b42faa609',
						'output_index': 0,
						'script': '4730440220266683da3b5ea04ac5804f316741e7c5cc681e7f06e7954a914c23048ff569c302203c5bbb354252d3aee04f686685cba59f6af08ca69198e25473e209f953dd3b690121038b8a97bb6827a178d21d3f5126023de08de8f88f7a3b1a0b5412f3b88df65f79',
						'output_value': 396856,
						'sequence': 4294967295,
						'addresses': ['1GzYfLfE5dTVWFk4i4cCAxE4nUyVLcwc2M'],
						'script_type': 'pay-to-pubkey-hash',
						'age': 784306
					}
				],
				'outputs': [
					{
						'value': 370000,
						'script': 'a9147503596fbe8ebba0d9acb987221090c78d929b8b87',
						'addresses': ['3CMizhsxEVYvgYwFf9RG52vyx89XHG3Jsa'],
						'script_type': 'pay-to-script-hash'
					}
				]
			}
		}
		:param rawData:
		:return:
		"""
		resp = blockcypher.pushtx(rawData, "btc", api_key=config.G_BLOCKCYPHER_API_KEY)
		logger.info("[BTC]发送交易[%s],结果:%s" % (rawData, resp))
		if resp.get("tx"):
			tx_id = resp.get("tx").get("hash")
			info = {
				"tx_id": tx_id,
			}
			return config.getErrInfo(ErrKey.OK, data=info)
		
		error = resp.get("error")
		return config.getErrInfo(ErrKey.ParamErr, errMsg=error)
	
	def estimateFee(self, from_address, to_address):
		"""
		查询币种默认矿工费
		:param from_address: 转出地址
		:param to_address: 转入地址
		:return:
		"""
		resp = blockcypher.get_blockchain_fee_estimates("btc", api_key=config.G_BLOCKCYPHER_API_KEY)
		# logger.info("预估矿工费[%s]" % (resp,))
		high = resp.get("high_fee_per_kb")
		medium = resp.get("medium_fee_per_kb")
		low = resp.get("low_fee_per_kb")
		
		info = {
			"high": high,
			"medium": medium,
			"low": low,
		}
		return config.getErrInfo(ErrKey.OK, data=info)
	
	def getTransactions(self, page, number, address):
		"""
		查询交易记录
		"""
		resp = blockchain_info_service.get_transfer_list(address, page, number)
		log_list = []
		for item in resp:
			log = toTransactionLog(item, address)
			log_list.append(log.to_dict())
		return config.getErrInfo(ErrKey.OK, data=log_list)
	
	def getTransactionDetail(self, txId, address):
		"""
		查询交易详情
		:param txId:
		:param address: 查询用户的钱包地址，用于判断是转入还是转出
		:return:
		"""
		resp = blockchain_info_service.get_transfer_detail(txId)
		log = toTransactionLog(resp, address)
		info = log.to_dict()
		return config.getErrInfo(ErrKey.OK, data=info)
