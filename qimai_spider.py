# -*- coding: utf-8 -*-

'''
------------------------------------------------------------
File Name: qimai.py
Description : 
Project: test
Last Modified: Friday, 25th January 2019 8:55:39 am
-------------------------------------------------------------
'''


import time
from urllib.parse import urlencode
import json
import base64

import requests


headers = {
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.qimai.cn/rank",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/59.0"
}

params = {
    "brand": "all",
    "country": "cn",
    "date": "2019-01-20",
    "device": "iphone",
    "genre": "36",
    "page": 1
}


# 自定义加密函数
def encrypt(
    a: str,
    n="00000008d78d46"
) -> str:
    s, n = list(a), list(n)
    sl, nl = len(s), len(n)
    for i in range(0, sl):
        s[i] = chr(ord(s[i]) ^ ord(n[i % nl]))
    return "".join(s)


def main() -> None:
    # iPhone 免费榜单

    # 步骤一：时间差
    t = str(int((time.time() * 1000 - 1515125653845)))
    # 步骤二：提取查询参数值并排序
    s = "".join(sorted([str(v) for v in params.values()]))
    # 步骤三：Base64 Encode
    s = base64.b64encode(bytes(s, encoding="ascii"))
    # 步骤四：拼接自定义字符串
    s = "@#".join([s.decode(), "/rank/indexPlus/brand_id/1", t, "1"])
    # 步骤五：自定义加密 & Base64 Encode
    s = base64.b64encode(bytes(encrypt(s), encoding="ascii"))
    # 步骤六：拼接 URL
    params["analysis"] = s.decode()
    url = "https://api.qimai.cn/rank/indexPlus/brand_id/1?{}".format(
        urlencode(params))
    # 测试：发起请求
    res = requests.get(url, headers=headers)
    rsp = json.loads(res.text)
    print(rsp)


if __name__ == '__main__':
    main()
