from datetime import date
import models,database
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

def findAvgRating(doctorId,db:Session=Depends(database.get_db)):

    average_star_count = db.query(func.avg(models.Review.starCount).label("average_star_count")) \
    .filter(models.Review.subject_id == doctorId) \
    .scalar()

    return average_star_count

