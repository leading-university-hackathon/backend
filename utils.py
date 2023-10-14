from datetime import date, timedelta,datetime
from enum import Enum
import models,const
from passlib.context import CryptContext
pwdContext = CryptContext(schemes=["bcrypt"], deprecated ="auto")

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

def convert_int_to_day(days):
    day_mapping = {
        0: "Sunday",
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday"
    }


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