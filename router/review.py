from datetime import date,datetime
from random import randrange
from typing import List
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

import models, schemas, utils, oauth2, database
from fastapi import Depends, FastAPI, status,Response, HTTPException, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["review"],
    prefix="/review",
)


@router.post("/add",status_code=201)
def addReview(review:str,star:int, reviewin:schemas.ReviewIn, db:Session=Depends(database.get_db), current_user: models.User = Depends(oauth2.getCurrentUser)):

    if current_user.role!="USER":
        raise HTTPException(status_code=404, detail="error")

    review = models.Review(review=review,starCount=star,reviewer_id=current_user.id,subject_id=reviewin.subjectId)

    doctor_serial = db.query(models.DoctorSerial).filter(models.DoctorSerial.id == reviewin.orderId).first()

    doctor_serial.reviewchecked = 1
    db.add(doctor_serial)
    db.commit()
    db.add(review)
    db.commit()

    return {"details":"success"}

@router.get("/{id}")
def getReview(id:int, db:Session=Depends(database.get_db), current_user: models.User = Depends(oauth2.getCurrentUser)):

    if current_user.role!="USER" and current_user.role!="DOCTOR":
        raise HTTPException(status_code=404, detail="error")

    reviews = db.query(models.Review).filter(models.Review.subject_id == id).all()
    reviewsout = []
    for i  in reviews:
        reviewout=schemas.ReviewOut(id=i.id,review=i.review,starCount=i.starCount,reviewerId=i.reviewer_id,subjectId=i.subject_id, reviewerName=i.reviewer.name)
        reviewsout.append(reviewout)
    
    return reviewsout

@router.get("/pending")
def getPendingReview(db:Session=Depends(database.get_db), current_user: models.User = Depends(oauth2.getCurrentUser)):

    if current_user.role!="USER":
        raise HTTPException(status_code=404, detail="error")

    doctorserials = db.query(models.DoctorSerial).filter(models.DoctorSerial.user_id == current_user.id).filter(models.DoctorSerial.reviewchecked == 0).all()
    reviewsout = []
    for i in doctorserials:
        reviewout=schemas.ReviewPending(orderId=i.id,subjectId=i.doctor_id,subjectName=1)
        reviewsout.append(reviewout)
    
    return reviewsout


