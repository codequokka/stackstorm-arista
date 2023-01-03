from datetime import datetime, timedelta, timezone

JST = timezone(timedelta(hours=+9), "JST")


def parse_datetime(datetime_str: str, datetime_format: str) -> datetime:
    """
    Parse a datetime string and return a datetime object

    parameters
    ----------
    datetme_str : str
        A datetime string

    datetme_format : str
        A datetime format code

    returns
    -------
    datetime
        A datetime object
    """
    parsed_datetime = datetime.strptime(datetime_str, datetime_format)

    if parsed_datetime.year == 1900 and parsed_datetime.tzinfo is None:
        start_year = 1900
        current_year = datetime.now().year

        parsed_datetime = parsed_datetime.replace(
            year=parsed_datetime.year + (current_year - start_year), tzinfo=JST
        )

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
