from datetime import date,datetime, timedelta
from random import randrange
from typing import List
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

import models, schemas, utils, oauth2, database,const
from fastapi import Depends, FastAPI, status,Response, HTTPException, APIRouter
from sqlalchemy.orm import Session

from repo import doctor_serialrepo

router = APIRouter(
    tags=["doctor_serial"],
    prefix="/doctor_serial"
)


@router.post("/add" ,status_code=201)
def addDoctorSerial(addDoctorSerial:schemas.addDoctorSerial, db:Session=Depends(database.get_db), current_user: models.User = Depends(oauth2.getCurrentUser)):

    if current_user.role!="USER":
        raise HTTPException(status_code=404, detail="error")


    doctor = db.query(models.Doctor).join(models.User).filter(models.User.id == addDoctorSerial.doctor_id).first()

    doctor_serial = models.DoctorSerial(price=addDoctorSerial.price,type = addDoctorSerial.type,user_id=current_user.id, doctor_id=doctor.user.id, date=datetime.now().date(), time=addDoctorSerial.time, appointmentDate=addDoctorSerial.appointmentDate)
      
    doctor_serial.checked = 0

    doctor_serial.reviewchecked =-1

    doctor_serial.prescription="default"

    doctor.balance+=addDoctorSerial.price-const.perUserCost

    if(addDoctorSerial.type=="online"):
        for i in doctor.availableOnlineTimes:
            if i.date == addDoctorSerial.appointmentDate:
                i.available_time = utils.set_new_serial_time(i.available_time)
                break
            
    if(addDoctorSerial.type=="offline"):
        for i in doctor.availableOfflineTimes:
            if i.date == addDoctorSerial.appointmentDate:
                i.available_time = utils.set_new_serial_time(i.available_time)
                break

    db.add(doctor_serial)
    db.commit()
    db.add(doctor)
    db.commit()

    return {"details":"success"}


@router.put("/update/pres/{id}",status_code=202)
def update_prescription(id:int, pres:schemas.Prescription, db:Session=Depends(database.get_db), current_user: models.User = Depends(oauth2.getCurrentUser)):

    if current_user.role!="DOCTOR":
        raise HTTPException(status_code=404, detail="error")

    serial = db.query(models.DoctorSerial).filter(models.DoctorSerial.id == id).first()

    if serial.doctor_id != current_user.id:
        raise HTTPException(status_code=404, detail="error")

    serial.prescription = pres.prescription

    db.add(serial)
    db.commit()

    return {"details":"success"}

@router.get("/upcoming",response_model=List[schemas.DoctorSerialOut])
def showUpcomingDoctorSerial(db:Session=Depends(database.get_db), current_user: models.User = Depends(oauth2.getCurrentUser)):

    if current_user.role!="USER" and current_user.role!="DOCTOR":
        raise HTTPException(status_code=404, detail="error")

    seriasOut =[]
    time = utils.convert_time_to_double(datetime.combine(datetime.today(), datetime.now().time()) - timedelta(minutes=30))
    if current_user.role=="USER":
        serials = doctor_serialrepo.findUpcomingSerialforUser(current_user.id, datetime.now().date(), time,db)
        for i in serials:
            serialOut = schemas.DoctorSerialOut(id=i.id, price=i.price, type=i.type, user_id=i.user_id, doctor_id=i.doctor_id, doctorName=i.doctor.name, time=i.time, appointmentDate=i.appointmentDate)
            seriasOut.append(serialOut)
    
    elif current_user.role=="DOCTOR":
        serials = doctor_serialrepo.findUpcomingSerialforDoctor(current_user.id, datetime.now().date(),time,db)
        for i in serials:
            serialOut = schemas.DoctorSerialOut(id=i.id, price=i.price, type=i.type, user_id=i.user_id, doctor_id=i.doctor_id, doctorName=i.doctor.name, time=i.time, appointmentDate=i.appointmentDate)
            seriasOut.append(serialOut)
    return seriasOut
    
@router.put("/check/{id}",status_code=202)
def checkDoctorSerial(id:int, db:Session=Depends(database.get_db), current_user: models.User = Depends(oauth2.getCurrentUser)):

    if current_user.role!="DOCTOR":
        raise HTTPException(status_code=404, detail="error")
    
    serial = db.query(models.DoctorSerial).filter(models.DoctorSerial.id == id).first()
    serial.checked = 1
    serial.reviewchecked = 0
    db.add(serial)
    db.commit()
    
    return {"details":"success"}

@router.get("/pres/all",status_code=status.HTTP_200_OK)
def getAllPrescriptions(db:Session=Depends(database.get_db), current_user: models.User = Depends(oauth2.getCurrentUser)):

    if current_user.role!="USER":
        raise HTTPException(status_code=404, detail="error")
    
    serials = doctor_serialrepo.findPrescriptionsForUser(current_user.id,db)

    prescriptions =[]

    for i in serials:
        prescription = schemas.CompletedPrescription(prescription=i.prescription, doctorId=i.doctor_id, doctorName=i.doctor.name)
        prescriptions.append(prescription)

    return prescriptions