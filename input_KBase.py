# coding:utf-8
"""
把PostgreSQl中的字段值修改到KBase里面；
"""


from CNKI import KBase
import psycopg2


# 连接到一个给定的数据库
conn_pg = psycopg2.connect(database="cnki_009_govin_pro_ods", user="postgres", password="fj5722902", host="10.170.128.121", port="5432")
conn_kb = KBase.connect(host="192.168.106.49", port=4567, user="DBOWN", passwd="")
# tpiclient = KBase.TPIClient(conn_kb)
cur_pg = conn_pg.cursor()
# cur_kb = conn_kb.cursor()

# print('connection handle is:', conn_kb.hcon)  # connection handle is: 1025


cur_pg.execute("select * from dfjx7919 where 附件名称 = 'fff'")

row_pg = cur_pg.fetchall()
num = 0
for row in row_pg:
    num  = num + 1
    print(num, row[0])
    # cur_kb.execute("update dfjx7919 set URL = '' where 文件名 = %s", (row[0],))
    xml = str(row[37])
    # print(xml)
    xml = xml.replace("URL", "URLL")
    # print(xml)
    sql_kb = "update dfjx7919 set xml = r'%s' where title = '%s'" %(xml, row[0])
    print(sql_kb)
    cur_pg.execute(sql_kb)
    conn_pg.commit()
    # cur_kb.execute("""update dfjx7919 set XML字段 = '{0}' where 文件名 = {1}""", (xml, row[0],))
    break

# cur_kb.close()
# conn_kb.close()


# 关闭游标
cur_pg.close()

# 关闭数据库连接
conn_pg.close()
