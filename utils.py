from datetime import date, timedelta,datetime
from enum import Enum
import models,const,database
from passlib.context import CryptContext
pwdContext = CryptContext(schemes=["bcrypt"], deprecated ="auto")
import logging,httpx
from sqlalchemy.orm import Session
from fastapi import Depends

logging.basicConfig(level=logging.INFO)

def hash(password:str):
    return pwdContext.hash(password)

def verify(plainPassword, hashedPassword):
    return pwdContext.verify(plainPassword, hashedPassword)

class Day(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

def current_date(day):
    input_day = Day[day.upper()]
    print(input_day)
    today = date.today()
    current_week_date = today - timedelta(days=today.weekday() - input_day.value)
    return current_week_date

def next_date(day):
    input_day = Day[day.upper()]
    today = date.today()
    days_until_next_day = (input_day.value - today.weekday() + 7) % 7
    next_week_date = today + timedelta(days=days_until_next_day)
    return next_week_date

def convert_double_to_time(time):
    hours = int(time)
    minutes = int((time - hours) * 100)

    if hours >= 12:
        if hours > 12:
            hours -= 12
        return time(hours, minutes).replace(hour=12, minute=minutes, second=0)
    else:
        return time(hours, minutes, second=0)

def convert_time_to_double(local_time):
    hours = local_time.hour
    minutes = local_time.minute

    time_in_double = hours + (minutes / 100.0)

    return time_in_double

def convert_string_to_local_time(time_string):
    local_time = datetime.strptime(time_string, "%H:%M").time()
    return local_time


def set_new_serial_time(time:float):
        int_time = int(time)
        frac_time = time - int_time
        frac_time += const.perConsultTime / 100.0

        if frac_time >= 0.6:
            int_time += 1
            frac_time -= 0.6

        return int_time + frac_time

def setSerialTime(doctor: models.Doctor):
    
    current_date = datetime.now().date()
    
    for i in doctor.availableOfflineTimes:
        start_time = i.start_time
        end_time = i.end_time
        available_time = i.available_time

        if i.date==current_date:

            current_time = convert_time_to_double(datetime.now().time())

            if available_time<current_time:
                available_time = current_time

            if (start_time<end_time and available_time>end_time) or (start_time>end_time and available_time>end_time and available_time<start_time):
                i.available_time = -1.0
            else:
                i.available_time = available_time

    for i in doctor.availableOnlineTimes:
        start_time = i.start_time
        end_time = i.end_time
        available_time = i.available_time

        if i.date==current_date:
            current_time = convert_time_to_double(datetime.now().time())

            if available_time<current_time:
                available_time = current_time

            if (start_time<end_time and available_time>end_time) or (start_time>end_time and available_time>end_time and available_time<start_time):
                i.available_time = -1.0
            else:
                i.available_time = available_time


def convert_int_to_day(days):
    day_map = {
        "0": "Sunday",
        "1": "Monday",
        "2": "Tuesday",
        "3": "Wednesday",
        "4": "Thursday",
        "5": "Friday",
        "6": "Saturday"
    }

    part = days.split(",")
    day_list = [day_map[i] for i in part if i in day_map]

    return day_list


def convert_string_to_local_time(time_string):
    time_format = "%H:%M" 
    
    try:
        local_time = datetime.strptime(time_string, time_format).time()
        return local_time
    except ValueError:
        return None

MESSAGE_API = "http://bulksmsbd.net/api/smsapi?api_key={password}&type=text&number={number}&senderid={user}&message={message}"

async def send_message(medicine: str, time: str, contact_no: str):
    message = f"You have to take {medicine} at {time}. Kindly take it"
    url = MESSAGE_API.format(
        user="8809617613117",  
        password="huCqtTC4s44wPSkNKI0b",  
        number=contact_no,
        message=message
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        if 200 <= response.status_code < 300:
            logging.info("Message sent successfully")
        else:
            logging.info("Error: Message not sent")

            
async def send_message(medicine: str, time: str, contact_no: str):
    message = f"You have to take {medicine} at {time}. Kindly take it"
    url = MESSAGE_API.format(
        user="8809617613117",  
        password="huCqtTC4s44wPSkNKI0b",  
        number=contact_no,
        message=message
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        if 200 <= response.status_code < 300:
            logging.info("Message sent successfully")
        else:
            logging.info("Error: Message not sent")

async def sendSingleMedicineReminder(medicineReminder:models.MedicineReminder):
    time = convert_string_to_local_time(medicineReminder.time).strftime("%H:%M")
  
    days = convert_int_to_day(medicineReminder.days)
    current_time = datetime.now().strftime("%H:%M")
   

    for day in days:
        current_day = datetime.now().strftime("%A")
        if day.upper()==current_day.upper() and time == current_time:
            try:
                await send_message(medicineReminder.description, medicineReminder.time, medicineReminder.user.phone)
            except:

                logging.info("Error sending message")

async def sendMedincineReminders():
    db = database.SessionLocal()
    medicineReminders = db.query(models.MedicineReminder).all()
    for medicineReminder in medicineReminders:
        await sendSingleMedicineReminder(medicineReminder)

    
