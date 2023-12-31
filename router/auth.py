import models, schemas, utils, oauth2, database
from fastapi import Depends,HTTPException, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["authentication"]
)

@router.post("/signin", response_model=schemas.Token)
def signin(userCredentials:schemas.UserSignin, db:Session = Depends(database.get_db)):
     
    user = db.query(models.User).filter(models.User.email == userCredentials.email ).first()
    if not user:
        raise HTTPException(status_code= 404, 
                            detail=f"error")
    
    if not utils.verify(userCredentials.password, user.password):
        raise HTTPException(status_code=404, detail="error")
    
    

    accessToken = oauth2.createAccessToken(data = {"id":user.id, 
                                                    "email":user.email,
                                                    "role":user.role,
                                                    "name":user.name,
                                                    "phone":user.phone})
    tokenData = schemas.Token(id=user.id ,accessToken=accessToken,token_type="Bearer", email=user.email, name=user.name, url=user.url,phone = user.phone,role=user.role)

    return tokenData



@router.post("/signup",
             status_code= 201,
             response_model= schemas.UserOut)
def signup(user:schemas.UserSignup, db:Session = Depends(database.get_db)):
    user.password = utils.hash(user.password)
    user = models.User(**user.model_dump())
    user.role ="USER"
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/doctor/signup")
def doctor_signup(doctorsignup:schemas.DoctorSignUp, db:Session = Depends(database.get_db)):

    user = models.User(**doctorsignup.user.model_dump())
    user.password = utils.hash(user.password)
    user.role ="DOCTOR"
    db.add(user)
    db.commit()
    db.refresh(user)

    doctor = models.Doctor(user=user, bio=doctorsignup.bio, expertise=doctorsignup.expertise, current_hospital=doctorsignup.current_hospital, place=doctorsignup.place, online_fee=doctorsignup.online_fee, offline_fee=doctorsignup.offline_fee, degrees=doctorsignup.degrees)
    doctor.balance=0
    doctor.rating =0.0
    db.add(doctor)
    db.commit()
    db.refresh(doctor)

    for i in doctorsignup.availableOnlineTimes:
        availableOnlineTime = models.availableOnlineTime(doctor_id=doctor.id, date=utils.current_date(i.day), day= i.day,start_time=i.start_time, end_time=i.end_time, available_time=i.start_time)
        db.add(availableOnlineTime)
        db.commit()
        db.refresh(availableOnlineTime)

    for i in doctorsignup.availableOfflineTimes:
        availableOfflineTime = models.availableOfflineTime(doctor_id=doctor.id, date=utils.current_date(i.day), day=i.day, start_time=i.start_time, end_time=i.end_time, available_time=i.start_time)
        db.add(availableOfflineTime)
        db.commit()
        db.refresh(availableOfflineTime)

    raise HTTPException(status_code=201, detail="Doctor Created")
    

@router.post("/hospital/signup")
def hospital_signup(hospitalsignup:schemas.HospitalSignUp, db:Session = Depends(database.get_db)):

    user = models.User(**hospitalsignup.user.model_dump())
    user.password = utils.hash(user.password)
    user.role ="HOSPITAL"
    db.add(user)
    db.commit()
    db.refresh(user)

    hospital = models.Hospital(user=user, bio=hospitalsignup.bio, hospitalName=hospitalsignup.hospitalName, place=hospitalsignup.place)

    db.add(hospital)
    db.commit()
    db.refresh(hospital)

    raise HTTPException(status_code=201, detail="Hospital Created")


