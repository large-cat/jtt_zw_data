find_article_num_path = [".*?（(.*?)〔(.*?)〕(.*?号)）",
                         ".*?（(.*?)﹝(.*?)〕(.*?号)）",
                         ".*?（(.*?)﹝(.*?)﹞(.*?号)）",
                         ".*?\((.*?)﹝(.*?)﹞(.*?号)\)",
                         ".*?（(.*?)〔(.*?)﹞(.*?号)）",
                         ".*?\((.*?)〔(.*?)〕(.*?号)\)",
                         ".*?（(.*?)\[(.*?)\](.*?号)）",
                         ".*?\((.*?)\[(.*?)\](.*?号)\)",
                         ".*?(黔.*?)〔(.*?)〕(.*?号)",
                         ".*?(黔.*?)（(.*?)）(.*?号)",
                         ".*?(黔.*?)\((.*?)\)(.*?号)",]

form_list = ["通知", "意见", "批复", "建议", "决定", "函", "规范性文件"]

article_class_wrong_path = [".*\((.*)", ".*（(.*)"]
