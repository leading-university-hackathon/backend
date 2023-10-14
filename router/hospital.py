import models, schemas, utils, oauth2, database
from fastapi import Depends, FastAPI, status,Response, HTTPException, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/hospital",
    tags=["hospital"]
)

