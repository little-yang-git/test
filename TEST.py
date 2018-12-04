import appmodel.app_main as app_main
import appmodel.app_photo as app_photo
import appmodel.app_api as app_api
import datetime

start = datetime.datetime.now()

# 进行照片目录检索
# a = app_photo.runphoto("/Volumes/图片/整理/2018秋冬10月")

# 通过api更新efast库位表
d = {"a_met": "prm.goods.inv.get", "page": '1'}
pd = app_api.runapi(d)
print(pd)
sql = "insert into API_Kucun_Efast values(%s,%s,%s,%s,%s,%s)"
app_main.dblink('GNet', "delete from API_Kucun_Efast", 'e')
app_main.dblink('GNet', sql, 'i', pd)

end = datetime.datetime.now()
print('Running time: %s Seconds' % (end - start))

