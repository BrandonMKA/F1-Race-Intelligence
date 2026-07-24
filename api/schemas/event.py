from datetime import datetime

from pydantic import BaseModel


class EventSummary(BaseModel):
    event_id: int
    season: int
    round_number: int
    event_name: str
    session_name: str
    session_date: datetime | None = None


class EventDetail(EventSummary):
    result_count: int
    lap_count: int
