from appmodel.app_main import *
import datetime

start = datetime.datetime.now()

while True:
    a = LinkApi()
    txt = a.goods(update='yes')
    print(txt)
    print('Efast库存检索；运行时间：%s 秒' % (datetime.datetime.now() - start))
    # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    sys.stdout.flush()
    pzb = LinkPhoto().zb(update=False)
    print(pzb)
    print('总部照片检索；运行时间：%s 秒' % (datetime.datetime.now() - start))
    sys.stdout.flush()
    pnas = LinkPhoto().nas()
    print(pnas)
    print('Nas照片检索；运行时间：%s 秒' % (datetime.datetime.now() - start))
    sys.stdout.flush()
    end = datetime.datetime.now()
    # time.sleep(600)

