from pydantic import BaseModel
from datetime import datetime


class User_Creation(BaseModel):
    name: str
    email: str
    mobile_no: int
    password: str
    password1: str

    verified: bool = False

    created_at: datetime
    updated_at: datetime
