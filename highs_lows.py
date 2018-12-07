import time
import sys
for x in range(10):
    # print("aaa%d" % x, end="\r")
    sys.stdout.write('\r')
    sys.stdout.write("aaa%d" % x)
    sys.stdout.flush()
    time.sleep(0.5)