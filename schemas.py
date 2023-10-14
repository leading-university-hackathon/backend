from datetime import date, datetime, time

from typing import List, Optional
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token:str
    token_type: str
    email:EmailStr
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

class availableOfflineTime(BaseModel):
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

class DoctorOut(BaseModel):
    user:UserOut
    bio:str
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


class addDoctorSerial(BaseModel):
    type: str
    price: int
    appointmentDate: date
    prescription: str
    time: float
    doctor_id: int
