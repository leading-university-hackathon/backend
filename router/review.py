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

    review = models.Review(review=review,starCount=star,reviewer_id=current_user.id,subject_id=reviewin.subject_id)

    doctor_serial = db.query(models.DoctorSerial).filter(models.DoctorSerial.id == reviewin.orderId).first()

    doctor_serial.reviewchecked = 1
    db.add(doctor_serial)
    db.commit()
    db.add(review)
    db.commit()

    return {"details":"success"}

