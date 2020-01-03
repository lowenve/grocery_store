from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from datetime import datetime
import time
import psycopg2
import poplib
import re


def insetpgsql(msg, subject):
    try:
        # 连接到一个给定的数据库
        conn_pg = psycopg2.connect(database="cnki_003_xinfang_pro", user="postgres", password="fj5722902", host="10.170.128.121", port="5432")
        cur_pg = conn_pg.cursor()
        sql_pg = "INSERT INTO petition_emaillinklist (msg, title) VALUES ('{0}', '{1}');".format(msg, subject)
        print(sql_pg)
        cur_pg.execute(sql_pg)
        conn_pg.commit()
        # 关闭游标
        cur_pg.close()
        # 关闭数据库连接
        conn_pg.close()
    except Exception:
        print("重复数据，插入失败～")


def find_url(string):
    # findall() 查找匹配正则表达式的字符串
    url = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', string)
    return url[0]


def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def print_info(msg, indent=0):
    if msg.get('To') != "root@loongtext.com":
        print("非法邮件～")
    else:
        subject = str()
        if indent == 0:
            for header in ['From', 'To', 'Subject']:
                value = msg.get(header, '')
                if value:
                    if header == 'Subject':
                        value = decode_str(value)
                        subject = decode_str(value)
                    else:
                        hdr, addr = parseaddr(value)
                        name = decode_str(hdr)
                        value = u'%s <%s>' % (name, addr)
                print('%s%s: %s' % ('  ' * indent, header, value))
        if (msg.is_multipart()):
            parts = msg.get_payload()
            for n, part in enumerate(parts):
                print('%spart %s' % ('  ' * indent, n))
                print('%s--------------------' % ('  ' * indent))
                print_info(part, indent + 1)
        else:
            content_type = msg.get_content_type()
            if content_type == 'text/plain' or content_type == 'text/html':
                content = msg.get_payload(decode=True)
                charset = guess_charset(msg)
                if charset:
                    content = content.decode(charset)
                print('%sText: %s' % ('  ' * indent, content + '...'))
                msg_url = content.split('\n')[0]
                # msg_url = find_url(content)
                print("URL:", msg_url)
                insetpgsql(msg=msg_url, subject=subject)
            else:
                print('%sAttachment: %s' % ('  ' * indent, content_type))


if __name__ == '__main__':
    # 输入邮件地址, 口令和POP3服务器地址:
    # email = input('Email: ')
    # password = input('Password: ')
    email = "lowenve@foxmail.com"
    password = "vqpfezncneetbfff"
    pop3_server = 'pop.'+email.split('@')[-1]
    while True:
        try:
            # 连接到POP3服务器:
            server = poplib.POP3(pop3_server)
            # 可以打开或关闭调试信息:
            server.set_debuglevel(1)
            # 可选:打印POP3服务器的欢迎文字:
            print(server.getwelcome().decode('utf-8'))
            # 身份认证:
            server.user(email)
            server.pass_(password)
            # stat()返回邮件数量和占用空间:
            print('Messages: %s. Size: %s' % server.stat())
            # list()返回所有邮件的编号:
            resp, mails, octets = server.list()
            # 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
            # print(mails)
            # 获取最新一封邮件, 注意索引号从1开始:
            index = len(mails)
            for i in range(index-20, index+1):
                print("邮件的ID = ", i)
                resp, lines, octets = server.retr(i)
                # lines存储了邮件的原始文本的每一行,
                # 可以获得整个邮件的原始文本:
                msg_content = b'\r\n'.join(lines).decode('utf-8', 'ignore')
                # 稍后解析出邮件:
                msg = Parser().parsestr(msg_content)
                print_info(msg)
                # 可以根据邮件索引号直接从服务器删除邮件:
                # server.dele(index)
            # 关闭连接:
            server.quit()

            print(datetime.now().strftime("%Y-%m-%d  %H:%M:%S"))
            time.sleep(600)
        except Exception as e:
            raise(e)
            print("正在长睡～")
            time.sleep(3600)
