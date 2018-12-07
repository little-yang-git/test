from appmodel.app_main import *
import appmodel.app_photo as app_photo
import appmodel.app_api as app_api
import datetime

start = datetime.datetime.now()

# 进行照片目录检索
# a = app_photo.runphoto("/Volumes/图片/整理/2018秋冬10月")

# 通过api更新efast库位表
d = LinkDb('GNet')
# print(d.get())
if d.get()[-1] is True:
    a = {"a_met": "prm.goods.inv.get"}
    pd = app_api.runapi(a,1,3)
    # print(pd)
    sql = "insert into API_Kucun_Efast values(%s,%s,%s,%s,%s,%s)"
    d.edit("delete from API_Kucun_Efast")
    d.insert(sql, pd)

end = datetime.datetime.now()
print('Running time: %s Seconds' % (end - start))

