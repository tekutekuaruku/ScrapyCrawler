import scrapy
from .utils.judge_page import judge_page
from .utils.utils import get_content, set_data, check_info_and_cnt, csv_to_dict
from scrapy_site.items import Page

class SinglePageSpider(scrapy.Spider):
    name = 'SinglePage'
    def __init__(self, origin_path="", name_path="", ataglength_limit=300, path_pattern_path = '', txt_anchor_path = '', *args, **kwargs):
        super(SinglePageSpider, self).__init__(*args, **kwargs)
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
        print("[INFO]{}個目のデータです".format(str(cnt)))
        if response.text:
            short_title, summary_content = get_content(response.text)
            html = response.text
            status = judge_page(response.text, self.name_dict)
        else:
            short_title, summary_content, html = ""
            status = "nopage_first"
        yield Page(index = index, meta = meta, url=response.url, short_title=short_title, html=html, status=status, summary_content=summary_content)