from pydantic import BaseModel


class Lap(BaseModel):
    driver_id: int
    driver_code: str
    full_name: str | None = None
    lap_number: int
    stint_number: int | None = None
    compound: str | None = None
    tire_life: float | None = None
    position: int | None = None
    lap_time_ms: float | None = None
    sector_1_ms: float | None = None
    sector_2_ms: float | None = None
    sector_3_ms: float | None = None
    is_personal_best: bool
    pit_in: bool
    pit_out: bool