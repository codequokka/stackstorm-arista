from datetime import datetime, timedelta, timezone

from dateutil.parser import parse

JST = timezone(timedelta(hours=+9), "JST")


def parse_datetime(datetime_str: str) -> datetime:
    """
    Parse a datetime string and return a datetime object

    parameters
    ----------
    datetme_str : str
        A datetime string

    returns
    -------
    datetime
        A datetime object
    """
    parsed_datetime = parse(datetime_str)

    if parsed_datetime.tzinfo is None:
        parsed_datetime = parsed_datetime.replace(tzinfo=JST)

    return parsed_datetime


def get_current_datetime() -> datetime:
    """
    Return a datetime object with the current datetime

    returns
    -------
    datetime
        A datetime object
    """
    current_datetiem = datetime.now(JST)

    return current_datetiem
