from datetime import datetime, timedelta
from pytz import timezone

tz_tashkent = timezone('Asia/Tashkent')


def shoud_edit(message_date : datetime) -> bool:
    age = datetime.now() - message_date
    if age < timedelta(hours=47):
        return True 
    return False


def get_expair_time(seconds : int) -> int:
    return int((datetime.now() + timedelta(seconds=seconds)).timestamp())


def get_next_day_sec() -> int:
    now = datetime.now()
    tmorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0) 
    left =  tmorrow - now
    return left.seconds