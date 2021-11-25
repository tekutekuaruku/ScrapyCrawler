from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import glob
from parser_option import get_arg
from utils import excel_to_csv
from settings import *

if __name__ == '__main__':
    args = get_arg()
    spider_name = 'MultiplePages' if args.follow else 'SinglePage'
    origin_pathes = glob.glob(ORIGIN_PATH)
    name_path = glob.glob(NAME_PATH)
    name_path = name_path[0]

    for origin_path in origin_pathes:
        print('-' * 10)
        print("[INFO]ファイル：{}の処理を開始します".format(origin_path))

        #check xlsx or csv or else
        if origin_path.endswith(".xlsx"):
            origin_path = excel_to_csv(origin_path)
        elif not origin_path.endswith(".csv"):
            print("[Error]ファイルの拡張子がxlsxまたはcsvであることを確認してください")
            continue

        origin_dir, origin_file = os.path.split(origin_path)
        html_path = os.path.join(HTML_DIR, origin_file.replace('.csv', '_html.csv'))

        #scrapy main process
        if os.path.isfile(html_path):
            print("[INFO]htmlファイルが既に存在するのでスクレイピング作業はスキップします")
        else:
            settings = get_project_settings()
            settings.set('FEED_FORMAT', 'csv')
            settings.set('FEED_URI', html_path)
            process = CrawlerProcess(settings)
            process.crawl(
                spider_name, origin_path=origin_path, name_path=name_path,
                ataglength_limit=A_TAG_LENGTH_LIMIT, path_pattern_path = PATH_PATTERN_PATH,
                txt_anchor_path = TXT_ANCHOR_PATH
            )
            process.start() # the script will block here until the crawling is finished