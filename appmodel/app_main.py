import json
import time
import datetime
import hashlib
import requests
import sys
import pymssql as mssql
import pymysql as mysql
import os
from PIL import Image
import re
import shutil


def jsonfile(k, kk=None, kkk=None):  # n=数据库名称
    """读取数据库连接属性 返回连接属性自定a[n]"""
    with open(sys.path[0] + os.sep + "appmodel" + os.sep + "links.json", 'rb') as f:
        lt = json.load(f)
        if kk:
            if kkk:
                return lt[k][kk][kkk]
            else:
                return lt[k][kk]
        else:
            return lt[k]
        # return lt[k][kk] if kk in lt[k] else None if kk else lt[k] if k in lt else None
        # if kk:
        #     return lt[k][kk] if kk in lt[k] else None
        # else:
        #     return lt[k] if k in lt else None


class DBlink(object):
    def __init__(self, link):
        # 数据库连接关键字=link;
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

    def __init__(self, lk, inout='in'):
        # 数据库关键字=lk; 内外网参数=inout
        # self.__lk = lk
        self.link = jsonfile('LinkDB', lk)
        self.link['host'] = self.link['host'][inout]

    def get(self):
        with DBlink(self.link) as f:
            return f

    def select(self, sqltxt):
        with DBlink(self.link) as f:
            if f[-1] is True:
                try:
                    f[0].execute(sqltxt)
                    rows = f[0].fetchall()
                    fc = f[0].rowcount
                    return rows, fc
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
                    fc = f[0].rowcount
                    return '%s Rows %s is OK.' % (sqltxt.split(' ')[0].title(), fc)
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
                    fc = f[0].rowcount
                    return '%s Rows %s is OK.' % (sqltxt.split(' ')[0].title(), fc)
                except Exception as e:
                    f[1].rollback()
                    return str(e)
            else:
                return f

    def runsql(self, sqlf):  # sqlf=sql文件名称
        """连接数据库执行sql文件"""
        sf = jsonfile("LinkDB", "SqlFiles")
        sql_file = sf + sqlf + ".sql"
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
        dbname = jsonfile('LinkDB', 'DB', 'goods')
        apitxt['key'] = self.__key
        if barcode: apitxt.update(barcode=barcode)
        if start_time:
            now = (datetime.datetime.now() + datetime.timedelta(days=int(start_time))).strftime("%Y-%m-%d %H:%M:%S")
            apitxt.update(start_time=now)
        else:
            if update == 'yes':
                rtime = d.select("SELECT MAX(etime) AS time FROM " + dbname)
                if rtime[0][0]['time']:
                    apitxt.update(start_time=rtime[0][0]['time'].strftime("%Y-%m-%d %H:%M:%S"))
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
            sql = "insert into " + dbname + "(SPDM,SPTM,COLOR_ID,SIZE_ID,SL,KW,etime) values(%s,%s,%s,%s,%s,%s,%s)"
            dtt = d.edit("delete from " + dbname)
            itt = d.insert(sql, rall)
            return True, dtt, itt
        elif update == 'yes':
            sqlt = "insert into " + dbname + "_T(SPDM,SPTM,COLOR_ID,SIZE_ID,SL,KW,etime) values(%s,%s,%s,%s,%s,%s,%s)"
            dttt = d.edit("delete from " + dbname + "_T")
            ittt = d.insert(sqlt, rall)
            sf = d.runsql(dbname)
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

    # def run(self):
    #     a = self.__test
    #     a['a'] = '1'
    #     b = self.urlsign(a)
    #     return b


class LinkPhoto(object):

    def __init__(self, delfile=True, view=False):
        # 检索目录=dirs; 是否删除文件=delfile; 图片修改最长边=photosize; 显示检索过程=view
        self.dlx = delfile
        self.view = view
        self.__runtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        dirs = jsonfile("PhotoDir")
        self.__zbpath = dirs['zb']
        self.__naspath = dirs['nas']
        self.__zbnaspath_b = dirs['zb_nas_b']
        self.__zbnaspath_s = dirs['zb_nas_s']

    def __delfile(self, files):
        # 根据files列表，删除图片文件
        f = []
        for file in files:
            if os.path.exists(file):
                os.remove(file)
            else:
                f.append(file)
        if f:
            return False, f
        else:
            return True

    def __rephoto(self, files, rs=600):  # rs为最长边数值
        # 修改图片文件像素
        for file in files:
            try:
                im = Image.open(file[0])
                (x, y) = im.size
                if x > y:
                    x_s = rs
                    y_s = round(y * rs / x)
                else:
                    y_s = rs
                    x_s = round(x * rs / y)
                out = im.resize((x_s, y_s), Image.ANTIALIAS)
                out.convert('RGB')
                out.save(file[1])
            except Exception as e:
                print(file[0], file[1], e)

    def nas(self, dirs=None):
        # 图片检索主程序
        dirs = dirs if dirs else self.__naspath
        print('检索路径为' + dirs)
        db = LinkDb('GNet')
        dbname = jsonfile("LinkDB", "DB", "nas")
        if not db.get()[-1]: return db.get()
        # 检查数据库是否可以连接
        fn = ['1@', '2@']
        # 图片类型列表
        pd = []
        # 输出列表
        rp = []
        # 生成小图列表
        dp = []
        # 删除列表
        for r, ds, fs in os.walk(dirs):
            # 遍历检索目录
            if self.view: print(r)
            for d in ds:
                # 遍历子目录
                ft = ''
                # 目录状态参数
                fg = d.split("@") if d.count("@") == 2 else ['', '', '']
                # 如果有2个@，进行商品信息分割
                fu = os.listdir(os.path.join(r, d))
                # 将子目录中所有文件及文件夹存入 fu
                fl = [i.lower() for i in fu]
                # 将 fu 转为小写生成 fl
                for flist in fn:
                    # 遍历图片类型列表
                    f = flist + '.jpg'
                    fs = flist + 's.jpg'
                    if f in fl:
                        # 如果目录中有图片类型
                        fun = os.path.join(r, d, fu[fl.index(f)])
                        ft += f
                        if fs in fl:
                            # 如果目录中有小图
                            fmn = os.path.join(r, d, fu[fl.index(fs)])
                            # 生成文件绝对路径
                            fsize = os.path.getsize(fmn)
                            fsize = round(fsize / 1024)
                            if fsize > 100 and self.dlx:
                                # 如果小图文件大于100k 并 删除标记为 True
                                dp.append(fmn)
                                # 加入删除列表
                                rp.append(fun, fun.replace('@.', '@S.'))
                                # 加入生成小图列表
                        else:
                            rp.append(fun, fun.replace('@.', '@S.'))
                            # 如果目录中没有小图 加入生成小图列表
                    else:
                        # 如果目录中没有图片类型
                        if fs in fl:
                            # 如果目录中有小图文件
                            fmn = os.path.join(r, d, fu[fl.index(fs)])
                            dp.append(fmn)
                            # 加入删除列表
                ft = ft.replace('1@.jpg', '模特图')
                ft = ft.replace('2@.jpg', '景物图')
                ft = ft or '无主图'
                # 生成目录状态
                pd.append((os.path.join(r, d), d, fg[0], fg[1], fg[2], ft))
                # 将目录详细数据添加到 pd 列表
        sql = "insert into " + dbname + " values(%s,%s,%s,%s,%s,%s)"
        dtt = db.edit("delete from " + dbname)
        itt = db.insert(sql, pd)
        if dp:
            self.__delfile(dp)
        if rp:
            self.__rephoto(rp)
        return '修改数量：' + str(len(rp)), rp, '删除数量：' + str(len(dp)), dp, '检索文件数量：' + str(len(pd)), dtt, itt

    def zb(self, dirs=None, update=True):
        if dirs:
            dir_zb = dirs['zb']
            dir_zbnas_b = dirs['zb_nas_b']
            dir_zbnas_s = dirs['zb_nas_s']
        else:
            dir_zb = self.__zbpath
            dir_zbnas_b = self.__zbnaspath_b
            dir_zbnas_s = self.__zbnaspath_s
        print('总部路径：%s; NAS路径：%s' % (dir_zb, dir_zbnas_b))
        dbname = jsonfile("LinkDB", "DB", "zb")
        db = LinkDb('GNet')
        fs = [os.path.join(r, f) for r, ds, fs in os.walk(dir_zb) for f in fs if
              os.path.splitext(f)[-1] in ['.jpg', '.JPG']]
        zb_files = []
        for f in fs:
            p = ['', '']
            try:
                ff = os.path.splitext(os.path.split(f)[-1])[0].replace(" ", "")
                z = re.findall(r'^[A-Za-z][A-Za-z0-9-]*', ff)
                y = re.findall(r'[\u4E00-\u9FA5]+', ff)
                if z:
                    p[0] = ''.join(z).upper()
                    p[1] = ''.join(y) if y else ''
                    zb_files.append((f, p[0], p[1], self.__runtime))
            except Exception as e:
                print(e, f, z, y)
        sql = "insert into " + dbname + "_T values(%s,%s,%s,%s)"
        dtt = db.edit("delete from " + dbname + "_T")
        itt = db.insert(sql, zb_files)
        db.edit("DELETE FROM " + dbname + "_T WHERE (dirs NOT IN (SELECT MIN(dirs) AS aa "
                                          "FROM " + dbname + "_T AS a GROUP BY SPDM, COLOR))")
        ett = db.edit("DELETE FROM " + dbname + "_T FROM " + dbname + "_T LEFT OUTER JOIN BSERP2.dbo.SHANGPIN AS SP"
                    " ON " + dbname + "_T.SPDM = SP.SPDM WHERE (SP.SPDM IS NULL)")
        stt = db.select("SELECT t.dirs, t.SPDM, t.COLOR FROM " + dbname + " AS zb RIGHT OUTER JOIN " + dbname + "_T AS t"
                       " ON zb.SPDM = t.SPDM AND zb.COLOR = t.COLOR WHERE (zb.SPDM IS NULL)")
        if update:
            n_fb = []
            n_fs = []
            for pi in stt[0]:
                newf = pi['SPDM'] + "@" + pi['COLOR'] + ".jpg" if pi['COLOR'] else pi['SPDM'] + ".jpg"
                n_fs.append((pi['dirs'], os.path.join(dir_zbnas_s, newf)))
                n_fb.append((pi['dirs'], os.path.join(dir_zbnas_b, newf)))
            if n_fb:
                # print(n_fb)
                self.__rephoto(n_fs)
                self.__rephoto(n_fb, 2000)
                f_nas = [(dir_zbnas_b + os.sep + f, os.path.splitext(f)[0].split('@')[0],
                          os.path.splitext(f)[0].split('@')[1], self.__runtime)
                         if len(os.path.splitext(f)[0].split('@')) is 2 else
                         (dir_zbnas_b + os.sep + f, os.path.splitext(f)[0].split('@')[0], '', self.__runtime)
                         for f in os.listdir(dir_zbnas_b) if os.path.splitext(f)[-1] in ['.jpg', '.JPG']]
                sql = "insert into " + dbname + " values(%s,%s,%s,%s)"
                db.edit("delete from " + dbname)
                db.insert(sql, f_nas)
            return '更新%s条记录。' % len(n_fb)
        else:
            return stt
