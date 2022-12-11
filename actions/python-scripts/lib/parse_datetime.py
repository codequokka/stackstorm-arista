from datetime import datetime

import pytz


def parse_datetime(datetime_str):
    start_year = 1900
    current_year = datetime.now(pytz.timezone("Asia/Tokyo")).year
    parsed_datetime = datetime.strptime(datetime_str, "%b %d %H:%M:%S")
    parsed_datetime = parsed_datetime.replace(
        year=parsed_datetime.year + (current_year - start_year),
        tzinfo=pytz.timezone("Asia/Tokyo"),
    )

    return parsed_datetime


def get_current_datetime():
    current_datetiem = datetime.now(pytz.timezone("Asia/Tokyo"))
    return current_datetiem
