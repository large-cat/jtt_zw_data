from json import dump, load, loads
from re import match
import csv

import pymysql

con = pymysql.connect(user="root",
                      passwd="123",
                      db="search",
                      host="192.168.43.95",
                      local_infile=1)


# cur.execute("desc article;")

data = """insert into `article_test`(`url`,`article_class`,`article_content`,`article_num`,`article_year`,`date`,`form`,`index_num`,`info_class`,
`mechanism`,`name`,`type`) values """

csv_file = './zw_data_8.csv'

find_article_num_path = [".*（(.*?)〔(.*?)〕(.*?号)）",
                         ".*（(.*?)﹝(.*?)〕(.*?号)）",
                         ".*（(.*?)﹝(.*?)﹞(.*?号)）",
                         ".*\((.*?)﹝(.*?)﹞(.*?号)\)",
                         ".*（(.*?)〔(.*?)﹞(.*?号)）",
                         ".*\((.*?)〔(.*?)〕(.*?号)\)",
                         ".*（(.*?)\[(.*?)\](.*?号)）",
                         ".*\((.*?)\[(.*?)\](.*?号)\)",
                         ".*(黔.*?)〔(.*?)〕(.*?号)",
                         ".*(黔.*?)（(.*?)）(.*?号)",
                         ".*(黔.*?)\((.*?)\)(.*?号)",]

r = []
with open(csv_file, 'r') as f:
    reader = csv.reader(f)

    with con:
        with con.cursor() as cur:
            i = 0
            for row in reader:
                i += 1
                if i <= 3000:
                    continue

                if row[1] == "省政府令":
                    row[10].replace(" ", "").replace(" ", "")
                    # print(row[10])
                    is_re = False
                    for path in find_article_num_path:
                        tmp_article_num = match(path, row[10])
                        if tmp_article_num is not None:
                            tmp_article_num = tmp_article_num.groups()
                            # print("result: ", path, tmp_article_num)

                            row[1] = tmp_article_num[0]
                            row[3] = tmp_article_num[2]
                            row[4] = tmp_article_num[1]
                            is_re = True
                            break

                    tmp_res = ['.*?\((.*)']

                    for path in tmp_res:
                        tem_result = match(path, row[1])

                        if tem_result is not None:
                            # print(row[1])
                            row[1] = tem_result.groups()[0]

                    if not is_re:
                        print(row[1], row[3:5], row[10])

                for p in range(len(row)):
                    if row[p] == "":
                        row[p] = 'null'

                    row[p] = "'" + row[p] + "'"

                tmp_data = data + '(' + ','.join(row[:-2]) + ');'
                # print(tmp_data)
                cur.execute(tmp_data)
                r.append(row[0])
                if i > 3700:
                    break
        con.commit()
        print(len(set(r)), r[0])
