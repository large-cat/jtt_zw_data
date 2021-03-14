#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2021-01-28 21:52:40
# Project: js_test

from pyspider.libs.base_handler import *
from re import match


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=60)
    def on_start(self):
        self.crawl('http://www.guizhou.gov.cn/zwgk/zcfg/szfwj_8191/szfl_8192/', callback=self.chek_left_nav,
                   fetch_type='js')

    def index_page(self, response):
        for each in response.doc('.right-list-box a').items():
            self.crawl(each.attr.href, callback=self.detail_page, fetch_type='js')

        next_pages = response.doc('.up').items()

        for next_page in next_pages:
            if next_page.text() == '下一页':
                self.crawl(next_page.attr.href, callback=self.index_page, fetch_type='js')

    @config(priority=2)
    def detail_page(self, response):
        info_table = response.doc('tbody')
        tds = []

        i = 0
        for td in response.doc('tbody td').items():
            if i % 2 == 0:
                tds.append(td.find('strong').text().replace("\n", "").replace("\t", ""))

            elif i == 3:
                info_class = []
                td = response.doc('td.xxfl-1 em').items()

                for em in td:
                    info_class.append(em.text().replace("\n", "").replace("\t", ""))

                tds.append(info_class)

            elif i == 5:
                tmp_str_result = td.text().replace("\n", "").replace("\t", "")
                r_str = match(".*}(.*?)$", tmp_str_result).groups()[0]

                tds.append(r_str)

            else:
                tds.append(td.text().replace("\n", "").replace("\t", ""))

            i += 1

        title_ansys = match(".*的(.*)\((.*?)〔(.*?)〕(.*?号)\)$", response.doc('title').text())

        if title_ansys is None:
            title_ansys = match(".*的(.*)（(.*?)〔(.*?)〕(.*?号)）$", response.doc('title').text())

        article_form = None
        article_type = None
        article_info_class = None

        if title_ansys:
            title_ansys = title_ansys.groups()

            article_class = title_ansys[1]
            article_year = title_ansys[2]
            article_num = title_ansys[3]

            article_form = title_ansys[0]

        else:
            article_class = "省政府令"
            article_year = tds[7].split('-')

            if len(article_year) > 0:
                article_year = article_year[0]
            else:
                article_year = None

            article_num = match(".*（(.*?)）", response.doc('title').text())

            if article_num is None:
                article_num = match(".*\((.*?)\)", response.doc('title').text())

                if article_num is not None:
                    article_num = article_num.groups()[0]
            else:
                article_num = article_num.groups()

        length = len(tds[3])

        if length == 3:
            if not tds[3][2] == "":
                article_form = tds[3][2]

            if not tds[3][1] == "":
                article_type = tds[3][1]

            if not tds[3][0] == "":
                article_info_class = tds[3][0]

        elif length == 2:
            article_type = tds[3][1]
            article_info_class = tds[3][0]

        elif length == 1:
            article_info_class = tds[3][0]

        data = {
            "url": response.url,
            "index_num": tds[1],
            "date": tds[7],
            "mechanism": tds[5],
            "name": tds[13],

            "info_class": article_info_class,
            "type": article_type,
            "form": article_form,

            "article_content": response.doc('.zw-con').text(),
            "article_class": article_class,
            "article_year": article_year,
            "article_num": article_num,
            # "tds": tds,

        }

        return data

    @config(priority=2)
    def chek_left_nav(self, response):
        i = 0
        for each in response.doc('.left-nav a').items():
            self.crawl(each.attr.href, callback=self.index_page, fetch_type='js')
            i += 1
            if i == 7:
                break
