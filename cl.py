from appmodel.app_main import *
import datetime

start = datetime.datetime.now()

while True:
    a = LinkApi()
    txt = a.goods()
    print(txt)
    print('Efast库存检索；运行时间：%s 秒' % (datetime.datetime.now() - start))
    sys.stdout.flush()
    pnas = LinkPhoto().nas()
    print(pnas)
    print('Nas照片检索；运行时间：%s 秒' % (datetime.datetime.now() - start))
    sys.stdout.flush()
    pzb = LinkPhoto().zb()
    print(pzb)
    print('总部照片检索；运行时间：%s 秒' % (datetime.datetime.now() - start))
    sys.stdout.flush()
    end = datetime.datetime.now()
    # time.sleep(600)

