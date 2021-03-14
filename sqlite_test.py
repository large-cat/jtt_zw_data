import sqlite3


res_db_conn = sqlite3.connect('./zw.db')
jtt_cur = res_db_conn.cursor()

# sql_command = """
#             insert into test (`url`)
#             values ({});
#         """
#
# sql_msg = jtt_cur.execute(sql_command.format('123'))
#
# print("sql return msg: ", sql_msg)
# # if time() - self.last_commit_time > 5:
#
# res_db_conn.commit()
