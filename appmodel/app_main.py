import json
import time
import datetime
import hashlib
import requests
import sys
import pymssql as mssql
import pymysql as mysql


def jsonfile(k, kk=None):  # n=数据库名称
    """读取数据库连接属性 返回连接属性自定a[n]"""
    with open(sys.path[0] + "/appmodel/links.json", 'rb') as f:
        lt = json.load(f)
        return lt[k][kk] if kk in lt[k] else None if kk else lt[k] if k in lt else None
        # if kk:
        #     return lt[k][kk] if kk in lt[k] else None
        # else:
        #     return lt[k] if k in lt else None


class DBlink(object):
    def __init__(self, link):
        self.link = link
        self.zt = str(self.__run())

    def __enter__(self):
        if self.zt[-2:] == 'OK':
            # self.__run()
            return self.cur, self.con, self.zt, True
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

    def __init__(self, lk):
        self.__lk = lk
        self.link = jsonfile('LinkDB', lk)

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
                    f[1].commit()
                    return 'Edit is OK'
                except Exception as e:
                    f[1].rollback()
                    return str(e)
            else:
                return f

    def insert(self, sqltxt, intxt):
        with DBlink(self.link) as f:
            if f[-1] is True:
                try:
                    f[0].executemany(sqltxt, intxt)
                    f[1].commit()
                    return 'Insert is OK'
                except Exception as e:
                    f[1].rollback()
                    return str(e)
            else:
                return f

    def runsql(self, sqlf):  # sqlf=sql文件路径
        """连接数据库执行sql文件"""
        sql_file = "/Volumes/web/TP/app/" + sqlf + ".sql"
        sql = ""
        with open(sql_file, 'r', encoding='gbk') as f:
            # 读取sql并转为gbk编码
            for each_line in f:
                sql += each_line
        with DBlink(self.link) as f:
            if f[-1] is True:
                try:
                    f[0].execute(sql)
                    f[1].commit()
                    return 'SqlFile is OK'
                except Exception as e:
                    f[1].rollback()
                    return str(e)


class LinkApi(object):
    def __init__(self):
        self.__test = {'method': 'prm.goods.inv.get', 'page': '1', 'store_code': '001', 'page_size': '1'}
        t = jsonfile('LinkApi')
        self.__url = t['url']
        self.__key = t['key']
        self.__runtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def urlsign(self, data):
        # 拼合post；sign数据
        a_url = self.__url
        a_data = data
        # 基础数据
        signtxt = ''.join([k + str(v) for k, v in sorted(a_data.items())])
        # 拼合data
        sign = hashlib.md5(signtxt.encode(encoding='UTF-8')).hexdigest().upper()
        # 生成sign
        url = a_url + ''.join(['&' + k + '=' + str(v) for k, v in a_data.items()]) + 'sign=' + sign
        # 生成url
        a_data['sign'] = sign
        return {'url': url, 'data': a_data}

    def __runapi(self, sign):
        r = requests.post(sign['url'], sign['data'])
        # api请求
        if r.status_code != 200:
            return False, '连接错误'
        else:
            a = r.json()
            if a['status'] == 1:
                return True, '连接正常' + "/" + a['message'], a
            else:
                return False, '连接正常' + "/" + a['message'], a
            # 生产字典输出到data

    def get(self, lx='test'):
        apitxt = jsonfile('LinkApi', lx)
        apitxt['key'] = self.__key
        apitxt['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        signtxt = self.urlsign(apitxt)
        apidata = self.__runapi(signtxt)
        if apidata[0]:
            return apidata
        else:
            return apidata

    def goods(self, page=None, pages=None, barcode=None, start_time=None, end_time=None, update='yes'):
        if update != 'no':
            d = LinkDb('GNet')
            if not d.get()[-1]: return d.get()
        ps = 2
        rall = []
        apitxt = jsonfile('LinkApi', 'goods')
        apitxt['key'] = self.__key
        if barcode: apitxt.update(barcode=barcode)
        if start_time:
            now = (datetime.datetime.now() + datetime.timedelta(days=int(start_time))).strftime("%Y-%m-%d %H:%M:%S")
            apitxt.update(start_time=now)
        else:
            if update == 'yes':
                rtime = d.select("SELECT MAX(etime) AS time FROM API_Kucun_Efast")
                if rtime[0]['time']:
                    apitxt.update(start_time=rtime[0]['time'].strftime("%Y-%m-%d %H:%M:%S"))
        if end_time:
            now = (datetime.datetime.now() + datetime.timedelta(days=int(end_time))).strftime("%Y-%m-%d %H:%M:%S")
            apitxt.update(end_time=now)
        if page and barcode is None and start_time is None and end_time is None:
            apitxt.update(page=page)
            p = page
        else:
            p = 1
        while p <= ps:
            apit = apitxt.copy()
            apit['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            apit['page'] = p
            signtxt = self.urlsign(apit)
            apidata = self.__runapi(signtxt)
            if not apidata[0]:
                if update == 'yes':
                    return '没有数据需要更新'
                else:
                    return apidata
            else:
                rall += (self.__goods_kwcf(apidata[-1]))
                # 将每页数据汇总
                if p == page or p == 1:
                    # 如果为首次循环
                    pagec = apidata[-1]['data']['filter'].get('page_count')
                    rowc = apidata[-1]['data']['filter'].get('record_count')
                    # 获取总页数
                    ps = pages + p - 1 if pages and pages + p - 1 <= pagec else pagec
                    # 如果设置返回页数<=总页数
                    print('共检索到%d页，%s条记录' % (pagec, rowc))
                    # 计算共多少页
                sys.stdout.write('\r')
                sys.stdout.write('检索到第%d页' % p)
                sys.stdout.flush()
                p += 1
        print('\n')
        if update == 'no':
            return True, rall
        elif update == 'all':
            sql = "insert into API_Kucun_Efast(SPDM,SPTM,COLOR_ID,SIZE_ID,SL,KW,etime) values(%s,%s,%s,%s,%s,%s,%s)"
            dtt = d.edit("delete from API_Kucun_Efast")
            itt = d.insert(sql, rall)
            return True, dtt, itt
        elif update == 'yes':
            sqlt = "insert into API_Kucun_Efast_T(SPDM,SPTM,COLOR_ID,SIZE_ID,SL,KW,etime) values(%s,%s,%s,%s,%s,%s,%s)"
            dttt = d.edit("delete from API_Kucun_Efast_T")
            ittt = d.insert(sqlt, rall)
            sf = d.runsql('API_Kucun_Efast')
            return True, dttt, ittt, sf

    def __goods_kwcf(self, data):
        # 拆分商品资料字典
        z = []
        lx = ['goods_code', 'sku', 'barcode', 'num', 'shelf_list']
        # 在字典中需要查找的key值
        jd = data['data']['data']
        # 截取商品数据字典
        for i in range(len(jd) - 1, -1, -1):
            # 倒序遍历商品数据字典
            u = {}
            di = jd.pop(i)
            for lxt in lx:
                u[lxt] = int(di.get(lxt)) if lxt == 'num' else di.get(lxt)
                # 如果key为num，转换为数值型
            # u['shelf_list'] = u['shelf_list'][0]['shelf'][0]['shelf_code'] if u['shelf_list'] else None
            u['shelf_list'] = ''.join([i['shelf_code'] + ';' for i in u['shelf_list'][0]['shelf']])[:-1] \
                if u['shelf_list'] else None
            # ------ 如果有库位信息保存，否则返回None
            uu = list(u.values())
            # 将字典拼合为list
            cs = uu.pop(1)
            # 提取sku字段
            uu.insert(2, cs[-4:-2])
            uu.insert(3, cs[-2:])
            uu.append(self.__runtime)
            # 截取sku中，色号尺码号部分拆分字段
            uu = tuple(uu)
            # 转换为元组
            z.append(uu)
        return z

    def run(self):
        a = self.__test
        a['a'] = '1'
        b = self.urlsign(a)
        return b
