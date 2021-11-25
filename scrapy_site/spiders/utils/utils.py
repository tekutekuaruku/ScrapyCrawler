import logging
from typing import Tuple
import lxml.html
import readability
import pandas as pd
import re
import copy
import csv

#To prevent the readability-lxml log from being displayed in large numbers when Spider is executed, making the log difficult to read.
logging.getLogger('readability.readability').setLevel(logging.WARNING)

def get_content(html: str) -> Tuple[str, str]:
    document = readability.Document(html)
    content_html = document.summary()
    content_text = lxml.html.fromstring(content_html).text_content().strip()
    short_title = document.short_title()
    return short_title, content_text

def set_data(row_num, path):
    row_data = []
    origin_list = pd.read_csv(path, encoding="utf_8").values.tolist()
    i = 0
    while i < len(origin_list):
        row_data.append('')
        row_data[i] = copy.deepcopy(re.sub(r"\s", "", str(origin_list[i][row_num])))
        i += 1
    return row_data

def check_info_and_cnt(response_url, index_list, meta_list, url_list):
    cnt = -1
    if not response_url:
        print("[ERROR]response_urlが存在しません")
        return
    for url in url_list:
        cnt += 1
        if url == response_url:
            break
    if cnt > (len(url_list) - 1):
        print("[ERROR]CNTでエラーが発生しています")
        return

    index = copy.deepcopy(str(index_list[cnt]))
    meta = copy.deepcopy(meta_list[cnt])
    return cnt + 1, index, meta

def csv_to_dict(path):
    dictionary = []
    with open(path, 'r',encoding="utf-8") as f:
        for row in csv.DictReader(f):
            dictionary.append(row)
        return dictionary