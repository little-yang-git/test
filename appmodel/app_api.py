import time
import hashlib
import requests
import sys


def api_kwcf(data):
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
        # ------ 库位字典格式
        # a = {"shelf_list": [
        #     {
        #         "store_code": "001",
        #         "shelf": [
        #             {
        #                 "shelf_code": "D03L05",
        #                 "shelf_name": "D03L05"
        #             },
        #             {
        #                 "shelf_code": "D07L03",
        #                 "shelf_name": "D07L03"
        #             },
        #             {
        #                 "shelf_code": "D07R05",
        #                 "shelf_name": "D07R05"
        #             },
        #             {
        #                 "shelf_code": "S03R05",
        #                 "shelf_name": "S03R05"
        #             }]
        #     }
        # ]}
        # ------ 如果有库位信息保存，否则返回None
        uu = list(u.values())
        # 将字典拼合为list
        cs = uu.pop(1)
        # 提取sku字段
        uu.extend([cs[-4:-2], cs[-2:]])
        # 截取sku中，色号尺码号部分拆分字段
        uu = tuple(uu)
        # 转换为元组
        z.append(uu)
    return z


def urlsign(data):
    # 拼合post；sign数据
    a_url = "http://openapi.baotayun.com/openapi/webefast/web/?app_act=openapi/router"
    a_data = {'method': data['a_met'],
              'format': 'json',
              'key': "bfd7910d15467517613d9661835afc41",
              'v': '2.0',
              'sign_method': 'md5',
              'timestamp': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
              'page': data['page'],
              'store_code': '001'}
    # 基础数据
    signtxt = ''.join([k + str(v) for k, v in sorted(a_data.items())])
    # 拼合data
    sign = hashlib.md5(signtxt.encode(encoding='UTF-8')).hexdigest().upper()
    # 生成sign
    url = a_url + ''.join(['&' + k + '=' + str(v) for k, v in a_data.items()]) + 'sign=' + sign
    # 生成url
    a_data['sign'] = sign
    return {'url': url, 'data': a_data}


def runapi(dtxt, page=1, pages=None):
    # api访问主程序 dtxt=访问参数；page=开始页数；pages=返回页数
    d = dtxt
    p = page
    ps = page + 3
    rall = []
    while p <= ps:
        d['page'] = p
        dout = urlsign(d)
        # 解析访问参数
        r = requests.post(dout['url'], dout['data'])
        # api请求
        if r.status_code != 200:
            print('连接错误！')
            sys.exit()
        # else:
        #     print(dout['data'])
        data = r.json()
        # 生产字典输出到data
        if p == page:
            # 如果为首次循环
            pagec = data['data']['filter'].get('page_count')
            # 获取总页数
            ps = pages + page - 1 if pages and pages + page - 1 <= pagec else pagec
            # 如果设置返回页数<=总页数
            print(pagec)
            # 计算共多少页
        rall += (api_kwcf(data))
        # 将每页数据汇总
        print(p)
        # 打印页数
        # time.sleep(1)
        # 等待
        p += 1
    return rall
