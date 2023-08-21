#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
错误配置
"""


class ErrKey(object):
    OK = "OK"
    Success = "Success"
    UnkownErr = "UnkownErr"
    ParamErr = "ParamErr"
    UnChangeErr = "UnChangeErr"
    NotFoundErr = "NotFoundErr"
    RecordExistErr = "RecordExistErr"
    UserNotExistErr = "UserNotExistErr"

    TokenErr = "TokenErr"
    AuthErr = "AuthErr"

    PasswordErr = "PasswordErr"
    SystemErr = "SystemErr"


ErrInfo = {
    "OK": {"c": 0, "m": "ok"},
    "Success": {"c": 0, "m": "ok"},

    "UnkownErr": {"c": -1, "m": "unkown err."},
    "ParamErr": {"c": 1, "m": "param is error"},
    "UnChangeErr": {"c": 302, "m": "数据无变化"},
    "NotFoundErr": {"c": 404, "m": "not found"},
    "RecordExistErr": {"c": 405, "m": "记录已存在"},
    "UserNotExistErr": {"c": 8, "m": "用户不存在"},

    "TokenErr": {"c": 9, "m": "token invalid"},  # 出现这个错误的时候，客户端会根据这个错误码自动重新登录，不可以随便修改此错误码
    "AuthErr": {"c": 10, "m": "auth invalid"},

    "PasswordErr": {"c": 11, "m": "账号或密码错误"},

    "SystemErr": {"c": -99, "m": "system error"}

}
