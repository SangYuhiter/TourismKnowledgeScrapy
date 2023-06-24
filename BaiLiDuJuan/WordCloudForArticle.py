#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# File Name    : WordCloudForArticle.py
# Author       : SangYu
# Email        : sangyu.code@gmail.com
# Created Time : 2023年06月23日 星期五 11时05分55秒
# Description  : generate WordCloud
"""

import os
import pandas as pd
import jieba
from bs4 import BeautifulSoup
from WordCloud import generate_wordcloud_by_segment, generate_wordcloud_by_file

base_filename = "./out/article_titles_cluster_20_filtered.xlsx"
BAILIDUJUAN_1_OUT_PATH = "./out/BaiLiDuJuan"
BAILIDUJUAN_2_OUT_PATH = "./out/GuiZhouBaiLiDuJuanLvYou"
BASE_OUT_PATH = "wordcloud.png"
BAILIDUJUAN_DICT_PATH = "./SpecialDict.txt"
jieba.load_userdict(BAILIDUJUAN_DICT_PATH)

STOP_WORDS_FILE_PATH = "../stopwords.txt"


def load_stop_word_list(file_path):
    stop_words = set()
    with open(file_path, "r", encoding="utf-8") as f_stopwords:
        for line in f_stopwords:
            stop_words.add(line.strip())
    return stop_words


stop_words = load_stop_word_list(STOP_WORDS_FILE_PATH)

def get_main_information(file_path):
    print("get main information for {}".format(file_path))
    content = ""
    with open(file_path, "r", encoding="utf-8") as fr:
        content = fr.read()
    soup = BeautifulSoup(content, "lxml")
    soup.prettify()
    main_content = soup.find(class_="rich_media_content js_underline_content autoTypeSetting24psection")
    source_text = ""
    if main_content:
        source_text = main_content.get_text()
    else:
        source_text = soup.get_text()
    table = str.maketrans('', '', ' \n')
    source_text = source_text.translate(table)
    return source_text


def generate_one_label_tile(label, article_titles):
    content_file = BASE_OUT_PATH.replace(".png", "_" + str(label) + "_title.txt")
    out_put_img = BASE_OUT_PATH.replace(".png", "_" + str(label) + "_title.png")
    print("generate {} begin!!!".format(out_put_img))

    # read all file content
    segment = []
    for line in article_titles:
        line_content = line.strip().replace(" ", "")
        segment += [item for item in jieba.cut(line_content) if item.strip() and item not in stop_words]

    # generate img
    generate_wordcloud_by_segment(segment, out_put_img)
    print("generate {} end!!!".format(out_put_img))


def generate_one_label(label, article_titles):
    content_file = BASE_OUT_PATH.replace(".png", "_" + str(label) + ".txt")
    out_put_img = BASE_OUT_PATH.replace(".png", "_" + str(label) + ".png")
    print("generate {} begin!!!".format(out_put_img))

    # read all file content
    contexts = []
    for file in article_titles:
        path1 = os.path.join(BAILIDUJUAN_1_OUT_PATH, file)
        path2 = os.path.join(BAILIDUJUAN_2_OUT_PATH, file)
        content = ""
        if os.path.exists(path1):
            # print("path1 {} exists".format(path1))
            # content = get_main_information(path1)
            content = file
            pass
        elif os.path.exists(path2):
            # print("path2 {} exists".format(path2))
            # content = get_main_information(path2)
            content = file
            pass
        else:
            print("no such file!!!")
        contexts.append(content)

    with open(content_file, "w", encoding="utf-8") as fw:
        for line in contexts:
            fw.write(line + "\n")

    # generate img
    generate_wordcloud_by_file(content_file, out_put_img)
    print("generate {} end!!!".format(out_put_img))


def generate_all_label():
    df = pd.read_excel(base_filename)

    record_count = len(df['article_title'])
    labels = set()
    labels_articles = {}
    labels_articles_title = {}
    for i in range(record_count):
        article_title = df['article_title'][i]
        article_title_preprocess = df['preprocess_title'][i]
        label = df['label'][i]
        labels.add(label)
        if label not in labels_articles.keys():
            labels_articles[label] = [article_title]
            labels_articles_title[label] = [article_title_preprocess]
        else:
            labels_articles[label].append(article_title)
            labels_articles_title[label].append(article_title_preprocess)
    print("label content:{}".format(labels))
    # for k, v in labels_articles.items():
    #    print("label {} has content size {}".format(k,len(v)))

    for k, v in labels_articles.items():
        # generate_one_label(k, v)
        break
    for k, v in labels_articles_title.items():
        generate_one_label_tile(k, v)

    # generate all in one image
    generate_one_label_tile(999, df['preprocess_title'])


if __name__ == "__main__":
    generate_all_label()
    pass
