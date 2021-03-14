from pyspider.libs.base_handler import *
from re import match
from time import sleep

from config import find_article_num_path, form_list, article_class_wrong_path


url_list = [
    "http://www.guizhou.gov.cn/xwdt/dt_22/df/gy/202102/t20210208_66716800.html",
    "http://www.guizhou.gov.cn/xwdt/dt_22/df/zy/202102/t20210205_66690793.html",
    "http://www.guizhou.gov.cn/xwdt/dt_22/df/lps/202102/t20210208_66716741.html",
    "http://www.guizhou.gov.cn/xwdt/dt_22/df/as/202102/t20210205_66690982.html",
    "http://www.guizhou.gov.cn/xwdt/dt_22/df/bj/202102/t20210205_66691035.html",
    "http://www.guizhou.gov.cn/xwdt/dt_22/df/tr/202102/t20210207_66705831.html",
    "http://www.guizhou.gov.cn/xwdt/dt_22/df/qdn/202102/t20210208_66716611.html",
    "http://www.guizhou.gov.cn/xwdt/dt_22/df/qn/202102/t20210208_66716579.html",
    "http://www.guizhou.gov.cn/xwdt/dt_22/df/qxn/202102/t20210205_66691308.html",
    "http://www.guizhou.gov.cn/xwdt/dt_22/df/gaxq/202102/t20210205_66691393.html",
]


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        for url in url_list:
            self.crawl(url, callback=self.detail_page, fetch_type='js')
            sleep(10)


    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page, fetch_type='js')

    @config(priority=2)
    def detail_page(self, response):
        next_page_tags = response.doc(".nextpage a").items()

        for next_page in next_page_tags:
            local_url = next_page.attr.href

            # print("next page: ", local_url)
            if local_url.startswith('http'):
                self.crawl(local_url, callback=self.detail_page, fetch_type='js')

        return self.analysis_page(response)

    @staticmethod
    def analysis_page(response):
        # print("analysis start")
        info_table = response.doc('tbody')
        tds = []

        article_form = None
        article_type = None
        article_info_class = "新闻"
        mechanism = None
        article_year = None
        article_class = None
        index_num = None
        date = None
        title = response.doc('title').text()

        article_class = list(response.doc('.CurrChnlCls').items())[2].attr("title")

        article_ly = response.doc('.Article_ly span').items()

        # analysis article_ly tag
        for span in article_ly:
            tmp_text = span.text()
            # print(tmp_text)

            if match(".*?文章来源.*?", tmp_text):
                text_has_js = match(".*}(.*)", tmp_text)

                if text_has_js:
                    tmp_text = "".join(text_has_js.groups())

                tmp_text = tmp_text.replace("文章来源", "")
                tmp_text = tmp_text.replace(":", "").replace("：", "")

                if len(tmp_text) > 50:
                    tmp_text_split = tmp_text.split()

                    if len(tmp_text) > 2:
                        tmp_text = " ".join(tmp_text_split[0:2])

                    else:
                        tmp_text = tmp_text[0:50]

                mechanism = tmp_text

            elif match(".*?发布时间.*?", tmp_text):
                date = match(".*?(.{4}-.{1,2}-.{1,2}).*?", tmp_text).groups()[0]
                article_year = date.split('-')[0]
                # date = tmp_text

        data = {
            "url": response.url,
            "index_num": index_num,
            "date": date,
            "mechanism": mechanism,
            "name": title,

            "info_class": article_info_class,
            "type": article_type,
            "form": article_form,

            "article_content": response.doc('.zw-con').text(),
            "article_class": article_class,
            "article_year": article_year,
            "article_num": None,
            # "tds": tds,

        }
        # print(data)
        return data
