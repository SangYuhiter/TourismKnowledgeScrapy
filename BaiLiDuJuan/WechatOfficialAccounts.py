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
import sys
from bs4 import BeautifulSoup

sys.path.append("..")
from BasicInternetConnect import get_headers

WECHAT_MAIN_PAGE_URL = "https://mp.weixin.qq.com"
WECHAT_SEARCH_PAGE_URL = "https://mp.weixin.qq.com/cgi-bin/searchbiz"
WECHAT_ARTICLES_PAGE_URL = "https://mp.weixin.qq.com/cgi-bin/appmsg"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    # "Cookie": "appmsglist_action_3946503740=card; pac_uid=0_07feff2fa75e3; iip=0; pgv_pvid=1936248458; logTrackKey=e35157d2c7ec47a7a1ef5ff6246052ec; ua_id=4bpZ1czqYPI99twGAAAAACHpbCj7bRAT3xxAi9PPv1U=; wxuin=85875017099003; uuid=01963f8a2f172d8099e676cd355f1bc5; rand_info=CAESIOZ0e4Ix9TcbdZIERBrv75rpGOBlPk+aqQLZVi+yA4QT; slave_bizuin=3946503740; data_bizuin=3946503740; bizuin=3946503740; data_ticket=sS0/LtkhOfEvhDi5Knr06pckBTy7cdAPBNaKiTmksCrGLtT4J4NUROMq2N1lWLmt; slave_sid=ZGFnMW9CMXhjcW52M0pvSGMyM0ZEbTlBazZBSFhoQnp1X0tmTjlsYWxPcEVaNHZNWTY1TldDX1BFcFhfRlF3eUpaZnM1RThLZGJSbVludlJSSzFMWlJxREwxOGxObWZydHVya3RUWDIzcHFuOUFZVGRjSHVKNnR1cGdUR0lnT1dGOUlaSUptWHlsZ2ZmSmJZ; slave_user=gh_22b9ae63fe96; xid=da6fa6653543f08916f95bd32b884acf; mm_lang=zh_CN; _clck=3946503740|1|fcg|0; _clsk=1jq81kf|1686701030535|1|1|mp.weixin.qq.com/weheat-agent/payload/record",
    "Cookie": "appmsglist_action_3946503740=card; pac_uid=0_07feff2fa75e3; iip=0; pgv_pvid=1936248458; logTrackKey=e35157d2c7ec47a7a1ef5ff6246052ec; ua_id=4bpZ1czqYPI99twGAAAAACHpbCj7bRAT3xxAi9PPv1U=; wxuin=85875017099003; mm_lang=zh_CN; uuid=0774d337b6d8992b12cde963d576afaf; rand_info=CAESIDXYvU2vi8HT3OZ0yLaAEi6itMPEqMQ5wtSXaH0d3iL1; slave_bizuin=3946503740; data_bizuin=3946503740; bizuin=3946503740; data_ticket=vQBxHgYKSmDS5/PDFBCOGSfuKqoqXYE+eiK8Axj3wle+01J2iWdeKdma8uXUTF2H; slave_sid=RjZ1bFNVMFp2d1BoYmdicVZ4NkxrYno1RVVNbEp2MjBUaHBjODJ6SHlXSkVoR2tQVTFtVVVvWkJ0VVRRX0pIVm5KaEhSRFZEeGhYVzYxZmJrcmxKQlduZTk0NGhzeWV3cFRHSWlaNzk1bXQ5OUZkMGZuMU1WR2N6SWhQbmd2RnBHSmh4MnczcFlzdGhQblpk; slave_user=gh_22b9ae63fe96; xid=5ace0a55f7925fc97338b7699426a05e; _clck=3946503740|1|fco|0; _clsk=16lzoyo|1687403343250|2|1|mp.weixin.qq.com/weheat-agent/payload/record",
    "Host": "mp.weixin.qq.com",
    "Referer": "https://mp.weixin.qq.com/"
}

BAILIDUJUAN_NICKNAME_1 = "百里杜鹃"
BAILIDUJUAN_1_OUT_PATH = "./out/BaiLiDuJuan"
BAILIDUJUAN_NICKNAME_2 = "贵州百里杜鹃旅游"
BAILIDUJUAN_2_OUT_PATH = "./out/GuiZhouBaiLiDuJuanLvYou"
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
            page_count = 1
            current_page = 1
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
                        table = str.maketrans('\\|/?><:*"：“”\n', '-------------')
                        title = item['title'].strip().translate(table)
                        article_name = os.path.join(store_path, "[%s]%s.html" % (post_date, title))
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
    enable_path_1 = False
    if enable_path_1:
        resource_path_1 = os.path.join(BAILIDUJUAN_1_OUT_PATH, STATIC_RESOURCE_PATH)
        if not os.path.exists(resource_path_1):
            os.makedirs(resource_path_1)
        get_wechat_information(BAILIDUJUAN_NICKNAME_1, BAILIDUJUAN_1_OUT_PATH)

    enable_path_2 = True
    if enable_path_2:
        resource_path_2 = os.path.join(BAILIDUJUAN_2_OUT_PATH, STATIC_RESOURCE_PATH)
        if not os.path.exists(resource_path_2):
            os.makedirs(resource_path_2)
        get_wechat_information(BAILIDUJUAN_NICKNAME_2, BAILIDUJUAN_2_OUT_PATH)


def format_file_name(store_dir):
    files = [file for file in os.listdir(store_dir) if "html" in file]
    print(len(files))
    for file in files:
        table = str.maketrans('\\|/?><:*"：“”\n', '-------------')
        old_file = os.path.join(store_dir, file)
        new_file = os.path.join(store_dir, file.strip().translate(table))
        os.rename(old_file, new_file)

if __name__ == "__main__":
    # get_main_information()
    # format_file_name(BAILIDUJUAN_1_OUT_PATH)
    format_file_name(BAILIDUJUAN_2_OUT_PATH)
