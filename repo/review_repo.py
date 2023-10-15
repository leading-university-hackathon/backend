import models,database
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

def findAvgRating(doctorId,db:Session=Depends(database.get_db)):

    average_star_count = db.query(func.avg(models.Review.starCount).label("average_star_count")) \
    .filter(models.Review.subject_id == doctorId) \
    .scalar()

    if average_star_count is None:
        print("Y")
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    return average_star_count

