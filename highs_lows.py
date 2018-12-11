import os
import time
from appmodel.app_main import *

db = LinkDb('GNet')
tt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
dirs = {'zb': '/Volumes/部门内部文件/物流部', 'zb_nas': '/Volumes/图片/整理/总部'}
fs = [(dirs['zb_nas'] + os.sep + f, os.path.splitext(f)[0].split('@')[0], os.path.splitext(f)[0].split('@')[1], tt)
      if len(os.path.splitext(f)[0].split('@')) is 2 else
      (dirs['zb_nas'] + os.sep + f, os.path.splitext(f)[0].split('@')[0], '', tt)
      for f in os.listdir(dirs['zb_nas']) if os.path.splitext(f)[-1] in ['.jpg', '.JPG']]
print(fs)
sql = "insert into PhotoFile_ZB values(%s,%s,%s,%s)"
dtt = db.edit("delete from PhotoFile_ZB")
itt = db.insert(sql, fs)
print(dtt, itt)
# a = 'ZS-3561@驼灰'
# print(a.split('@'))
