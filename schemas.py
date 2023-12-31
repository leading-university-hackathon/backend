from datetime import date

from typing import List
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    id :int
    accessToken:str
    token_type: str
    email:EmailStr
    role:str
    phone:str
    name:str
    url:str


class TokenData(BaseModel):
    id:int


class payload(BaseModel):
    id:int
    email:EmailStr
    role:str

    class Config:
        orm_mode = True



class UserSignup(BaseModel):
    email:EmailStr
    password:str
    name:str
    url:str
    phone:str

class UserOut(BaseModel):
    id:int
    name:str
    email:EmailStr
    url:str
    role:str
    phone:str

class UserSignin(BaseModel):
    email:EmailStr
    password:str

class availableOnlineTime(BaseModel):
    date:date
    day:str
    start_time:float
    end_time:float
    available_time:float
    class Config():
        orm_mode = True

class availableOnlineTimeOut(BaseModel):
    id:int
    date:date
    day:str
    start_time:float
    end_time:float
    available_time:float
    class Config():
        orm_mode = True

class availableOfflineTime(BaseModel):
    date:date
    day:str
    start_time:float
    end_time:float
    available_time:float
    class Config():
        orm_mode = True

class availableOfflineTimeOut(BaseModel):
    id:int
    date:date
    day:str
    start_time:float
    end_time:float
    available_time:float
    class Config():
        orm_mode = True


class DoctorSignUp(BaseModel):
    user:UserSignup
    bio:str
    bmdc:str
    expertise:str
    current_hospital:str
    place:str
    online_fee:int
    offline_fee:int
    degrees:str
    availableOnlineTimes:List[availableOnlineTime]
    availableOfflineTimes:List[availableOfflineTime]

    class Config():
        orm_mode = True

class HospitalSignUp(BaseModel):
    user:UserSignup
    bio:str
    hospitalName:str
    place:str
    class Config():
        orm_mode = True

class DoctorOut(BaseModel):
    user:UserOut
    bio:str
    expertise:str
    current_hospital:str
    place:str
    online_fee:int
    offline_fee:int
    degrees:str
    availableOnlineTimes:List[availableOnlineTimeOut]
    availableOfflineTimes:List[availableOfflineTimeOut]
    rating:float
    balance:int

    class Config():
        orm_mode = True


class addDoctorSerial(BaseModel):
    type: str
    price: int
    appointmentDate: date
    time: float
    doctor_id: int

class DoctorSerialOut(BaseModel):
    id:int
    price:int
    type:str
    user_id:int
    doctor_id:int
    doctorName:str
    patientName:str
    time:float
    appointmentDate:date
    class Config():
        orm_mode = True


class Prescription(BaseModel):
    prescription :str

class CompletedPrescription(BaseModel):
    prescription:str
    doctorId:int
    doctorName:str

    class Config():
        orm_mode = True

class ReviewIn(BaseModel):
    subjectId:int
    orderId:int

class ReviewOut(BaseModel):
    id:int
    subjectId:int
    reviewerId:int
    reviewerName:str
    review:str
    starCount:int


    class Config():
        orm_mode = True

class ReviewPending(BaseModel):
    orderId:int
    subjectId:int
    subjectName:str

    class Config():
        orm_mode = True

class MedicineReminderIn(BaseModel):
    description:str
    time:str
    days:str

class MedicineReminderOut(BaseModel):
    id:int
    description:str
    time:str
    days:str

    class Config():
        orm_mode = True

class addDiagnosis(BaseModel):
    name:str
    price:int
    description:str

class DiagnosisOut(BaseModel):
    name:str
    description:str
    price:int
    hospitalName:str
    rating:float