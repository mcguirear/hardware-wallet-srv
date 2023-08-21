# -*- coding: utf-8 -*-
from app.wallet.app_sio import app
from app.wallet.app_authorize import deal_handler
from app.wallet.services import wallet_service

from xlib import xlog

logger = xlog.getLogger()


@app.route('/wallet/getPrice', methods=['GET', 'POST'])
@deal_handler(check_sign=False, check_token=False)
def walletGetPrice(arguments, **kwargs):
	"""
	查询最新价格
	:param arguments:
	:param kwargs:
	:return:
	"""
	return wallet_service.getPrice(arguments, **kwargs)


@app.route('/wallet/getBalance', methods=['GET', 'POST'])
@deal_handler(check_sign=False, check_token=False)
def walletGetBalance(arguments, **kwargs):
	"""
	查询余额
	:param arguments:
	:param kwargs:
	:return:
	"""
	return wallet_service.getBalance(arguments, **kwargs)


@app.route('/wallet/validateAddress', methods=['GET', 'POST'])
@deal_handler(check_sign=False, check_token=False)
def walletValidateAddress(arguments, **kwargs):
	"""
	验证地址
	:param arguments:
	:param kwargs:
	:return:
	"""
	return wallet_service.validateAddress(arguments, **kwargs)


@app.route('/wallet/sendRawTransaction', methods=['GET', 'POST'])
@deal_handler(check_sign=False, check_token=False)
def walletSendRawTransaction(arguments, **kwargs):
	"""
	发送交易
	:param arguments:
	:param kwargs:
	:return:
	"""
	return wallet_service.sendRawTransaction(arguments, **kwargs)


@app.route('/wallet/estimateFee', methods=['GET', 'POST'])
@deal_handler(check_sign=False, check_token=False)
def walletGetEstimateFee(arguments, **kwargs):
	"""
	查询币种默认矿工费
	:param arguments:
	:param kwargs:
	:return:
	"""
	return wallet_service.estimateFee(arguments, **kwargs)


@app.route('/wallet/getTransactions', methods=['GET', 'POST'])
@deal_handler(check_sign=False, check_token=False)
def walletGetTransactions(arguments, **kwargs):
	"""
	查询交易记录
	:param arguments:
	:param kwargs:
	:return:
	"""
	return wallet_service.getTransactions(arguments, **kwargs)


@app.route('/wallet/getTransactionDetail', methods=['GET', 'POST'])
@deal_handler(check_sign=False, check_token=False)
def walletGetTransactionDetail(arguments, **kwargs):
	"""
	查询交易记录详情
	:param arguments:
	:param kwargs:
	:return:
	"""
	return wallet_service.getTransactionDetail(arguments, **kwargs)


@app.route('/wallet/getUTXOs', methods=['GET', 'POST'])
@deal_handler(check_sign=False, check_token=False)
def walletGetUTXOs(arguments, **kwargs):
	"""
	BTC获取UTXO列表
	:param arguments:
	:param kwargs:
	:return:
	"""
	return wallet_service.getUTXOs(arguments, **kwargs)
