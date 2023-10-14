
from fastapi import Depends, FastAPI, status,Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware


import models
from database import engine, SessionLocal
from router import auth, doctor, doctor_serial, review

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# models.Base.metadata.drop_all(bind=engine)

models.Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(doctor.router)
app.include_router(doctor_serial.router)
app.include_router(review.router)