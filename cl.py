from appmodel.app_main import *
import time


while True:
    a = LinkApi()
    txt = a.goods(update='yes')
    print(txt + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    sys.stdout.flush()
    time.sleep(2)
