from sqlalchemy import Column, String, Integer
from database import Base

class Student(Base):
    __tablename__ = 'student'
    sid = Column(String(10), primary_key=True)
    name = Column(String(50))
    age = Column(Integer)
    phone_number = Column(String(30))