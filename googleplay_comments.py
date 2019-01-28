# -*- coding: utf-8 -*-
'''
------------------------------------------------------------
File Name: gp_comments.py
Description :
Project: scripts
Last Modified: Friday, 25th January 2019 12:52:18 pm
-------------------------------------------------------------
'''


import asyncio
import json
import time
import re
from typing import List
# from pprint import pprint as print

from aiohttp import ClientSession

async def get_app_pagetoken(session: ClientSession, pkg_id: str) -> str:
    response = await session.get(
        url=f"https://play.google.com/store/apps/details?id={pkg_id}",
        headers={
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
            "cookie": "_ga=GA1.3.1820839936.1542965589; CONSENT=YES+HK.zh-CN+; _gac_UA-19995903-1=1.1544778308.EAIaIQobChMI-aab9_ue3wIV06mWCh2qTwiOEAAYASAAEgLSRvD_BwE; PLAY_ACTIVE_ACCOUNT=ICrt_XL61NBE_S0rhk8RpG0k65e0XwQVdDlvB6kxiQ8=linhanqiu@conew.com; OTZ=4735277_24_24__24_; ANID=AHWqTUmSVy1D0eD87D47gDkIHHK8h5bbnr9KogZZ4RsduO_Zx_l2MSO6u59FhiSL; _gid=GA1.3.366267096.1548316668; PLAY_PREFS=CqsMCP-p7oOwBxKhDBrtCxESExQVFhjUAdUBpwLEBOMF5QXoBdcG2AbeBt8GkJWBBpGVgQaSlYEGlZWBBpeVgQaklYEGuJWBBsCVgQbBlYEGxJWBBsWVgQbIlYEGzpWBBs-VgQbQlYEG1JWBBtmVgQbylYEGhpaBBoeWgQaLloEGjZaBBpKWgQabloEGnZaBBp6WgQafloEGoJaBBqaWgQanloEGqJaBBqmWgQbul4EG75eBBoWYgQaJmIEGq5uBBq2bgQbKm4EGy5uBBtWbgQa8nYEG3Z2BBuedgQaQnoEG4qKBBvOigQb8ooEGi6OBBpqkgQa_pYEG6qWBBsamgQbUpoEG1aaBBs6ogQa8rIEG1q-BBoeygQaJsoEG1rKBBrG0gQbWuYEGjsCBBqLAgQbAwIEGwcCBBvLAgQbWwoEGjMWBBo_FgQbKxoEGy8aBBrDHgQb4x4EGqsqBBtjMgQbczIEG3c2BBobOgQahz4EGxNKBBpXVgQba2IEG4tiBBvLbgQbY5IEGl-WBBrjogQbP64EGsOyBBtf1gQa6-4EGu_-BBsn_gQbVg4IGyISCBrmGggamh4IGp4eCBuyHggbth4IG642CBvuNggaJjoIGzJGCBpWYggaPmoIGmZqCBsGaggb3moIGnZ6CBvaiggbipIIGkqWCBp6ogga0qIIG0bWCBq22ggb8uYIG_rmCBv-5ggbCu4IGj7-CBrzBggaQy4IGkcuCBtHLggbczIIG2NCCBovSggba04IGgdiCBoXaggaN2oIGnNqCBqPaggbF24IGsdyCBvjdggbv34IGpOGCBuThggbl4YIGlumCBqPtggaF7oIGmu6CBrPuggax8IIG6_aCBq34ggaz-IIG9vqCBuP7ggbb_IIGgICDBvKBgwbphIMGkIWDBteFgwbXh4MGm4iDBrmIgwbwiIMGhY-DBpCPgwbZkYMG_JGDBvySgwaslYMGuJWDBsCWgwbjloMG3JeDBpmbgwbQnIMG8Z6DBvSegwaYoIMGm6CDBv2ggwbsr4MGiLCDBpW0gwantIMGqLSDBq20gwa4toMGgLiDBuC8gwb0vIMG9ryDBq6-gwbNvoMGnsODBrjGgwbkxoMGrciDBp7JgwabyoMG9cuDBsrNgwb-zYMGotCDBrrQgwb504MG69SDBs_Wgwbj14MG6deDBtHZgwaA3oMGsN-DBojggwaN4YMG7-ODBqblgwaA5oMGkOaDBursgwaV7oMGwO-DBuPvgwaf8oMGnfSDBtX0gwb594MGjfiDBq37gwaM_oMGpP6DBof_gwangYQG3YGEBt-BhAbygoQG-oOEBo-EhAbXhIQGyYiEBsqIhAa-iYQGp4uEBpqMhAb1jIQGgI6EBqyOhAatjoQGhpCEBtuThAaKmIQG9JiEBpqZhAb9moQG-ZyEBoqdhAbhn4QGlaCEBs2jhAbPo4QG0KOEBqGkhAaopYQG0aaEBv-nhAaSqYQGk6mEBqmvhAbBr4QG2rOEBqC2hAahtoQGrbiEBuO4hAaguYQGwLmEBsi7hAb9u4QGh7-EBqy_hAa3v4QGo8GEBtbChAbywoQGjMOEBprDhAbixYQGpsiEBrfIhAbkyYQGhcqEBpPLhAbLy4QGsMyEBunOhAb7zoQG_tCEBp_RhAap0YQGgtOEBoTThAaG1IQGr9iEBsfYhAbr3oQGpeGEBrrhhAbY4YQGiuKEBsfmhAbr5oQGgOeEBojnhAbC54QGnOiEBvLphAau6oQG4uuEBsrthAbR8YQGj_SEBsn0hAbc9oQGi_iEBsn4hAab-YQG8vqEBon7hAat-4QGt_yEBsL8hAaE_oQGhf6EBqf-hAbx_oQG-f6EBr-BhQbJgYUGzYGFBrWEhQajhYUGpYWFBrOGhQbihoUGr4eFBrKHhQa3h4UGxYeFBtmHhQaBiIUGgoiFBu-JhQaujIUGmo2FBqaNhQbJjYUG9Y2FBv6NhQaHjoUGto6FBqmPhQaClIUGg5SFBtuUhQaBlYUGzZWFBvSVhQbFloUG9JeFBruZhQbcmYUGKLzn8pqILTokOTQyOGJhOGItZmFmMS00ZDM1LTgyOTQtODE0YWVhOGRkMDVmQAFIAA:S:ANO1ljIHe4Js8JmLdA; NID=156=M9bTLLm2gd-3UKNbG5qrF6bU8v3T7HMDr9bpXvgePlonB2hr9gJvF3Xz_fNkPESlRd4y89T0klQhNpO5Nx5PNUUgpxdm0DZoMXv9J454mLSqKsZX7QB-ACFaG4bqEugQcomRZh2cUF8kdb_1G8rF-ayyRZaPmMsVlGy7I5xCVOJtYxXrEX26EquNfxbPOZeiDEqpo_VlXeSYjasjGmtgFfaEtlU0-Q03zYM2imAAfkVgldU8QeqzwRyjZexvP4q9Sl3iWBcr8Wrb7P6IG0uVAQSPRlW871jVKLG4ppPolCNBX7LqnIZ1EWPq5cB1xaJ7wrzfU5oUyRNiNtfpkTRMGf0NZ3o9p4DZkLYrFZEL4Kiy4_UB8PWoPfmSCUlRC-0W1Y85f9G8aw6233qHC9ByKgL9AU11Anc_x6FjcCwYW0Uw6DRb9f3--fdTHLYvZsIB2_MmO46BXTWsbqk; 1P_JAR=2019-1-25-7; _gat_UA199959031=1; SID=_gY2X6Y0xxZJjS-K8soQ2T-hgyteKV3BLTf_ONqcpgYdk41lfDteE-g9h28MOsvJjY3ROw.; HSID=AI5hSxuIOav0IMFcs; SSID=AbWm0SqvtTDIA3VRh; APISID=m8GuuywKHx9TGMHd/AICPxy0wQ3VAArlfe; SAPISID=Wh-EVc5SMV9Ddo92/A-naEwku_xVOhxRYS; _gat=1; S=billing-ui-v3=AhEI9U6PW7cyMzA-ox6_8byK6zBXZrbT:billing-ui-v3-efe=AhEI9U6PW7cyMzA-ox6_8byK6zBXZrbT; SIDCC=ABtHo-HhDgNDAzGs_kURskAF9p0PgLj2Q7uH5_ULkl2rKNXXBHD1G0h-YxlNCYHOXIrzoY45Shw"
        }
    )
    sid = re.findall(r'FdrFJe":"([\s\S]*?)"', await response.text())[0]
    content = re.findall(r"ds:22', isError[\s\S]*?script nonce", await response.text())[0]
    content = re.sub(r'gp:[\s\S]*?gp', '', content)
    content = re.findall(r'\[null,"[\s\S]*?"]', content)[0]
    content = json.loads(content)
    return sid, content[1]


async def get_app_comment(session: ClientSession, app_id: str, sid: str, pagetoken: str):
    if pagetoken == "null":
        datas = r'[[["UsvDTd","[null,null,[2,2,[100,null,%s]],[\"%s\",7]]",null,"generic"]]]' % (
            pagetoken, app_id)
    else:
        datas = r'[[["UsvDTd","[null,null,[2,2,[100,null,\"%s\"]],[\"%s\",7]]",null,"generic"]]]' % (
            pagetoken, app_id)
    response = await session.post(
        url="https://play.google.com/_/PlayStoreUi/data/batchexecute",
        data={
            "f.req": datas,
        },
        headers={
            "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
            "cookie": "_ga=GA1.3.1820839936.1542965589; CONSENT=YES+HK.zh-CN+; _gac_UA-19995903-1=1.1544778308.EAIaIQobChMI-aab9_ue3wIV06mWCh2qTwiOEAAYASAAEgLSRvD_BwE; PLAY_ACTIVE_ACCOUNT=ICrt_XL61NBE_S0rhk8RpG0k65e0XwQVdDlvB6kxiQ8=linhanqiu@conew.com; OTZ=4735277_24_24__24_; ANID=AHWqTUmSVy1D0eD87D47gDkIHHK8h5bbnr9KogZZ4RsduO_Zx_l2MSO6u59FhiSL; _gid=GA1.3.366267096.1548316668; HSID=AI7LcTNumNKVJYskH; SSID=AGVwalxddwiJmb5KR; APISID=gEvcSm73s9Ds_M_J/AGB3EUFPxmUM2DDck; SAPISID=p-WOBFB7PF8kRWWX/A_4eEk7ieY0Lm7Ch9; SID=_gY2X6m_0J0xw789GcDQoma8_vA_ZHzYGyRbrvvO45ADGBmPPxOUpVZT8GgKoihMmYoy7w.; NID=156=O6u-TNLvVppN6F3sohQu_SDFVKQFG0faUxMBl_sV_INnlqU4K93uDVXRjKvaU6YdIwanJ4DCHKJV4CTMPhzL_6MKqEpsc8sumWx4u4wagd0gRFRBg0cpZGfM1mYTGCWvuQUdK7YK0hfiTwBhqFOek4jxqg0WYxxwQWcWUIgrqbBtfKcPlZC8rqKEBksq7BVVETymrlgMalUBjCPdMApJfwxXNSet4efmSuYNLlwg_VcCtBsgJ-dc35PkzCkWgMUO37xvfbbyJ8w-HApw4lSBUkcnA5_gYDYCez_s3GFRYuqKkj9tvQ3UIWZ9Bsw_ZVHXhRQRiwutBNsZpvP0ZAMzq7wp0PHq4oaWvjGV9Eqv9uxrFLyUxDPYs-nbgtdgZ7sQc1YcQmeLJ1TeFVWqcBFgJhf6O64xgez5FhY6glf3ICT-3zw5rZDxxzXHltSI2rjiEx0jsvNj93gl4Hs; PLAY_PREFS=CqsMCP-p7oOwBxKhDBrtCxESExQVFhjUAdUBpwLEBOMF5QXoBdcG2AbeBt8GkJWBBpGVgQaSlYEGlZWBBpeVgQaklYEGuJWBBsCVgQbBlYEGxJWBBsWVgQbIlYEGzpWBBs-VgQbQlYEG1JWBBtmVgQbylYEGhpaBBoeWgQaLloEGjZaBBpKWgQabloEGnZaBBp6WgQafloEGoJaBBqaWgQanloEGqJaBBqmWgQbul4EG75eBBoWYgQaJmIEGq5uBBq2bgQbKm4EGy5uBBtWbgQa8nYEG3Z2BBuedgQaQnoEG4qKBBvOigQb8ooEGi6OBBpqkgQa_pYEG6qWBBsamgQbUpoEG1aaBBs6ogQa8rIEG1q-BBoeygQaJsoEG1rKBBrG0gQbWuYEGjsCBBqLAgQbAwIEGwcCBBvLAgQbWwoEGjMWBBo_FgQbKxoEGy8aBBrDHgQb4x4EGqsqBBtjMgQbczIEG3c2BBobOgQahz4EGxNKBBpXVgQba2IEG4tiBBvLbgQbY5IEGl-WBBrjogQbP64EGsOyBBtf1gQa6-4EGu_-BBsn_gQbVg4IGyISCBrmGggamh4IGp4eCBuyHggbth4IG642CBvuNggaJjoIGzJGCBpWYggaPmoIGmZqCBsGaggb3moIGnZ6CBvaiggbipIIGkqWCBp6ogga0qIIG0bWCBq22ggb8uYIG_rmCBv-5ggbCu4IGj7-CBrzBggaQy4IGkcuCBtHLggbczIIG2NCCBovSggba04IGgdiCBoXaggaN2oIGnNqCBqPaggbF24IGsdyCBvjdggbv34IGpOGCBuThggbl4YIGlumCBqPtggaF7oIGmu6CBrPuggax8IIG6_aCBq34ggaz-IIG9vqCBuP7ggbb_IIGgICDBvKBgwbphIMGkIWDBteFgwbXh4MGm4iDBrmIgwbwiIMGhY-DBpCPgwbZkYMG_JGDBvySgwaslYMGuJWDBsCWgwbjloMG3JeDBpmbgwbQnIMG8Z6DBvSegwaYoIMGm6CDBv2ggwbsr4MGiLCDBpW0gwantIMGqLSDBq20gwa4toMGgLiDBuC8gwb0vIMG9ryDBq6-gwbNvoMGnsODBrjGgwbkxoMGrciDBp7JgwabyoMG9cuDBsrNgwb-zYMGotCDBrrQgwb504MG69SDBs_Wgwbj14MG6deDBtHZgwaA3oMGsN-DBojggwaN4YMG7-ODBqblgwaA5oMGkOaDBursgwaV7oMGwO-DBuPvgwaf8oMGnfSDBtX0gwb594MGjfiDBq37gwaM_oMGpP6DBof_gwangYQG3YGEBt-BhAbygoQG-oOEBo-EhAbXhIQGyYiEBsqIhAa-iYQGp4uEBpqMhAb1jIQGgI6EBqyOhAatjoQGhpCEBtuThAaKmIQG9JiEBpqZhAb9moQG-ZyEBoqdhAbhn4QGlaCEBs2jhAbPo4QG0KOEBqGkhAaopYQG0aaEBv-nhAaSqYQGk6mEBqmvhAbBr4QG2rOEBqC2hAahtoQGrbiEBuO4hAaguYQGwLmEBsi7hAb9u4QGh7-EBqy_hAa3v4QGo8GEBtbChAbywoQGjMOEBprDhAbixYQGpsiEBrfIhAbkyYQGhcqEBpPLhAbLy4QGsMyEBunOhAb7zoQG_tCEBp_RhAap0YQGgtOEBoTThAaG1IQGr9iEBsfYhAbr3oQGpeGEBrrhhAbY4YQGiuKEBsfmhAbr5oQGgOeEBojnhAbC54QGnOiEBvLphAau6oQG4uuEBsrthAbR8YQGj_SEBsn0hAbc9oQGi_iEBsn4hAab-YQG8vqEBon7hAat-4QGt_yEBsL8hAaE_oQGhf6EBqf-hAbx_oQG-f6EBr-BhQbJgYUGzYGFBrWEhQajhYUGpYWFBrOGhQbihoUGr4eFBrKHhQa3h4UGxYeFBtmHhQaBiIUGgoiFBu-JhQaujIUGmo2FBqaNhQbJjYUG9Y2FBv6NhQaHjoUGto6FBqmPhQaClIUGg5SFBtuUhQaBlYUGzZWFBvSVhQbFloUG9JeFBruZhQbcmYUGKLzn8pqILTokOTQyOGJhOGItZmFmMS00ZDM1LTgyOTQtODE0YWVhOGRkMDVmQAFIAA:S:ANO1ljIHe4Js8JmLdA; S=billing-ui-v3=xf2yyzo3IRNdKfI4LFU4fN1UDmShKwa0:billing-ui-v3-efe=xf2yyzo3IRNdKfI4LFU4fN1UDmShKwa0; 1P_JAR=2019-1-25-5; _gat_UA199959031=1; SIDCC=ABtHo-FEzd7FarZ-XuGaTOt3oY8Hx6OSLgyRMHrZ52iyD4SMqq3p53l-Je6swLbaoAFuLBH3Gs8"
        },
        params={
            "rpcids": "UsvDTd",
            "f.sid": sid,
            "bl": "boq_playuiserver_20190122.10_p0",
            "hl": "zh-CN",
            "authuser": 1,
            "soc-app": 121,
            "soc-platform": 1,
            "soc-device": 1,
            "rt": "c"
        }
    )
    text = await response.text()
    pagetoken = re.findall(
        r'\[null,\\"(C[\s\S]*?)\\"]\\n]\\n",null,null,null,"generic"]\n', text)
    pagetoken = pagetoken[0] if pagetoken else ""
    c = parse(content=text)
    stop = 0
    for i in c:
        if i["date"] < 1514736000:
            stop = 1
            break

    return c, pagetoken, stop


def parse(content: str) -> List[str]:
    comments = []
    text = re.findall(r'(\[\\"gp[\s\S]*?)\\n\,\[\\"gp', content)
    for i in text:
        i = i.replace('\\n', '')
        i = i.replace('\\', '')
        try:
            format_comment = json.loads(i)
            comment = {
                "uid": format_comment[1][0],
                "date": format_comment[5][0],
                "content": f"{format_comment[3]}{format_comment[4]}".replace("None", "")
            }
            comments.append(comment)
        except json.JSONDecodeError as e:
            pass
    return comments


async def side(session: ClientSession, pkg_id: str):
    sign = ""
    sid, pagetoken = await get_app_pagetoken(
        session=session,
        pkg_id=pkg_id
    )
    comments = []
    pagetoken = "null"
    while sign != pagetoken:
        sign = pagetoken
        comment, pagetoken, stop = await get_app_comment(
            session=session,
            app_id=pkg_id,
            sid=sid,
            pagetoken=pagetoken
        )
        if not pagetoken:
            break
        if stop:
            break
    

async def main():
    pkg_ids = ["com.android.chrome"]
    tasks = [
        side(
            session=aiohttp.ClientSession(),
            pkg_id=pkg_id
        ) for pkg_id in pkg_ids
    ]
    await asyncio.gather(* tasks)

import aiohttp
l = asyncio.get_event_loop()
l.run_until_complete(main())
