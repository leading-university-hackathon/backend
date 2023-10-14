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
    name:str
    url:str

    class Config:
        orm_mode = True







class UserSignup(BaseModel):
    email:EmailStr
    password:str
    name:str
    url:str

class UserOut(BaseModel):
    name:str
    email:EmailStr

class UserSignin(BaseModel):
    email:EmailStr
    password:str


