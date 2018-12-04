import pymssql as mssql
import pymysql as mysql
import json


def relink(n):  # n=数据库名称
    """读取数据库连接属性 返回连接属性自定a[n]"""
    with open('links.json', 'rb') as f:
        a = json.load(f)
        return a[n]


def dblink(lk, sqltxt, lx, intxt=''):
    """根据sql返回查询"""
    with open('./appmodel/links.json', 'rb') as f:
        a = json.load(f)
    link = a[lk]
    if link['lx'] == 'mssql':
        con = mssql.connect(link['host'], link['user'], link['pw'], link['db'], as_dict=True)
        cur = con.cursor()
    else:
        con = mysql.connect(link['host'], link['user'], link['pw'], link['db'])
        cur = con.cursor(mysql.cursors.DictCursor)
    if lx == 's':
        # 如果为查询请求
        cur.execute(sqltxt)
        rows = cur.fetchall()
        return rows
    elif lx == 'e':
        # 如果为编辑请求
        cur.execute(sqltxt)
        con.commit()
        return 'ok'
    elif lx == 'i':
        # 如果为插入请求
        # print(sqltxt)
        # print(intxt)
        cur.executemany(sqltxt, intxt)
        con.commit()
        return 'ok'
    cur.close()
    con.close()


def runsql(linktxt, sqlf):  # linktxt=连接名称；sqlf=sql文件路径
    """连接数据库执行sql文件"""
    con = mssql.connect(linktxt['host'], linktxt['user'], linktxt['pw'], linktxt['db'])
    cur = con.cursor()
    sql_file = sqlf
    sql = ""
    with open(sql_file, 'r', encoding='gbk') as f:
        # 读取sql并转为gbk编码
        for each_line in f:
            sql += each_line
    print(sql)
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()
