from typing import Literal

from pydantic import BaseModel


class PumpStateResponse(BaseModel):
    is_on: bool | None = None
    current_glucose_value: float | None = None
    glucose_level: Literal["normal", "low", "high"] | None = None
    alert_level: Literal["off", "notification", "warning", "critical"] | None = None
    bolus_status: Literal[
        "pump_off",
        "limit_check",
        "allowed",
        "with_warning",
        "suspended",
        "blocked",
    ] | None = None
    basal_speed_pc: int | None = None
    manual_action_required: bool | None = None
    message: str | None = None
    action_message: str | None = None
    alerts_count: int = 0