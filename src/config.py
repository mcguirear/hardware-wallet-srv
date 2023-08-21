#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
配置文件
"""

import copy
import os

from error_info_config import ErrInfo, ErrKey

# 钱包App签名Key
WALLET_APP_KEY = "1b865943c6b7105668af2b4ba7b39c11c"

CURRENT_DIR = os.path.dirname(__file__)

# 上传存储目录
UPLOAD_STORAGE_DIR = os.path.join(os.path.dirname(CURRENT_DIR), "upload_storage")

# infura.io的ETH节点接口地址
ETH_ENDPOINT = "https://mainnet.infura.io/v3/cc84a030722d490cb68bc88b946b13d1"
# etherscan.io的APIKey
G_ETHER_SCAN_APIKEY = "86GY7F3C8ZPK2EESTRIKI4G4SJCK4XF6U3"
# accounts.blockcypher.com的APIKey
G_BLOCKCYPHER_API_KEY = "9fdb6990bf2e412c8cd825ac559345e0"

DB_CONFIG_LIST = {
	"CACHE_REDIS": {
		'host': '127.0.0.1',
		'port': 6379,
		'passwd': '',
		'db': 0,
	},
}


def getErrInfo(errName="Success", errMsg=None, data=None):
	err = ErrInfo.get(errName)
	if not err:
		err = {"c": -1, "m": "unkown err."}
	else:
		err = copy.deepcopy(err)
	if errMsg is not None:
		err["m"] = errMsg
	if data is not None:
		err["data"] = data
	return err
