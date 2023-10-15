from datetime import datetime
from typing import List


import models, schemas, utils, oauth2, database
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from repo import review_repo

router = APIRouter(
    tags=["doctor"],
    prefix="/doctor"
)
@router.get("/all", response_model=List[schemas.DoctorOut])
def get_doctors(db: Session = Depends(database.get_db), current_user: models.User= Depends(oauth2.getCurrentUser)):

    if current_user.role!="DOCTOR" and current_user.role!="USER":
        raise HTTPException(status_code=404, detail="error")
    
    doctors = db.query(models.Doctor).join(models.User).all()

    current_date = datetime.now().date()
    updated_doctors = []

    if not doctors:
        raise HTTPException(status_code=404, detail="empty")

    for doctor in doctors:
        for offline_time in doctor.availableOfflineTimes:
            if offline_time.date < current_date:
                offline_time.date = utils.next_date(offline_time.day)
                offline_time.available_time = offline_time.start_time

        for online_time in doctor.availableOnlineTimes:
            if online_time.date < current_date:
                online_time.date = utils.next_date(online_time.day)
                online_time.available_time = online_time.start_time

        utils.setSerialTime(doctor)
        doctor.rating = review_repo.findAvgRating(doctor.user.id,db)
        if not doctor.rating:
         doctor.rating = 0.0

        db.add(doctor)
        db.commit()
        db.refresh(doctor)

        updated_doctors.append(doctor)

    return updated_doctors

@router.get("/{id}",response_model=schemas.DoctorOut)
def get_doctor(id:int, db:Session = Depends(database.get_db),current_user: models.User = Depends(oauth2.getCurrentUser)):

    if current_user.role!="DOCTOR" and current_user.role!="USER":
        raise HTTPException(status_code=404, detail="error")
    
    doctor = db.query(models.Doctor).join(models.User).filter(models.User.id == id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor Not Found")

    current_date = datetime.now().date()
    for i in range(doctor.availableOfflineTimes.__len__()):
        if doctor.availableOfflineTimes[i].date <current_date:
            doctor.availableOfflineTimes[i].date=utils.next_date(doctor.availableOfflineTimes[i].day)
            doctor.availableOfflineTimes[i].available_time =doctor.availableOfflineTimes[i].start_time
    
    for i in range(doctor.availableOnlineTimes.__len__()):
        if doctor.availableOnlineTimes[i].date <current_date:
            doctor.availableOnlineTimes[i].date=utils.next_date(doctor.availableOnlineTimes[i].day)
            doctor.availableOnlineTimes[i].available_time =doctor.availableOnlineTimes[i].start_time
    
    utils.setSerialTime(doctor)
    
    doctor.rating = review_repo.findAvgRating(doctor.user.id,db)

    if not doctor.rating:
        doctor.rating = 0.0
    
    db.commit()


    return doctor

