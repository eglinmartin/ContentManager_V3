from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class Media:
    title: str
    director: str
    cast: List[str]
    code: int
    date: datetime
    media_type: str
    tags: List[str]
