from pydantic import BaseModel, Field
from datetime import datetime
class InstanceTaskRequest(BaseModel):
    task_name: str = Field(..., example="Immediate Task")

class ScheduleTaskRequest(BaseModel):
    task_name: str = Field(..., example="Schedule Task")
    schedule_type: str = Field(..., example="daily", description="'daily' or 'one_time'")
    # Required only for one-time scheduling
    run_datetime: datetime | None = Field(
        None, example="2025-09-22T14:30:00", description="For one-time scheduling"
    )
    # Required only for daily scheduling
    run_time: str | None = Field(
        None, example="10:30", description="For daily schedule in HH:MM format"
    )