import re

from appmodel.app_main import *

db = LinkDb('GNet')
b = r'C:\Users\YY.PC\Desktop\1'
fs = [os.path.join(r, f) for r, ds, fs in os.walk(b) for f in fs if os.path.splitext(f)[-1] in ['.jpg', '.JPG']]
zb_files = []
for f in fs:
    p = ['', '']
    try:
        ff = os.path.splitext(os.path.split(f)[-1])[0].replace(" ", "")
        z = re.findall(r'^[A-Za-z][A-Za-z0-9-]*', ff)
        y = re.findall(r'[\u4E00-\u9FA5]+', ff)
        if z:
            p[0] = ''.join(z).upper()
            p[1] = ''.join(y) if y else ''
            zb_files.append((f, p[0], p[1], ''))
    except Exception as e:
        print(e, f, z, y)
for i in zb_files:
    print(i)
# sql = "insert into PhotoFile_ZB values(%s,%s,%s,%s)"
# dtt = db.edit("delete from PhotoFile_ZB")
# itt = db.insert(sql, zb_files)
