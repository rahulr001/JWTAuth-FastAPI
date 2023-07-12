from pydantic import BaseModel, EmailStr, constr
from datetime import datetime


class User_Creation_Schema(BaseModel):
    name: str
    email: EmailStr
    mobile_no: int
    password: str
    password1: str

    verified: bool = False

    verification_code: str | None

    created_at: datetime
    updated_at: datetime


class User_Login_Schema(BaseModel):
    email: EmailStr
    password: constr(max_length=8)
