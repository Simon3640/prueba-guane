from datetime import datetime

from pydantic import BaseModel, validator


class NotificationEmail(BaseModel):
    email: str
    name: str
    pending: bool = False
    regular: bool = False
    date: datetime | None
   
    @validator('date', always=True)
    def validate_date(cls, v, values):
        if v is None and ((values['pending'] is True) or (values['regular'] is True)) :
            raise ValueError('Si la notificación es programada debe proporcianar una fecha')
        return v


class NotificationMobile(BaseModel):
    pass