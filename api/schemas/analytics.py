from pydantic import BaseModel


class FastestLap(BaseModel):
    position: int
    driver_id: int
    driver_code: str
    full_name: str | None = None
    constructor_name: str | None = None
    lap_number: int
    lap_time_ms: float
    compound: str | None = None


class PositionGain(BaseModel):
    driver_id: int
    driver_code: str
    full_name: str | None = None
    constructor_name: str | None = None
    grid_position: int | None = None
    finish_position: int | None = None
    positions_gained: int | None = None


class ConstructorPerformance(BaseModel):
    constructor_id: int
    constructor_name: str
    driver_count: int
    total_points: float
    best_finish: int | None = None
    average_finish: float | None = None


class StintSummary(BaseModel):
    driver_id: int
    driver_code: str
    full_name: str | None = None
    stint_number: int
    compound: str | None = None
    first_lap: int
    last_lap: int
    lap_count: int
    average_lap_time_ms: float | None = None
    fastest_lap_time_ms: float | None = None