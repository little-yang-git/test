import re

from appmodel.app_main import *

db = LinkDb('GNet')
fs = db.select('SELECT zb.dirs FROM PhotoFile_ZB AS zb LEFT OUTER JOIN BSERP2.dbo.SHANGPIN AS sp ON zb.SPDM = sp.SPDM '
              'WHERE (sp.SPDM IS NULL)')
print(len(fs))
for f in fs:
    os.remove(f['dirs'])