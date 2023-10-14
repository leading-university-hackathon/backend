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
    
    hospital = db.query(models.HOSPITAL).join(models.User).filter(models.User.id==current_user.id).first()

    diagnosis = models.Diagnosis(**addDiagnosis.model_dump(), hospital_id=hospital.id)

    db.add(diagnosis)
    db.commit()
    db.refresh(diagnosis)

    return {"details":"success"}

@router.get("/diagnosis/all")
def getAllDiagnosis(db:Session=Depends(database.get_db), current_user: models.User = Depends(oauth2.getCurrentUser)):
    if current_user.role!="USER":
        raise HTTPException(status_code=404, detail="error")

    diagnosisAll = db.query(models.Diagnosis).all()

    diagnosisAllOut = []

    for i in diagnosisAll:
        diagnosisOut = schemas.DiagnosisOut( name=i.name, description=i.description,price=i.price,hospitalName=i.hospital.hospitalName,rating =4)
        diagnosisAllOut.append(diagnosisOut)

    return diagnosisAllOut