from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from utils.database import Base
from bson import ObjectId


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    mobile_no = Column(String)

    verified = Column(Boolean, default=False)
    password = Column(String)

    verification_code = Column(String)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now)
