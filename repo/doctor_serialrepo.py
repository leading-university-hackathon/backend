from datetime import date
import models,database
from fastapi import Depends
from sqlalchemy.orm import Session
def findUpcomingSerialforUser(userId, date:date, time:float,db:Session=Depends(database.get_db)):

 upcoming_serials = (
        db.query(models.DoctorSerial)
        .filter(
            (
                (models.DoctorSerial.appointmentDate == date)
                & (models.DoctorSerial.time >= time)
            )
            | (models.DoctorSerial.appointmentDate > date)
        )
        .filter(models.DoctorSerial.user_id == userId)
        .filter(models.DoctorSerial.checked == 0)
        .all()
    )
 
 return upcoming_serials
    

def findUpcomingSerialforDoctor(doctorId, date:date, time:float,db:Session=Depends(database.get_db)):
    upcoming_serials = (
        db.query(models.DoctorSerial)
        .filter(
            (
                (models.DoctorSerial.appointmentDate == date)
                & (models.DoctorSerial.time >= time)
            )
            | (models.DoctorSerial.appointmentDate > date)
        )
        .filter(models.DoctorSerial.doctor_id == doctorId)
        .filter(models.DoctorSerial.checked == 0)
        .all()
    )
    return upcoming_serials

def findPrescriptionsForUser(userId, db:Session=Depends(database.get_db)):
    doctorSerial = db.query(models.DoctorSerial).filter(models.DoctorSerial.user_id == userId).filter(models.DoctorSerial.prescription != "default").all()
    
    return doctorSerial