import itchat
import psycopg2
from itchat.content import *



def insetpgsql(msg):
    ## 连接到一个给定的数据库
    conn_pg = psycopg2.connect(database="cnki_009_govin_pro_ods", user="postgres", password="fj5722902", host="10.170.128.121", port="5432")
    cur_pg = conn_pg.cursor()
    sql_pg = "INSERT INTO pyitchat VALUES ('{0}');".format(msg)
    print(sql_pg)
    cur_pg.execute(sql_pg)
    conn_pg.commit()
    ## 关闭游标
    cur_pg.close()
    ## 关闭数据库连接
    conn_pg.close()


#自动回复
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    print(msg)
    insetpgsql(msg["Text"])
    return "东小东回复数据:"+msg["Text"]

#登入
itchat.auto_login()
#保持运行
itchat.run()
