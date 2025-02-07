from datetime import datetime, timezone
from typing import Optional

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, field_validator


class TaskResponse(BaseModel): 
    id: int
    task_info: str
    created_at: datetime
    updated_at: datetime 
    datetime_to_do: datetime


class TaskCreate(BaseModel):
    task_info: str
    datetime_to_do: datetime

    @field_validator("datetime_to_do", mode="after")
    def validate_deadline(cls, value):
        date_now = datetime.now(timezone.utc)
        if value < date_now:   
            err = "Value of `datetime_to_do` should not be in the past"
            raise RequestValidationError(err)
        return value
    

class TaskCreateDB(TaskCreate):
    pass


class TaskUpdate(BaseModel): 
    task_info: Optional[str] = None
    datetime_to_do: Optional[datetime] = None
    
    @field_validator("datetime_to_do", mode="after")
    def validate_deadline(cls, value):
        date_now = datetime.now(timezone.utc)
        if value < date_now:   
            err = "Value of `datetime_to_do` should not be in the past"
            raise RequestValidationError(err)
        return value

class TaskUpdateDB(TaskUpdate): 
    pass