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
    

class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, 
                       server_default=text("current_timestamp"))
    url = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User")

# class Departments(Base):
#     __tablename__ = "departments"
#     id = Column(Integer, autoincrement=True,  primary_key= True)
#     department = Column(String, nullable= False, unique=True)

# class Doctor(Base):
#     __tablename__ = "doctors"
#     id = Column(Integer, primary_key=True, nullable= False, autoincrement=True)
#     email = Column(String, nullable=False, unique= True)
#     password = Column(String, nullable=False)
#     created_at = Column(Date, nullable=False, 
#                        server_default=text("current_timestamp"))
#     name = Column(String, nullable= False)
#     specialization = Column(String, ForeignKey("departments.department", ondelete="CASCADE"))
#     availability = relationship("Doctors_availability",back_populates="doctor" )



# class Doctors_availability(Base):
#     __tablename__ = "doctors_availability"
#     id = Column(Integer, primary_key=True, nullable= False, autoincrement=True)
#     doctor_id = Column(Integer, ForeignKey("doctors.id", ondelete="CASCADE"), unique= True)
#     date = Column(ARRAY(Date))
#     available_time_slot = Column(ARRAY(Time))
#     doctor = relationship("Doctor", back_populates="availability")



# class Patient(Base):
#     __tablename__ = "patients"
#     id = Column(Integer, primary_key=True, nullable= False, autoincrement=True)
#     email = Column(String, nullable=False, unique= True)
#     password = Column(String, nullable=False)
#     created_at = Column(Date, nullable=False, 
#                        server_default=text("current_timestamp"))
#     name = Column(String, nullable= False)

#     Disease = Column(String, ForeignKey("departments.department", ondelete="CASCADE"))


# class appoinments(Base):
#     __tablename__ = "appoinments"
#     id = Column(Integer, primary_key=True, nullable= False, autoincrement=True)
#     created_at = Column(Date, nullable=False, 
#                        server_default=text("current_date"))
#     name = Column(String, nullable= False)

#     created_at = Column(Date, nullable=False, 
#                        server_default=text("current_timestamp"))
    
#     patient_id = Column(Integer, ForeignKey("patients.id"))
#     doctor_id = Column(Integer, ForeignKey("doctors.id"))
#     appoinment_date = Column(DateTime)
    



