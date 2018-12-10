import os
import re
from appmodel.app_main import *
db = LinkDb('GNet')
b = '/Volumes/部门内部文件/物流部'
fs = [os.path.join(r, f) for r, ds, fs in os.walk(b) for f in fs if os.path.splitext(f)[-1] in ['.jpg', '.JPG']]
zb_files = []
for f in fs:
    ff = os.path.splitext(os.path.split(f)[-1])[0].replace(" ", "")
    z = re.findall(r'(.*[A-Za-z0-9-])(.*[\u4E00-\u9FA5])', ff)
    zb_files.append((f, z[0][0].upper(), z[0][1], ''))
print(zb_files)
sql = "insert into PhotoFile_ZB values(%s,%s,%s,%s)"
dtt = db.edit("delete from PhotoFile_ZB")
itt = db.insert(sql, zb_files)
