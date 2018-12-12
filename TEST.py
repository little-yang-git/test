import re

from appmodel.app_main import *
# dir_zbnas_b = "/Volumes/部门内部文件/物流部/物流部专用/2017年报表汇总/货品图册/1月"
# db = LinkDb('GNet')
# f_nas = [(dir_zbnas_b + os.sep + f, os.path.splitext(f)[0].split('@')[0],
#           os.path.splitext(f)[0].split('@')[1], self.__runtime)
#          if len(os.path.splitext(f)[0].split('@')) is 2 else
#          (dir_zbnas_b + os.sep + f, os.path.splitext(f)[0].split('@')[0], '', self.__runtime)
#          for f in os.listdir(dir_zbnas_b) if os.path.splitext(f)[-1] in ['.jpg', '.JPG']]
# sql = "insert into PhotoFile_ZB values(%s,%s,%s,%s)"
# db.edit("delete from PhotoFile_ZB")
# db.insert(sql, f_nas)
a = LinkPhoto().zb()
print(a)
