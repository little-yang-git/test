import json
import time
import hashlib
import requests
import sys
import pymssql as mssql
import pymysql as mysql


class DBlink(object):
    def __init__(self, link):
        self.link = link
        self.zt = str(self.__run())

    def __enter__(self):
        if self.zt[-2:] == 'OK':
            # self.__run()
            return self.cur, self.zt, True
        else:
            return self.zt, self.zt, False

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.zt[-2:] == 'OK':
            self.cur.close()
            self.con.close()

    def __run(self):
        try:
            if self.link['lx'] == 'mssql':
                self.con = mssql.connect(self.link['host'], self.link['user'],
                                         self.link['pw'], self.link['db'])
                self.cur = self.con.cursor(as_dict=True)
                return 'Mssql is OK'
            elif self.link['lx'] == 'mysql':
                self.con = mysql.connect(self.link['host'], self.link['user'],
                                         self.link['pw'], self.link['db'])
                self.cur = self.con.cursor(mysql.cursors.DictCursor)
                return 'Mysql is OK'
            else:
                return 'Link is Nothing'
        except Exception as e:
            return e


class LinkDb(object):

    # __slots__ = ('text', 'lx')

    def __init__(self, lk, sqlpath='./appmodel/links.json'):
        self.__lk = lk
        self.__sqlpath = sqlpath
        self.__relink()

    def __relink(self):  # n=数据库名称
        """读取数据库连接属性 返回连接属性自定a[n]"""
        with open(self.__sqlpath, 'rb') as f:
            lt = json.load(f)
            self.link = lt[self.__lk] if self.__lk in lt else {'lx': None}

    def get(self):
        with DBlink(self.link) as f:
            return f

    def select(self, sqltxt):
        with DBlink(self.link) as f:
            if f[-1] is True:
                try:
                    f[0].execute(sqltxt)
                    rows = f[0].fetchall()
                    return rows
                except Exception as e:
                    return str(e)
            else:
                return f

    def edit(self, sqltxt):
        with DBlink(self.link) as f:
            if f[-1] is True:
                try:
                    f[0].execute(sqltxt)
                    f[0].commit()
                    return 'Edit is OK'
                except Exception as e:
                    # f[0].rollback()
                    return str(e)
            else:
                return f

    def insert(self, sqltxt, intxt):
        with DBlink(self.link) as f:
            if f[-1] is True:
                try:
                    f[0].executemany(sqltxt, intxt)
                    f[0].commit()
                    return 'Insert is OK'
                except Exception as e:
                    # f[0].rollback()
                    return str(e)
            else:
                return f


class LinkApi(object):
    def __init__(self):
        self.__test = {'method': 'prm.goods.inv.get', 'page': '1', 'store_code': '001', 'page_size': '1'}

    def urlsign(self, data):
        # 拼合post；sign数据
        a_url = "http://openapi.baotayun.com/openapi/webefast/web/?app_act=openapi/router"
        a_data = {'method': data['method'],
                  'format': 'json',
                  'key': "bfd7910d15467517613d9661835afc41",
                  'v': '2.0',
                  'sign_method': 'md5',
                  'timestamp': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                  'page': data['page'],
                  'store_code': data['store_code'],
                  'page_size': data['page_size']}
        # 基础数据
        signtxt = ''.join([k + str(v) for k, v in sorted(a_data.items())])
        # 拼合data
        sign = hashlib.md5(signtxt.encode(encoding='UTF-8')).hexdigest().upper()
        # 生成sign
        url = a_url + ''.join(['&' + k + '=' + str(v) for k, v in a_data.items()]) + 'sign=' + sign
        # 生成url
        a_data['sign'] = sign
        return {'url': url, 'data': a_data}

    def run(self):
        a = self.__test
        a['a'] = '1'
        b = self.urlsign(a)
        return b



# def runapi(dtxt, page=1, pages=None):
#     # api访问主程序 dtxt=访问参数；page=开始页数；pages=返回页数
#     d = dtxt
#     p = page
#     ps = page + 3
#     rall = []
#     while p <= ps:
#         d['page'] = p
#         dout = urlsign(d)
#         # 解析访问参数
#         r = requests.post(dout['url'], dout['data'])
#         # api请求
#         if r.status_code != 200:
#             print('连接错误！')
#             sys.exit()
#         # else:
#         #     print(dout['data'])
#         data = r.json()
#         # 生产字典输出到data
#         if p == page:
#             # 如果为首次循环
#             pagec = data['data']['filter'].get('page_count')
#             # 获取总页数
#             ps = pages + page - 1 if pages and pages + page - 1 <= pagec else pagec
#             # 如果设置返回页数<=总页数
#             print(pagec)
#             # 计算共多少页
#         rall += (api_kwcf(data))
#         # 将每页数据汇总
#         print(p)
#         # 打印页数
#         # time.sleep(1)
#         # 等待
#         p += 1
#     return rall
#
#
# def api_kwcf(data):
#     # 拆分商品资料字典
#     z = []
#     lx = ['goods_code', 'sku', 'barcode', 'num', 'shelf_list']
#     # 在字典中需要查找的key值
#     jd = data['data']['data']
#     # 截取商品数据字典
#     for i in range(len(jd) - 1, -1, -1):
#         # 倒序遍历商品数据字典
#         u = {}
#         di = jd.pop(i)
#         for lxt in lx:
#             u[lxt] = int(di.get(lxt)) if lxt == 'num' else di.get(lxt)
#             # 如果key为num，转换为数值型
#         # u['shelf_list'] = u['shelf_list'][0]['shelf'][0]['shelf_code'] if u['shelf_list'] else None
#         u['shelf_list'] = ''.join([i['shelf_code'] + ';' for i in u['shelf_list'][0]['shelf']])[:-1] \
#             if u['shelf_list'] else None
#         # ------ 库位字典格式
#         # a = {"shelf_list": [
#         #     {
#         #         "store_code": "001",
#         #         "shelf": [
#         #             {
#         #                 "shelf_code": "D03L05",
#         #                 "shelf_name": "D03L05"
#         #             },
#         #             {
#         #                 "shelf_code": "D07L03",
#         #                 "shelf_name": "D07L03"
#         #             },
#         #             {
#         #                 "shelf_code": "D07R05",
#         #                 "shelf_name": "D07R05"
#         #             },
#         #             {
#         #                 "shelf_code": "S03R05",
#         #                 "shelf_name": "S03R05"
#         #             }]
#         #     }
#         # ]}
#         # ------ 如果有库位信息保存，否则返回None
#         uu = list(u.values())
#         # 将字典拼合为list
#         cs = uu.pop(1)
#         # 提取sku字段
#         uu.extend([cs[-4:-2], cs[-2:]])
#         # 截取sku中，色号尺码号部分拆分字段
#         uu = tuple(uu)
#         # 转换为元组
#         z.append(uu)
#     return z
#
#
# def runapi(dtxt, page=1, pages=None):
#     # api访问主程序 dtxt=访问参数；page=开始页数；pages=返回页数
#     d = dtxt
#     p = page
#     ps = page + 3
#     rall = []
#     while p <= ps:
#         d['page'] = p
#         dout = urlsign(d)
#         # 解析访问参数
#         r = requests.post(dout['url'], dout['data'])
#         # api请求
#         if r.status_code != 200:
#             print('连接错误！')
#             sys.exit()
#         # else:
#         #     print(dout['data'])
#         data = r.json()
#         # 生产字典输出到data
#         if p == page:
#             # 如果为首次循环
#             pagec = data['data']['filter'].get('page_count')
#             # 获取总页数
#             ps = pages + page - 1 if pages and pages + page - 1 <= pagec else pagec
#             # 如果设置返回页数<=总页数
#             print(pagec)
#             # 计算共多少页
#         rall += (api_kwcf(data))
#         # 将每页数据汇总
#         print(p)
#         # 打印页数
#         # time.sleep(1)
#         # 等待
#         p += 1
#     return rall
