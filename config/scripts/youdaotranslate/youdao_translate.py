#!/usr/bin/env python2
# coding: utf8

import sys
import requests
import json

# http://fanyi.youdao.com/openapi?path=data-mode
API_URL = "http://fanyi.youdao.com/openapi.do"
API_PARAMS = {
    'keyfrom': 'Mutate',
    'key': '1978918042',
    'type': 'data',
    'doctype': 'json',
    'version': '1.1',
}

ERROR_CODES = {
    20: u'要翻译的文本过长',
    30: u'无法进行有效的翻译',
    40: u'不支持的语言类型',
    50: u'无效的key',
    60: u'无词典结果，仅在获取词典结果生效',
}


class ScriptResult(object):
    def __init__(self, value, subtext='', command='copy', icon=''):
        self.value = value
        self.command = 'copy'
        self.icon = icon
        self.subtext = subtext

    def __str__(self):
        return (u"[{value}]\n"
                u"command={command}\n"
                u"icon={icon}\n"
                u"subtext={subtext}\n").format(**self.__dict__).encode('utf8')


def main():
    query = " ".join(sys.argv[1:])
    params = API_PARAMS.copy()
    params['q'] = query
    result = requests.get(API_URL, params).json()
    # print json.dumps(result, ensure_ascii=False, indent=2)

    if result['errorCode'] != 0:
        ScriptResult(ERROR_CODES.get(result['errorCode'], u'未知错误'))
        sys.exit(1)

    results = []
    if 'translation' in result:
        trans_list = result['translation']
        for trans in trans_list:
            results.append(ScriptResult(trans))

    if 'web' in result:
        web_list = result['web']
        for web in web_list:
            results.append(ScriptResult(web['key'], ",".join(web['value'])))

    if 'basic' in result:
        basic = result['basic']
        phonetic = basic.get('phonetic', '')
        if phonetic:
            for explain in basic.get('explains', []):
                results.append(ScriptResult(explain, phonetic))

    for result in results:
        print result


if __name__ == '__main__':
    main()

