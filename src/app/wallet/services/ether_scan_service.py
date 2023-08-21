# -*- coding: utf-8 -*-
"""
etherscan.io的文档地址
https://docs.etherscan.io/
"""

import requests
import json

import config
from xlib import xlog

logger = xlog.getLogger()


def submit_request(module, action, params):
	payload = {
		"module": module,
		"action": action,
		"apikey": config.G_ETHER_SCAN_APIKEY,
	}
	payload.update(params)
	logger.info(f"[etherscan]请求参数:f{payload}")
	ulr = "https://api.etherscan.io/api"
	r = requests.get(ulr, params=payload)
	logger.info(f"[etherscan]返回:f{r.text}")
	return r.json()


def get_transfer_list(start_block, page, offset, address):
	params = {
		"address": address,
		"startblock": start_block,
		"endblock": "9999999999",
		"page": page,
		"offset": offset,
		"sort": "desc",
	}
	# txlistinternal, txlist
	resp_data = submit_request("account", "txlist", params)
	# logger.debug(json.dumps(resp_data, ensure_ascii=False, indent=2))
	result = resp_data.get("result")
	logger.info(f"[etherscan]获取交易列表参数[f{params}],返回数量{len(result)}")
	if not isinstance(result, list):
		return []
	return result
