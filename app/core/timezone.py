from datetime import datetime, timedelta, timezone

SEOUL = timezone(offset=timedelta(hours=9))


def utcnow():
    return datetime.now(tz=timezone.utc)
