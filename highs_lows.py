import os
import re

a = 'FY-11229A枣红3590'.upper()
b = a.encode('utf-8')
p = re.compile(r'/w*[\u4E00-\u9FA5]')
x = p.findall(a)
print(x)
z = re.findall(r'(.*[A-Za-z0-9-])(.*[\u4E00-\u9FA5])', a)
print(z)
print(type(z[0][1]))
