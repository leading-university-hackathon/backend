
from fastapi import Depends, FastAPI, status,Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware


import models,utils
from database import engine, SessionLocal
from router import auth, doctor, doctor_serial, review,medicine_reminder

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit,logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown())



app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def start_scheduler():
    logging.info("Starting Scheduler")
    trigger = IntervalTrigger(minutes=1)  # Run every 1 minute
    scheduler.add_job(utils.sendMedincineReminders, trigger=trigger)
    logging.info("Finishing Scheduler")


app.include_router(auth.router)
app.include_router(doctor.router)
app.include_router(doctor_serial.router)
app.include_router(review.router)
app.include_router(medicine_reminder.router)