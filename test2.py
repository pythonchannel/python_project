import time


def time_long2str(timeStamp):
    """把long类型的时间转换成字符串形式"""
    timeArray = time.localtime(timeStamp)
    strTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return strTime[:10]

print(time_long2str(1545026190))
