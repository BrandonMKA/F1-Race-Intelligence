from pydantic import BaseModel


class RaceResult(BaseModel):
    driver_id: int
    driver_number: int | None = None
    driver_code: str
    first_name: str | None = None
    last_name: str | None = None
    full_name: str | None = None
    constructor_name: str | None = None
    grid_position: int | None = None
    finish_position: int | None = None
    points: float
    status: str | None = None