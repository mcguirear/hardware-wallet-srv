# -*- coding: utf-8 -*-

import unittest
import logging

import eth_utils
from hexbytes import HexBytes

from app.wallet.services import ether_scan_service
from xlib import xlog

SYSTEM_NAME = "test"
# 初始日志
xlog.initLogger("../../logs/%s/" % (SYSTEM_NAME,), "%s.log" % (SYSTEM_NAME,), True)
logger = xlog.getLogger()
logger.info("初始日志配置完成")
logger.setLevel(logging.DEBUG)


class MyTestCase(unittest.TestCase):
	
	def test_get_transfer_list(self):
		ether_scan_service.get_transfer_list(0, 1, 10, "0xCC9557F04633d82Fb6A1741dcec96986cD8689AE")
		self.assertEqual(True, True)  # add assertion here
	
	def test_address(self):
		address = "62534f9aea383dbafafe67914771a723214d5c1e"
		address = address.lower()
		if not eth_utils.is_address(address):
			print("address error")
			return
		if not eth_utils.is_checksum_address(address):
			sum_address = eth_utils.to_checksum_address(address)
			print(f" {address} -> {sum_address}")
	
	def test_HexBytes(self):
		data = HexBytes(b'\xc6\x8c\xfc+v\x92\x9ba\xd1\xaa\x16\xf3\xa2\xef\xdfl\xc0\x0f\xc8\xfc/\x00\x10\xfd\xba\x8e\x80\x8c\x99\xdd\x96\xcb')
		print(data)
		print(data.hex())
		
if __name__ == '__main__':
	unittest.main()

