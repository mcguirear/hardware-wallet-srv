# -*- coding: utf-8 -*-
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_DOWN


def round_half_up_dec(n, d):
    s = '0.' + '0' * d
    v = Decimal(str(n)).quantize(Decimal(s), ROUND_HALF_UP)
    return v


def round_half_down_dec(n, d):
    s = '0.' + '0' * d
    v = Decimal(str(n)).quantize(Decimal(s), ROUND_HALF_DOWN)
    return v
