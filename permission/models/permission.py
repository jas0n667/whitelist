from pydantic import BaseModel, Field, model_validator, root_validator
from typing import Optional
from datetime import datetime, timedelta
from enum import Enum
from fastapi import HTTPException


class TimeRangeModel(BaseModel):
    start_year: int = Field(..., ge=1900, description="Год")
    start_month: int = Field(..., ge=1, le=12, description="Месяц")
    start_day: int = Field(..., ge=1, le=31, description="День")

    end_year: int = Field(..., ge=1900, description="Год окончания")
    end_month: int = Field(..., ge=1, le=12, description="Месяц окончания")
    end_day: int = Field(..., ge=1, le=31, description="День окончания")
    
    @model_validator(mode="after")
    def validate_time_order(cls, values):
        try:
            start = datetime(
                values.start_year,
                values.start_month,
                values.start_day,
            )
        except ValueError:
            raise ValueError("Некорректная дата начала: Проверьте день, месяц и год.")
        
        try:            
            end = datetime(
                values.end_year,
                values.end_month,
                values.end_day,
            )   
        except ValueError:
            raise ValueError("Некорректная дата окончания: Проверьте день, месяц и год.")
        
        if end <= start:
            raise ValueError("Дата и время окончания должны быть позже даты и времени начала.")
        return values
    
    def is_current_time_in_range(self, current_time: datetime) -> bool:
        current_time = datetime.now()
        start_time = datetime(
            self.start_year, self.start_month, self.start_day)
        end_time = datetime(
            self.end_year, self.end_month, self.end_day)
        return start_time <= current_time <= end_time


class WeekdayEnum(str, Enum):
    monday = "Monday"
    tuesday = "Tuesday"
    wednesday = "Wednesday"
    thursday = "Thursday"
    friday = "Friday"
    saturday = "Saturday"
    sunday = "Sunday"

# Модель для графика работы
class TimeSchedule(BaseModel):
    start_hour: int = Field(..., ge=0, le=23, description="Час")
    start_minute: int = Field(..., ge=0, le=59, description="Минута начала")
    end_hour: int = Field(..., ge=0, le=23, description="Час окончания")
    end_minute: int = Field(..., ge=0, le=59, description="Минута окончания")
    
    @model_validator(mode="after")
    def validate_time(cls, values):
        start_hour = values.start_hour
        start_minute = values.start_minute
        end_hour = values.end_hour
        end_minute = values.end_minute

        # Проверка, чтобы время начала и окончания не были одинаковыми
        if start_hour == end_hour and start_minute == end_minute:
            raise ValueError("Время начала и окончания не могут быть одинаковыми.")

        # Проверка, чтобы end_hour не был меньше start_hour
        if end_hour < start_hour or (end_hour == start_hour and end_minute < start_minute):
            raise ValueError("Время окончания не может быть раньше времени начала.")

        return values
    

# Основная модель с разрешениями
class EmployeePermission(TimeRangeModel):
    schedule: TimeSchedule  
    weekday: Optional[WeekdayEnum] = None  
    is_last_weekday_of_month: bool = False 
    
    def get_last_weekday_of_month(self, year: int, month: int, weekday: WeekdayEnum) -> datetime:
        """
        Возвращает дату последнего дня недели (например, последний четверг месяца).
        """
        # Находим последний день месяца
        last_day = datetime(year, month + 1, 1) - timedelta(days=1)
        # Сдвигаем на предыдущий день недели
        offset = (last_day.weekday() - WeekdayEnum[weekday].value) % 7
        last_weekday = last_day - timedelta(days=offset)
        return last_weekday

    def is_valid_time(self, check_datetime: datetime) -> bool:
        """
        Проверка, входит ли указанное время в допустимый интервал.
        """
        # Преобразуем время начала и конца в datetime для сравнения
        try:
            # Преобразуем дату начала и конца в объекты datetime
            start_time = datetime(
                self.start_year, self.start_month, self.start_day,
                self.schedule.start_hour, self.schedule.start_minute
            )
            end_time = datetime(
                self.end_year, self.end_month, self.end_day,
                self.schedule.end_hour, self.schedule.end_minute
            )
        except ValueError as e:
            raise ValueError(f"Некорректная дата: {e}")
        
        # Проверка, что текущее время в пределах диапазона
        if not (start_time <= check_datetime <= end_time):
            return False

        # Проверка, совпадает ли день недели с разрешенным
        if self.weekday:
            if self.is_last_weekday_of_month:
                
                last_weekday_of_month = self.get_last_weekday_of_month(
                    check_datetime.year, check_datetime.month, self.weekday
                )
                if check_datetime.date() != last_weekday_of_month.date():
                    return False
            else:
                if check_datetime.strftime("%A") != self.weekday.value:
                    return False

        # Проверка, что текущее время находится в пределах рабочего интервала
        schedule_start_time = timedelta(hours=self.schedule.start_hour, minutes=self.schedule.start_minute)
        schedule_end_time = timedelta(hours=self.schedule.end_hour, minutes=self.schedule.end_minute)
        current_time = timedelta(hours=check_datetime.hour, minutes=check_datetime.minute)

        if not (schedule_start_time <= current_time <= schedule_end_time):
            return False

        return True


class EmployeePermissionDate(EmployeePermission):
    employee_id: str



