import os
import appmodel.app_main as appmain
from PIL import Image


def rephoto(files, rs): # rs为最长边数值
    # 修改图片文件像素
    for file in files:
        im = Image.open(file)
        (x, y) = im.size
        if x > y:
            x_s = rs
            y_s = round(y * rs / x)
        else:
            y_s = rs
            x_s = round(x * rs / y)
        out = im.resize((x_s, y_s), Image.ANTIALIAS)
        out.save(file.replace('@.', '@S.'))


def delfile(files):
    # 根据files列表，删除图片文件
    for file in files:
        if os.path.exists(file):
            os.remove(file)
        else:
            print("没有" + file + "此文件！")


def runphoto(dirs, dlx=True, Psize=600):
    # 图片检索主程序
    dt = dirs
    # 接受检索路径
    fn = ['1@', '2@']
    # 图片类型列表
    pd = []
    # 输出列表
    rp = []
    # 生成小图列表
    dp = []
    # 删除列表
    for r, ds, fs in os.walk(dt):
        # 遍历检索目录
        print(r)
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
                        if fsize > 100 and dlx:
                            # 如果小图文件大于100k 并 删除标记为 True
                            dp.append(fmn)
                            # 加入删除列表
                            rp.append(fun)
                            # 加入生成小图列表
                    else:
                        rp.append(fun)
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
    sql = """insert into File values(%s,%s,%s,%s,%s,%s)"""
    # 生成sql访问
    appmain.dblink('GNetMy', "delete from File", 'e')
    # 删除原表中数据
    appmain.dblink('GNetMy', sql, 'i', pd)
    # 向数据库中插入数据
    if dp:
        delfile(dp)
    if rp:
        rephoto(rp, Psize)
    return '修改数量：' + str(len(rp)), rp, '删除数量：' + str(len(dp)), dp, '检索文件数量：' + str(len(pd))
