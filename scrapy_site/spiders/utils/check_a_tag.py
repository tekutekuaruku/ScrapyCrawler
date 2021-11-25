import re
import copy

from .utils import csv_to_dict

class a_tag_checker():

    def __init__(self, a_tags='', response_url='', txt_anchor_path='', path_pattern_path='') -> None:
        self.a_tags = a_tags
        self.response_url = response_url
        self.txt_anchors = csv_to_dict(txt_anchor_path)
        self.path_patterns = csv_to_dict(path_pattern_path)

    def a_tag_checker(self):
        #read txt anchor and rank

        for txt_anchor in self.txt_anchors:
            #Check the number of appearances of text anchors
            hit_tags, text_cnt = self.count_txt_anchor_appearance(txt_anchor['txt'])

            #Text anchor appears once
            if text_cnt == 1:
                url = self.appearance_once(hit_tags)
                if url:
                    return url

            #Text anchor appears more than once
            if text_cnt > 1:
                url = self.appearance_more_than_once(hit_tags)
                if url:
                    return url

            #img process logic
            url = self.process_img_anchor(txt_anchor['txt'])
            if url:
                return url
            url = ""
        return url

    def count_txt_anchor_appearance(self, txt_anchor):
        text_cnt = 0
        hit_tags = []
        for a_tag in self.a_tags:
            text = re.sub("\s", "", a_tag.text)
            if txt_anchor in text:
                text_cnt += 1
                hit_tags.append(a_tag)
        return hit_tags, text_cnt

    def appearance_once(self, hit_tags):
        search_obj = re.search('href=".*?"', str(hit_tags[0]))
        if search_obj:
            url = self.url_checker(search_obj.group(0))
            return url
        else:
            return ""

    def appearance_more_than_once(self, hit_tags):
        for hit_tag in hit_tags:
            for path_pattern in self.path_patterns:
                search_obj = re.search('href=".*?{}.*?"'.format(path_pattern['pattern']), str(hit_tag))
                if search_obj:
                    url = self.url_checker(search_obj.group(0))
                    return url
            #Logic to adopt the first one(There is room for improvement)
            search_obj = re.search('href=".*?"', str(hit_tags[0]))
            if search_obj:
                url = self.url_checker(search_obj.group(0))
                return url
        return ""

    def process_img_anchor(self, txt_anchor):
        for a_tag in self.a_tags:
            for img in a_tag.select('a img'):
                alt=img.attrs.get('alt', 'None')
                if not (alt == 'None'):
                    if txt_anchor in alt:
                        search_obj = re.search('href=".*?"', str(a_tag))
                        if search_obj:
                            url = self.url_checker(search_obj.group(0))
                            return url
        return ""

    def url_checker(self, hit_obj):
        response_url = self.response_url
        if not str(response_url).endswith('/'):
            response_url = str(response_url) + '/'
        hit_path = copy.deepcopy(hit_obj)
        url_path = hit_path.replace('"', '').replace('href=','')
        if 'http' in url_path:
            url = url_path.lstrip()
        else:
            if re.search(r'../*', url_path):
                url_path = url_path.replace(r"../", "")
                split_response_url = [i for i in re.split(r'/',response_url) if i != '']
                if len(split_response_url) > 2:
                    root_url = split_response_url[0] + r"//" + split_response_url[1] + r"/"
                    url = root_url + url_path.lstrip("/")
                else:
                    url = response_url + url_path.lstrip("/")
            else:
                if url_path.startswith(r'.'):
                    url_path = copy.deepcopy(url_path[1:])
                url =  response_url + url_path.lstrip("/")
        return url

    def eliminate_atag_duplication(self):
        new_a_tags = []
        for a_tag in self.a_tags:
            search_obj = re.search('href=".*?"', str(a_tag))
            if search_obj:
                hit_path = copy.deepcopy(search_obj.group(0))
                url = hit_path.replace('"', '').replace('href=','')
                if "http" in url:
                    if self.response_url == url:
                        continue
                else:
                    split_resurl_parts = [i for i in re.split(r'/',self.response_url) if i != '']
                    split_url = [i for i in re.split(r'/',url) if i != '']
                    if split_url and split_resurl_parts:
                        if split_resurl_parts[-1] == split_url[-1]:
                            continue
                new_a_tags.append(a_tag)
        return new_a_tags
