from appmodel.app_main import *
import datetime

start = datetime.datetime.now()
# while True:
#     a = LinkApi()
#     txt = a.goods(update='yes')
#     print(txt + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
#     sys.stdout.flush()
#     time.sleep(2)

a = LinkPhoto('/Volumes/图片/整理/2018秋冬10月/10.11/11.20 修好').nas()

for i in a:
    print(i)

end = datetime.datetime.now()
print('Running time: %s Seconds' % (end - start))
