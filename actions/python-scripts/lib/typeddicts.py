from datetime import datetime
from typing import TypedDict


class StructuredLog(TypedDict):
    datetime: datetime
    fqdn: str
    message: str
