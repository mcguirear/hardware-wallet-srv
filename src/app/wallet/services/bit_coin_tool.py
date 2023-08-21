# -*- coding: utf-8 -*-
import re
from typing import Tuple

from app.wallet.services.py3specials import changebase, bin_dbl_sha256

MAGIC_BYTE = 0
SCRIPT_MAGICBYTE = 5
SEGWIT_HRP = "bc"


class UnrecognisedPublicKeyFormat(BaseException):
	pass


def get_pubkey_format(pub) -> str:
	two = 2
	three = 3
	four = 4
	
	if isinstance(pub, (tuple, list)):
		return 'decimal'
	elif len(pub) == 65 and pub[0] == four:
		return 'bin'
	elif len(pub) == 130 and pub[0:2] == '04':
		return 'hex'
	elif len(pub) == 33 and pub[0] in [two, three]:
		return 'bin_compressed'
	elif len(pub) == 66 and pub[0:2] in ['02', '03']:
		return 'hex_compressed'
	elif len(pub) == 64:
		return 'bin_electrum'
	elif len(pub) == 128:
		return 'hex_electrum'
	else:
		raise UnrecognisedPublicKeyFormat("Pubkey not in recognized format")


def b58check_to_bin(inp: str) -> Tuple[int, bytes]:
	leadingzbytes = len(re.match('^1*', inp).group(0))
	data = b'\x00' * leadingzbytes + changebase(inp, 58, 256)
	assert bin_dbl_sha256(data[:-4])[:4] == data[-4:]
	magicbyte = data[0]
	return magicbyte, data[1:-4]


def is_public_key(pub: str) -> bool:
	try:
		fmt = get_pubkey_format(pub)
		return True
	except UnrecognisedPublicKeyFormat:
		return False


def is_p2pkh(addr: str) -> bool:
	"""
	Legacy addresses only doesn't include Cash P2PKH Address
	"""
	try:
		magicbyte, bin = b58check_to_bin(addr)
		return magicbyte == MAGIC_BYTE
	except Exception:
		return False


def is_p2sh(addr: str) -> bool:
	"""
	Check if addr is a pay to script address
	"""
	try:
		magicbyte, bin = b58check_to_bin(addr)
		return magicbyte == SCRIPT_MAGICBYTE
	except Exception:
		return False


def is_native_segwit(addr: str) -> bool:
	return addr.startswith(SEGWIT_HRP)


def is_address(addr: str) -> bool:
	"""
	Check if addr is a valid address for this chain
	"""
	return is_p2pkh(addr) or is_p2sh(addr) or is_native_segwit(addr) or is_public_key(addr)
