#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# File Name    : WechatOfficialAccounts.py
# Author       : SangYu
# Email        : sangyu.code@gmail.com
# Created Time : 2023年06月10日 星期六 23时04分43秒
# Description  : get information from Wechat Official Accounts
"""
import os
import random
import re
import hashlib
import requests
import time
from bs4 import BeautifulSoup
from BasicInternetConnect import get_headers

WECHAT_MAIN_PAGE_URL = "https://mp.weixin.qq.com"
WECHAT_SEARCH_PAGE_URL = "https://mp.weixin.qq.com/cgi-bin/searchbiz"
WECHAT_ARTICLES_PAGE_URL = "https://mp.weixin.qq.com/cgi-bin/appmsg"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Cookie": "appmsglist_action_3946503740=card; pac_uid=0_07feff2fa75e3; iip=0; pgv_pvid=1936248458; logTrackKey=e35157d2c7ec47a7a1ef5ff6246052ec; ua_id=4bpZ1czqYPI99twGAAAAACHpbCj7bRAT3xxAi9PPv1U=; wxuin=85875017099003; rewardsn=; wxtokenkey=777; uuid=d07ca0b3207f7b7831e17b653a9940d0; cert=dBebXfGZL9zpD16VcAxZmCeszcoPu1NP; sig=h01d03b9a7514b1d714ea70e689147171721d0c649b9e0ed7768252e715f51b535d6b4ac40b891916e2; data_bizuin=3946503740; bizuin=3946503740; master_user=gh_22b9ae63fe96; master_sid=MEZBR01FQ204R1h4S09kcVJPMVdUR003Q0czbmU1ak5tWUtFSUlDbDYwMVQ5QmJSU0ZlcnRyWVJvM3N2TzBHaW83Qm9xNkJRMDV0NnloWTVfXzN4YmhxUWF1MWxyME1RT09TRHBaQ3JnV2xFajUzOVNQdDBNMWtBaDF5R2N1bTRraFRDZjBvdm5ocEtncXZY; master_ticket=c2d5f5626421ce5c0a45d574fc0058b1; media_ticket=e2487039808a5c7e8c498f644aad4032cc7336bc; media_ticket_id=3946503740; data_ticket=2BpBuRH/rOq20dkQZJ1miLDRbrMS/BqGWKfzq9JrL1b9gTyI5CB2k8DzI0NGY8ja; rand_info=CAESIM7uWpCug9gIigBAmwKfD+RNkQdjGRD0thJmF0iP0LQ1; slave_bizuin=3946503740; slave_user=gh_22b9ae63fe96; slave_sid=YjlOa2V4c2Z3N3JETWMzcTVrMmI5WXZIZ3llRjBXT0Z5ZGNQdVhqV09FR0JoV0dCblNfN25OUkNZU0xwanpWQ0RmekRZeU5HQ0lmRFRSTTlFaUtNWnFWWkkwMXNYMVpkcGFMTWdad2ZGTjNtZkc4ZzlaQWUxYVNTcHpTMlJrZUtPR1NES3hwNjE2SlRwZnh1; _clck=3946503740|1|fcc|0; _clsk=1xzn02j|1686408619952|8|1|mp.weixin.qq.com/weheat-agent/payload/record",
    "Host": "mp.weixin.qq.com",
    "Referer": "https://mp.weixin.qq.com/"
}

BAILIDUJUAN_NICKNAME_1 = "百里杜鹃"
BAILIDUJUAN_1_OUT_PATH = "./out/百里杜鹃"
STATIC_RESOURCE_PATH = "static"

def md5(x):
    m = hashlib.md5()
    m.update(x.encode('utf-8'))
    return m.hexdigest()
def get_wechat_information(nickname, store_path):
    s = requests.session()
    res = s.get(url=WECHAT_MAIN_PAGE_URL, headers=headers)
    if res.status_code == 200:
        print(res.url)

        # get token
        token = re.findall(r'.*?token=(\d+)', res.url)
        if token:
            token = token[0]
            print("token is {}".format(token))
        else:
            print("login failed for no token in url")
            return

        # search wechat official account
        data = {
            "action":"search_biz",
            "begin": "0",
            "count": "5",
            "query": nickname,
            "token": token,
            "lang": "zh_CN",
            "f": "json",
            "ajax": "1"
        }
        res = s.get(url=WECHAT_SEARCH_PAGE_URL, params=data, headers=headers)
        if res.status_code == 200:
            # get first item fakeid
            # print(res.json())
            fakeid = res.json()['list'][0]['fakeid']
            print("nickname:{},fakeid:{}".format(nickname, fakeid))

            # get article link
            page_size = 5
            page_count = 165
            current_page = 148
            while current_page <= page_count:
                data = {
                    "action": "list_ex",
                    "begin": str(page_size * (current_page - 1)),
                    "count": str(page_size),
                    "fakeid": fakeid,
                    "type": "9",
                    "query": "",
                    "token": token,
                    "lang": "zh_CN",
                    "f": "json",
                    "ajax": "1"
                }
                res = s.get(url=WECHAT_ARTICLES_PAGE_URL, params=data, headers=headers)
                if res.status_code == 200:
                    print(res.json())

                    # update page_count
                    if current_page == 1:
                        app_msg_cnt = res.json()['app_msg_cnt']
                        if app_msg_cnt % page_size == 0:
                            page_count = int(app_msg_cnt/page_size)
                        else:
                            page_count = int(app_msg_cnt/page_size) + 1
                    print("page_count:{},current_page:{}".format(page_count,current_page))

                    # save article info
                    app_msg_list = res.json()['app_msg_list']
                    for item in app_msg_list:
                        article_link = item['link']
                        post_date = time.strftime("%Y-%m-%d", time.localtime(int(item['update_time'])))
                        table = str.maketrans('\\|/?><:*"：“”', '------------')
                        title = item['title'].strip().translate(table)
                        article_name = os.path.join(BAILIDUJUAN_1_OUT_PATH, "[%s]%s.html" % (post_date, title))
                        res = s.get(url=article_link, headers=get_headers())
                        if res.status_code == 200:
                            article_soup = BeautifulSoup(res.text, "lxml")
                            article_soup.prettify()
                            article_content = res.content.decode()

                            # find img and replace
                            for img in article_soup.find_all('img'):
                                print(img)
                                img_url = img.attrs.get('src', '').strip()
                                img_url = img_url if img_url else img.attrs.get('data-src', '').strip()
                                if img_url:
                                    if img_url.startswith("//"):
                                        img_url = 'http:' + img_url
                                    if not img_url.startswith("http"):
                                        continue
                                    img_filename = '%s/%s/%s' % (store_path, STATIC_RESOURCE_PATH, md5(img_url))
                                    local_img_uri = '%s/%s' % (STATIC_RESOURCE_PATH, md5(img_url))
                                    if not os.path.isfile(img_filename):
                                        res = s.get(img_url, headers=get_headers())
                                        if res.status_code == 200:
                                            with open(img_filename, "wb") as fw:
                                                fw.write(res.content)
                                    print("replace {} by {}".format(img_url, local_img_uri))
                                    article_content = article_content.replace(img_url, local_img_uri)
                            article_content = article_content.replace("data-src", "src")
                            with open(article_name, "w", encoding="utf-8") as fw:
                                fw.write(article_content)
                            print("{} download successfully!!!".format(article_name))
                            sleep_time = random.randint(1, 10)
                            print("sleep {} s for scrapy".format(sleep_time))
                            time.sleep(sleep_time)
                        else:
                            print("get article_name:{},failed for {}".format(article_name, res.status_code))
                current_page += 1
        else:
            print("get nickname:{} fackid failed".format(nickname))
    else:
        print("login failed for {}".format(res.status_code))

def get_main_information():
    resource_path_1 = os.path.join(BAILIDUJUAN_1_OUT_PATH, STATIC_RESOURCE_PATH)
    if not os.path.exists(resource_path_1):
        os.makedirs(resource_path_1)
    get_wechat_information(BAILIDUJUAN_NICKNAME_1, BAILIDUJUAN_1_OUT_PATH)


if __name__ == "__main__":
    get_main_information()
