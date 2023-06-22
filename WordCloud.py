#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# File Name    : WordCloud.py
# Author       : SangYu
# Email        : sangyu.code@gmail.com
# Created Time : 2023年06月22日 星期四 11时13分27秒
# Description  : generate word cloud picture
"""

import jieba
import wordcloud

FONT_PATH = '/usr/share/fonts/truetype/sim/simfang.ttf'

def generate_wordcloud(file_path, out_path):
    word_frequency = {}
    segment = []
    with open(file_path,"r",encoding="utf-8")as f_chat:
        for line in f_chat:
            segs = jieba.cut(line.strip())
            for word in segs:
                if word not in word_frequency:
                    word_frequency[word] = 1
                else:
                    word_frequency[word] += 1
                segment.append(word)
    for k,v in sorted(word_frequency.items(),key=lambda x:x[1],reverse=True)[:10]:
        print(k+"--"+str(v))

    # generate wordcloud picture
    txt = " ".join(segment)
    width = 1000
    height = 700
    background_color = 'white'
    
    w = wordcloud.WordCloud(font_path=FONT_PATH, width=width, height=height, background_color=background_color)
    w.generate(txt)
    w.to_file(out_path)


if __name__ == "__main__":
    test_file_path = "test_file.txt"
    out_path = "test_wordcloud.png"
    generate_wordcloud(test_file_path,out_path)
    pass

