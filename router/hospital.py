import models, schemas, utils, oauth2, database
from fastapi import Depends, FastAPI, status,Response, HTTPException, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/hospital",
    tags=["hospital"]
)

@router.post("/add/diagnosis")
def add_diagnosis(addDiagnosis:schemas.addDiagnosis, db:Session=Depends(database.get_db), current_user: models.User = Depends(oauth2.getCurrentUser)):

    if current_user.role!="HOSPITAL":
        raise HTTPException(status_code=404, detail="error")

    diagnosis = models.Diagnosis(**addDiagnosis.model_dump(), hospital_id=current_user.id)

    db.add(diagnosis)
    db.commit()
    db.refresh(diagnosis)

    return {"details":"success"}

