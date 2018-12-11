import re

from appmodel.app_main import *

dirs = {'zb': '/Volumes/部门内部文件/物流部', 'zb_nas': '/Volumes/图片/整理/总部'}
a = LinkPhoto().zb(dirs)
print(a)

