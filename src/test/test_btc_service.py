# -*- coding: utf-8 -*-
import json
import unittest
import logging

from app.wallet.services.web3_btc_service import Web3BTCBaseService
from app.wallet.services import blockchain_info_service, bit_coin_tool
from common.json_util import XJsonEncoder
from xlib import xlog

SYSTEM_NAME = "test"
# 初始日志
xlog.initLogger("../../logs/%s/" % (SYSTEM_NAME,), "%s.log" % (SYSTEM_NAME,), True)
logger = xlog.getLogger()
logger.info("初始日志配置完成")
logger.setLevel(logging.DEBUG)

btcService = Web3BTCBaseService()


class MyTestCase(unittest.TestCase):
	
	def setUp(self) -> None:
		pass
	
	def test_get_exchange_rates(self):
		resp = blockchain_info_service.get_exchange_tickers()
		logger.info(f"最新价格信息:{json.dumps(resp, indent=2)}")
	
	def test_is_address(self):
		a = bit_coin_tool.is_address("3LYJfcfHPXYJreMsASk2jkn69LWEYKzexb")
		logger.info(f"is_address:{a}")
	
	def test_get_balance(self):
		addr = "3LYJfcfHPXYJreMsASk2jkn69LWEYKzexb"
		btcService.getBalance(addr)
		pass
	
	def test_get_transfer_detail(self):
		# tx_hash = "7d14fb0ef201c09603e1ea72780e8ecab5b35ebdfbe9181c3acdfa186a754a88"
		# address = "3L2JpTQm1gSMYkhcXT2XLkTVaERrV9MQbz"
		# resp = btcService.getTransactionDetail(tx_hash, address)
		# logger.info("查询交易详情: %s" % (json.dumps(resp, indent=2)))
		
		tx_hash = "b2fb03b29174a39a6a71b94b1c8abfc01bc9a22f5c37bfbfb8c12e9b42faa609"
		address = "1GzYfLfE5dTVWFk4i4cCAxE4nUyVLcwc2M"
		resp = btcService.getTransactionDetail(tx_hash, address)
		logger.info("查询交易详情: %s" % (json.dumps(resp, indent=2,cls=XJsonEncoder)))
		pass
	
	def test_get_transactions(self):
		address = "3L2JpTQm1gSMYkhcXT2XLkTVaERrV9MQbz"
		resp = btcService.getTransactions(1, 20, address)
		logger.info("查询交易列表: %s" % (json.dumps(resp, indent=2)))
		pass
	
	def test_get_utxo_list(self):
		address = "1FeexV6bAHb8ybZjqQMjJrcCrHGW9sb6uF"
		btcService.getUTXOs(address, 3)
	
	def test_estimateFee(self):
		from_address = "1FeexV6bAHb8ybZjqQMjJrcCrHGW9sb6uF"
		to_address = "3L2JpTQm1gSMYkhcXT2XLkTVaERrV9MQbz"
		btcService.estimateFee(from_address, to_address)
	
	def test_c(self):
		resp = {
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
						'age': 784306}],
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
		tx_id = resp.get("tx").get("hash")
		print(tx_id)

if __name__ == '__main__':
	unittest.main()
