import models, schemas, utils, oauth2, database
from fastapi import Depends, FastAPI, status,Response, HTTPException, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["reminder"],
    prefix="/reminder"
)



@router.post("/add",status_code=201)
def add_medicine_reminder(reminderIn:schemas.MedicineReminderIn, db:Session=Depends(database.get_db), current_user: models.User = Depends(oauth2.getCurrentUser)):

    if current_user.role!="USER":
        raise HTTPException(status_code=404, detail="error")

    reminder = models.MedicineReminder(**reminderIn.model_dump(), user_id=current_user.id)

    db.add(reminder)
    db.commit()
    db.refresh(reminder)

    return {"details":"success"}

@router.delete("/delete/{id}",status_code=202)
def delete_reminder(id:int, db:Session=Depends(database.get_db), current_user: models.User = Depends(oauth2.getCurrentUser)):

    if current_user.role!="USER":
        raise HTTPException(status_code=404, detail="error")

    reminder = db.query(models.MedicineReminder).filter(models.MedicineReminder.id == id).first()

    db.delete(reminder)
    db.commit()

    return {"details":"deleted"}