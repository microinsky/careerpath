# coding: utf-8
from datetime import datetime
import pytz

def getTimezoneObject(timezone, offset):
    if timezone not in pytz.all_timezones:
        return None

    # 验证客户端给出的时区是否有效
    tz = pytz.timezone(timezone)
    cal_offset = tz.utcoffset(datetime(2000, 1, 1, 0, 0))
    if cal_offset.seconds / 3600 == int(offset):
        return tz

def isDaylightSavingTime(timezone, date):
    return timezone.dst(date).seconds != 0
