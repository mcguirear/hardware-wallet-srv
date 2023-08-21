# -*- coding: utf-8 -*-
LANG_DATA = {
	"zh": {
		"success": "成功!",
	},
	"en": {
		"success": "Success!",
	}
}


def getText(key, lang):
	"""
	获取文本信息
	:param key:
	:param lang:
	:return:
	"""
	text = LANG_DATA.get(lang, {}).get(key, "")
	if not text and lang != 'en':
		text = LANG_DATA.get('en', {}).get(key, "")
	if not text: text = key
	return text
