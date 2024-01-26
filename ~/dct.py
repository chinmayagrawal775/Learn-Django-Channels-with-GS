from ctypes import sizeof
from datetime import datetime,timedelta
from time import time


a = [
    # "15:30",
    # "15:59",
    # "2:08",
    # "2:59",
    # "14:35",
    # "17:43",
    # "30:28",
    # "31:06",
    # "16:25",
    # "27:01",
    # "16:23",
    # "28:36",
    # "2:01:29",
    # "48:20",
    # "30:13",
    # "1:58:09",
    # "1:52:40",
    # "8:08",
    # "3:51",
]

timestamp = []
for t in a:
    if(len(t)<=5):
        d = datetime.strptime(t, '%M:%S').time()
    else:
        d = datetime.strptime(t, '%H:%M:%S').time()
    s = ()
    a = (d.hour,)
    s = s + a
    a = (d.minute,)
    s = s + a
    a = (d.second,)
    s = s + a
    timestamp.append(s)

ho,mi,se = 0,0,0
for aaa in timestamp:
    ho += aaa[0]
    mi += aaa[1]
    se += aaa[2]

mi = mi * 60
ho = ho * 60 * 60
se = se + mi +ho

def convert(n):
    return str(timedelta(seconds = n))
     
print(convert(se))