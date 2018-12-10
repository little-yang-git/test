import os

# from

b = '/Volumes/图片/整理/2018秋冬10月/10.11'
server = '/Volumes/部门内部文件/物流部'
# fpath = []
# fpath = [os.path.join(r, f).lower() for r, ds, fs in os.walk(server) for f in fs if
#          os.path.splitext(f)[-1].lower() in '.jpg']
# for r, ds, fs in os.walk(server):
#     for f in fs:
#         if os.path.splitext(f)[-1].lower() == '.jpg':
#             fpath.append(os.path.join(r, f))


# for r, ds, fs in os.walk(b):
#     for d in ds:
#         fg = d.split("@") if d.count("@") == 2 else None
#         if fg:
#             fg.insert(0,os.path.join(r, d))
#             fpath.append(fg)
npath = [os.path.join(r, d) for r, ds, fs in os.walk(b) for d in ds]
print(npath)
print(len(npath))
