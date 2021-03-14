from pyspider.libs.base_handler import *
from re import match

from config import find_article_num_path, form_list, article_class_wrong_path


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.guizhou.gov.cn/zwgk/zcfg/szfwj_8191/qff_8193/202102/t20210222_66804235.html',
                   callback=self.detail_page, fetch_type='js')

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
        article_info_class = "部门规范性文件"
        mechanism = "中国省委"
        article_year = None
        article_class = None
        index_num = None
        date = None
        title = response.doc('title').text()

        # find article form
        for form_name in form_list:
            matched = match(".*的" + form_name + ".*", title)

            if matched:
                article_form = form_name
                break

        # find table
        i = 0
        for td in response.doc('tbody td').items():
            if i % 2 == 0:
                tds.append(td.find('strong').text().replace("\n", "").replace("\t", ""))

            elif i == 1:
                index_num = td.text()

            elif i == 3:
                info_class = []
                td = response.doc('td.xxfl-1 em').items()

                j = 0
                for em in td:
                    j += 1
                    tmp_text = em.text().replace("\n", "").replace("\t", "")
                    info_class.append(tmp_text)

                    if j == 1:
                        article_type = tmp_text

                    elif j == 2:
                        article_info_class = tmp_text

                    elif j == 3:
                        article_form = tmp_text

                tds.append(info_class)

            elif i == 5:
                tmp_str_result = td.text().replace("\n", "").replace("\t", "")

                r_str = match(".*}(.*?)$", tmp_str_result)

                if r_str is not None:
                    r_str = r_str.groups()[0]
                else:
                    r_str = tmp_str_result

                tds.append(r_str)

            elif i == 7:
                date = td.text()

            else:
                tds.append(td.text().replace("\n", "").replace("\t", ""))

            i += 1

        # analysis title
        title_analysis = None

        for path in find_article_num_path:
            title_analysis = match(path, title)
            if title_analysis is not None:
                break

        if title_analysis:
            title_analysis = title_analysis.groups()

            article_class = title_analysis[0]

            for path in article_class_wrong_path:
                article_class_is_wrong = match(path, article_class)

                if article_class_is_wrong:
                    article_class = article_class_is_wrong.groups()[0]
                    # print("wrong to true: ", article_class)
                    break

            article_year = title_analysis[1]
            article_num = title_analysis[2]

        else:
            # get article num from content
            # print("span span: ", response.doc('.view p span span').text())
            for path in find_article_num_path:
                matched = match(path, '(' + response.doc('.view p span span').text() + ')')
                if matched:
                    result_groups = matched.groups()

                    article_class = result_groups[0]
                    article_year = result_groups[1]
                    article_num = result_groups[2]
                    break

            article_num = match(".*（(.*?)）", title)

            if article_num is not None:
                article_num = article_num.groups()[0]

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
                tmp_text = tmp_text.replace(":", "").replace("：", "").replace(" ", "")
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
            "article_num": article_num,
            # "tds": tds,

        }
        # print(data)
        return data
