import scrapy
from .utils.check_a_tag import a_tag_checker
from .utils.judge_page import judge_page
from .utils.utils import get_content, set_data, check_info_and_cnt, csv_to_dict
from scrapy_site.items import Page
from bs4 import BeautifulSoup
import glob

class MultiplePagesSpider(scrapy.Spider):

    name = 'MultiplePages'
    def __init__(self, origin_path="", name_path="", ataglength_limit=300, path_pattern_path = '', txt_anchor_path = '', *args, **kwargs):
        super(MultiplePagesSpider, self).__init__(*args, **kwargs)
        self.start_urls = set_data(2, origin_path)#start_urls is process target urls
        self.index_list = set_data(0, origin_path)
        self.meta_list = set_data(1, origin_path)
        self.url_list = set_data(2, origin_path)
        self.name_dict = csv_to_dict(name_path)
        self.path_pattern_path = path_pattern_path
        self.txt_anchor_path = txt_anchor_path
        self.ataglength_limit = ataglength_limit

    def parse(self, response):
        print('-' * 10)
        print("[INFO]URL : " + response.url)

        #Check the redirect URL
        if "redirect_urls" in response.meta:
            request_url = response.meta["redirect_urls"][0]
        else:
            request_url = response.request.url

        cnt, index, meta = check_info_and_cnt(request_url, self.index_list, self.meta_list, self.url_list)
        print("[INFO]{}目のデータ".format(str(cnt)))
        short_title, summary_content = get_content(response.text)
        html = response.text
        status = judge_page(response.text, self.name_dict)
        if status:
            yield Page(index = index, meta = meta, url=response.url, short_title=short_title, html=html, status=status, summary_content=summary_content)
        else:
            #Get individual page links from the company's top page
            soup = BeautifulSoup(response.text, 'lxml')
            a_tags = soup.find_all('a')
            if len(a_tags) > self.ataglength_limit:
                print("[INFO]a_tagが{}以上です".format(str(self.ataglength_limit)))
                yield Page(index = index, meta = meta, url=response.url, short_title=short_title, html=html, status="tag_first", summary_content=summary_content)
            else:
                Process = a_tag_checker(a_tags, response.url, self.txt_anchor_path, self.path_pattern_path)
                url = Process.a_tag_checker()
                if url:
                    print("[INFO]候補URLが見つかりました")
                    print("候補URLは <{}>です".format(url))
                    yield scrapy.Request(url, callback=self.parse_page, cb_kwargs = {'index':index,'meta':meta})
                else:
                    print("[INFO]候補URLは見つかりませんでした")
                    yield Page(index = index, meta = meta, url=response.url, short_title=short_title, html=html, status="nopage_first", summary_content=summary_content)

    def parse_page(self, response, index, meta):
        print("[INFO]URL : " + response.url)
        print("[INFO]{}は二階層目です".format(meta))
        status = judge_page(response.text, self.name_dict)
        short_title, summary_content = get_content(response.text)
        html = response.text
        if status:
            yield Page(index = index, meta = meta, url=response.url, short_title=short_title, html=html, status=status, summary_content=summary_content)
        else:
            soup = BeautifulSoup(response.text, 'lxml')
            a_tags = soup.find_all('a')
            if len(a_tags) > self.ataglength_limit:
                print("[INFO]a_tagが{}以上です".format(str(self.ataglength_limit)))
                yield Page(index = index, meta = meta, url=response.url, short_title=short_title, html=html, status="tag_second", summary_content=summary_content)
            else:
                #Remove duplicate a tag
                Process = a_tag_checker(a_tags, response.url, self.txt_anchor_path, self.path_pattern_path)
                a_tags = Process.eliminate_atag_duplication()
                Process = a_tag_checker(a_tags, response.url, self.txt_anchor_path, self.path_pattern_path)
                url = Process.a_tag_checker()
                if url:
                    print("[INFO]二階層目で候補URLが見つかりました")
                    print("候補URLは <{}>です".format(url))
                    yield scrapy.Request(url, callback=self.parse_second_page, cb_kwargs = {'index':index,'meta':meta})
                else:
                    print("[INFO]候補URLは見つかりませんでした(second)")
                    yield Page(index = index, meta = meta, url=response.url, short_title=short_title, html=html, status="nopage_second", summary_content=summary_content)

    def parse_second_page(self, response, index, meta):
        print("[INFO]URL : " + response.url)
        print("[INFO]{}は三階層目です".format(meta))
        short_title, summary_content = get_content(response.text)
        html = response.text
        status = judge_page(html, self.name_dict)
        if not status:
            status = "nopage_third"
        yield Page(index = index, meta = meta, url=response.url, short_title=short_title, html=html, status=status, summary_content=summary_content)