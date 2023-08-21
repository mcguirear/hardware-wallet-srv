# -*- coding: utf-8 -*-
"""
blockchain.com的文档地址
https://www.blockchain.com/explorer/api
"""

import requests
import json
from decimal import Decimal

import config
from error_info_config import ErrKey
from xlib import xlog

logger = xlog.getLogger()


def submit_request(method, path, params):
	url = "https://blockchain.info%s" % (path,)
	# url = "https://testnet.blockchain.info%s" % (path,)
	logger.info(f"[blockchain]请求[{url}]参数:{params}")
	method = method.upper()
	if method == "GET":
		r = requests.get(url, params=params)
	else:
		r = requests.post(url, params=params)
	resp = r.json()
	logger.info("[blockchain]返回:%s" % (r.text,))
	return resp


def get_exchange_rates():
	"""
	https://blockchain.info/ticker
	:return:
	"""
	resp = submit_request("GET", "/ticker", {})
	return resp


def get_balance(address):
	"""
	https://blockchain.info/balance?active=$address
	:return:
	"""
	params = {
		"active": address,
	}
	resp = submit_request("GET", "/balance", params)
	final_balance = resp.get(address, {}).get("final_balance")
	return Decimal(final_balance / 100000000)


def get_transfer_detail(tx_hash):
	params = {
		"format": "json",
	}
	resp = submit_request("GET", f"/rawtx/{tx_hash}", params)
	# logger.info("交易[%s]详情:\n%s" % (tx_hash, json.dumps(resp, indent=2),))
	# final_balance = resp.get(address, {}).get("final_balance")
	# logger.info(f"final_balance:{final_balance}")
	# balance = final_balance / 100000000
	# return balance
	return resp


def get_transfer_list(address, page, pageNumber):
	limit = pageNumber
	offset = (page - 1) * limit
	params = {
		"address": address,
		"limit": limit,
		"offset": offset,
	}
	resp_data = submit_request("GET", f"/rawaddr/{address}", params)
	# logger.debug(json.dumps(resp_data, ensure_ascii=False, indent=2))
	result = resp_data.get("txs")
	if not isinstance(result, list):
		return []
	return result


def get_unspent_list(address, confirmations, limit):
	"""
	https://blockchain.info/unspent?active=$address
	:return:
	"""
	params = {
		"active": address,
		"confirmations": confirmations,
		"limit": limit,
	}
	resp_data = submit_request("GET", "/unspent", params)
	# logger.debug(json.dumps(resp_data, ensure_ascii=False, indent=2))
	unspent_outputs = resp_data.get("unspent_outputs")
	if not isinstance(unspent_outputs, list):
		return []
	return unspent_outputs


def get_exchange_tickers():
	"""
	https://api.blockchain.com/v3/exchange
	:return:
	"""
	url = "https://api.blockchain.com/v3/exchange/tickers"
	logger.info(f"[blockchain]请求[{url}]")
	headers = {
		"accept": "application/json"
	}
	r = requests.get(url, headers=headers)
	return r.json()
