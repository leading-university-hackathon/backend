from random import randrange
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

import models, schemas, utils, oauth2, database
from fastapi import Depends, FastAPI, status,Response, HTTPException, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["authentication"]
)

@router.post("/signin", response_model=schemas.Token)
def login(userCredentials:schemas.UserSignin, db:Session = Depends(database.get_db)):
     
    user = db.query(models.User).filter(models.User.email == userCredentials.email ).first()
    if not user:
        raise HTTPException(status_code= 404, 
                            detail=f"error")
    
    if not utils.verify(userCredentials.password, user.password):
        raise HTTPException(status_code=404, detail="error")
    
    

    accessToken = oauth2.createAccessToken( data = {"id":user.id, 
                                                    "email":user.email,
                                                    "name":user.name,
                                                    "url":user.url})
    tokenData = schemas.Token(access_token=accessToken,token_type="bearer", email=user.email, name=user.name, url=user.url)
    return tokenData



@router.post("/signup",
             status_code= 201,
             response_model= schemas.UserOut)
def login(user:schemas.UserSignup, db:Session = Depends(database.get_db)):
    user.password = utils.hash(user.password)
    user = models.User(**user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user






