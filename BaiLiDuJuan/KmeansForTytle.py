#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# File Name    : KmeansForTytle.py
# Author       : SangYu
# Email        : sangyu.code@gmail.com
# Created Time : 2023年06月23日 星期五 01时10分18秒
# Description  : Kmeans for article titles
"""

import os
import re
import jieba
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer



BAILIDUJUAN_1_OUT_PATH = "./out/BaiLiDuJuan"
BAILIDUJUAN_2_OUT_PATH = "./out/GuiZhouBaiLiDuJuanLvYou"
ARTICLE_TITLES_OUT_FILE = "./out/article_titles.csv"
ARTICLE_TITLES_PREPROCESS_OUT_FILE = "./out/article_titles_preprocess.csv"
ARTICLE_TITLES_CLUSTER_OUT_FILE = "./out/article_titles_cluster.xlsx"
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


def tokenize_text(text):
    return " ".join([item for item in jieba.cut(text) if item.strip() and item not in stop_words])


def remove_punctuation(text):
    punctuation = '!"#，。、$%&\'()*+,-./:;<=>?@[\\]^_`{|}~！!【】·•《》（）？▪●—…🎉🌷🌺🐸🐬🍀🙏👏—|丨‖→「」‘’'
    text = re.sub(r'[{}]+'.format(punctuation), '', text)
    return text

def text_to_tfidf_matrix(texts):
    tokenized_texts = [tokenize_text(remove_punctuation(text)) for text in texts]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(tokenized_texts)
    return tfidf_matrix

def cluster_texts(tfidf_matrix, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(tfidf_matrix)
    return kmeans.labels_

def extract_article_title():
    files_1 = [file for file in os.listdir(BAILIDUJUAN_1_OUT_PATH) if "html" in file]
    files_2 = [file for file in os.listdir(BAILIDUJUAN_2_OUT_PATH) if "html" in file]
    # use set remove duplicate item
    files = sorted(list(set(files_1 + files_2)))
    preprocess_files = [tokenize_text(remove_punctuation(file[file.find(']'):].split(".html")[0])) for file in files]
    df = pd.DataFrame({"article_title": files, "preprocess_title": preprocess_files})
    df.to_csv(ARTICLE_TITLES_OUT_FILE, index=False, encoding="utf-8")
    print("save {} successfully!".format(ARTICLE_TITLES_OUT_FILE))

    df = pd.read_csv(ARTICLE_TITLES_OUT_FILE, encoding="utf-8")
    texts = df["preprocess_title"].tolist()
    n_clusters = 100
    tfidf_matrix = text_to_tfidf_matrix(texts)
    labels = cluster_texts(tfidf_matrix, n_clusters)
    clusters = []
    for i, label in enumerate(labels):
        clusters.append(label)
    df["label"] = clusters
    output_filename = ARTICLE_TITLES_CLUSTER_OUT_FILE.replace(".xlsx", "_" + str(n_clusters) + ".xlsx")
    df.to_excel(output_filename, index=False)
    print("save {} successfully!".format(output_filename))

def filter_cluster():
    filter_keywords = ["疫", "调研", "法", "百里杜鹃管理区", "游戏", "资讯", "考试", "讲话", "天气", "科普"]
    cluster_base_filename = "./out/article_titles_cluster_20.xlsx"
    df = pd.read_excel(cluster_base_filename)
    print("before filter {} item".format(len(df['article_title'])))
    article_titles = []
    preprocess_titles = []
    labels = []
    for i in range(len(df['article_title'])):
        article_title = df['article_title'][i]
        preprocess_title = df['preprocess_title'][i]
        label = df['label'][i]
        if label == 1 or label == 11 or label == 16:
            continue
        is_filter = False
        for word in filter_keywords:
            if word in article_title:
                is_filter = True
                break
        if is_filter:
            continue
        article_titles.append(article_title)
        preprocess_titles.append(preprocess_title)
        labels.append(label)
    print("after filter {} item".format(len(article_titles)))
    odf = pd.DataFrame({"article_title": article_titles, "preprocess_title": preprocess_titles, "label": labels})
    output_filename = cluster_base_filename.replace(".xlsx", "_filtered.xlsx")
    odf.to_excel(output_filename, index=False)
    print("save {} successfully!".format(output_filename))


if __name__ == "__main__":
    # extract_article_title()
    filter_cluster()
    pass
