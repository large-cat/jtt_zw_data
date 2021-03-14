import sqlite3
from pyspider.result import ResultWorker
from time import time
from threading import Lock

sql_lock = Lock()
filed_list = ['url', 'article_class', 'article_content', 'article_num', 'article_year', 'date', 'form', 'index_num',
              'info_class', 'mechanism', 'name', 'type']


class JTTResultWorker(ResultWorker):
    res_db_conn = sqlite3.connect('./zw.db')
    jtt_cur = res_db_conn.cursor()

    # last_commit_time = time()

    def on_result(self, task, result):
        # assert task['taskid']
        # assert task['project']
        # assert task['url']
        # assert result
        #
        # for filed in filed_list:
        #     assert result[filed]

        sql_command_template = """
            insert into dt_article ({})
            values ({});
        """

        print('\n'*2)
        print("-"*20)

        print('')
        print("程序获取到数据:")

        for filed in filed_list:
            if filed in ['article_content']:
                print('\n')
                print(filed + ':\n', result[filed][:100] + "...")
                print('\n')
                continue

            try:
                print(filed + ':', result[filed])
            except Exception as e:
                print(e)

        print("-"*20)
        print('\n'*3)

        # with sql_lock:
        current_sql_command = ''

        try:
            for filed in filed_list:
                if result[filed] is not None:
                    result[filed] = result[filed].replace('"', '”').replace("'", '”')

            current_sql_command = sql_command_template.format(
                ','.join(['`' + filed + '`' for filed in filed_list]),
                ','.join(["'" + result[filed] + "'" if result[filed] is not None else 'null' for filed in filed_list])
            )

        except Exception as e:
            print(e)
            print("error")

        # print(current_sql_command)

        if not current_sql_command == '':
            sql_msg = self.jtt_cur.execute(current_sql_command)

        # for msg in sql_msg:
        #     print("sql return msg: ", msg)

        # if time() - self.last_commit_time > 5:

        self.res_db_conn.commit()
        # self.last_commit_time = time()

        # your processing code goes here
