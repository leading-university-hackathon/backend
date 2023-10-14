from database import Base
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP, DateTime, Date, ARRAY, Time
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship




class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique= True)
    password = Column(String, nullable=False)
    name = Column(String, nullable= False)
    url = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, 
                       server_default=text("current_timestamp"))
    






