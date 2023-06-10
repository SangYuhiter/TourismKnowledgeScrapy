#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# File Name    : OfficialWebsite.py
# Author       : SangYu
# Email        : sangyu.code@gmail.com
# Created Time : 2023年06月10日 星期六 11时30分03秒
# Description  : get official website information
"""

import os
from bs4 import BeautifulSoup
from BasicInternetConnect import request_url

STATISTICAL_INFORMATION_URL = "http://bldj.bijie.gov.cn/zwgk/zfxxgk/fdzdgknr/tjxx/index.html"
INFO_OUT = "./out/OfficialWebsite"


def get_statistical_information():
    main_page_source = request_url(STATISTICAL_INFORMATION_URL)
    main_page_source.encoding = main_page_source.apparent_encoding
    main_page_soup = BeautifulSoup(main_page_source.text, "lxml")
    main_page_soup.prettify()

    # find page num
    page_num_text = main_page_soup.find(class_="layuiPage").find(name="script").get_text()
    print(page_num_text)
    page_num = 0
    if page_num_text:
        page_num = int(page_num_text.split("(")[-1].split(",")[0])
    print("page_num:{}".format(page_num))

    # construct page url
    page_urls = []
    for i in range(page_num):
        page_url = STATISTICAL_INFORMATION_URL
        if i != 0:
            page_url = page_url.replace(".html", "_" + str(i) + ".html")
        print("i:{}\t------\tpage_url:{}".format(i, page_url))
        page_urls.append(page_url)

    # get each page article url
    article_urls = []
    for page_url in page_urls:
        print("get page_url:{}".format(page_url))
        each_page_source = request_url(page_url)
        each_page_source.encoding = each_page_source.apparent_encoding
        each_page_soup = BeautifulSoup(each_page_source.text, "lxml")
        each_page_soup.prettify()

        links = [(link["href"], link["title"].replace(" ", "")) for link in
                 each_page_soup.find(class_="zfxxgk_zdgkc").find_all(name="a")]
        article_urls += links
    for link_info in article_urls:
        print(link_info)

    if not os.path.exists(INFO_OUT):
        os.makedirs(INFO_OUT)
    # get each article content
    for link_info in article_urls:
        article_url = link_info[0]
        article_title = link_info[1]
        print("get title:{},article_url:{}".format(article_title, article_url))
        article_page_source = request_url(article_url)
        article_page_source.encoding = article_page_source.apparent_encoding
        article_page_soup = BeautifulSoup(article_page_source.text, "lxml")
        article_page_soup.prettify()

        # condition 1 --- has class="scroll_cont ScrollStyle"
        scroll_content = article_page_soup.find(class_="scroll_cont ScrollStyle")
        if scroll_content:
            article_name = os.path.join(INFO_OUT, article_title + ".txt")
            with open(article_name, "w", encoding="utf-8") as fw:
                fw.write(scroll_content.text)
                print("write scroll_content successfully!!!")
            xls_content = scroll_content.find_all(name="a")
            for xls_link in xls_content:
                suffix_info = xls_link.text.split(".")[-1]
                if suffix_info in ["xls", "doc", "pdf"]:
                    print(xls_link)
                    download_link = article_url[:article_url.rindex("/")] + xls_link["href"][1:]
                    download_name = os.path.join(INFO_OUT, xls_link["title"])
                    print("article_url:{},download_link:{}".format(article_url, download_link))
                    download_content = request_url(download_link).content
                    with open(download_name, "wb") as fd:
                        fd.write(download_content)
                    print("download {} successfully!!!".format(download_name))
        else:
            print("failed parse current article")


def get_content():
    scroll_content = None
    article_content = []
    for single_page_content in scroll_content.find_all(class_="ue_table"):
        for tr in single_page_content.find_all(name="tr"):
            line_content = ""
            for td in tr.find_all(name="td"):
                line_content += td.get_text() + "\t"
            article_content.append(line_content)


if __name__ == "__main__":
    get_statistical_information()

