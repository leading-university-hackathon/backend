import models,database
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

def findAvgRating(doctorId,db:Session=Depends(database.get_db)):

    average_star_count = db.query(func.avg(models.Review.starCount)).label('average') \
    .filter(models.Review.subject_id == doctorId)

    return average_star_count

