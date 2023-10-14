from datetime import date,datetime
from random import randrange
from typing import List
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

import models, schemas, utils, oauth2, database,const
from fastapi import Depends, FastAPI, status,Response, HTTPException, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["doctor_serial"],
    prefix="/doctor_serial"
)


@router.post("/add" ,status_code=201)
def addDoctor_Serial(addDoctorSerial:schemas.addDoctorSerial, db:Session=Depends(database.get_db), current_user: models.User = Depends(oauth2.getCurrentUser)):

    if current_user.role!="USER":
        raise HTTPException(status_code=404, detail="error")


    doctor = db.query(models.Doctor).join(models.User).filter(models.User.id == addDoctorSerial.doctor_id).first()

    doctor_serial = models.DoctorSerial(type = addDoctor_Serial.type,user_id=current_user.id, doctor_id=doctor.user.id, date=datetime.now().date(), time=addDoctorSerial.time, appointmentDate=addDoctorSerial.appointmentDate)
      
    doctor_serial.checked = 0

    doctor.balance+=addDoctor_Serial.price-const.perUserCost

    if(addDoctor_Serial.type=="online"):
        for i in doctor.availableOnlineTimes:
            if i.date == addDoctor_Serial.appointmentDate:
                i.available_time = utils.set_new_serial_time(i.available_time)
                break
            
    if(addDoctor_Serial.type=="offline"):
        for i in doctor.availableOfflineTimes:
            if i.date == addDoctor_Serial.appointmentDate:
                i.available_time = utils.set_new_serial_time(i.available_time)
                break

    db.add(doctor_serial)
    db.commit()
    db.add(doctor)
    db.commit()

    return {"details":"success"}
