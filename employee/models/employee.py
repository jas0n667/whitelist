from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import uuid4


class EmployeeBase(BaseModel):
    full_name: str = Field(
        ...,
        description="Full name of the employee.",
        example="John Doe"
    )
    iin: str = Field(
        ...,
        
        description="Individual Identification Number (IIN), exactly 12 digits.",
        example="123456789012"
    )


class EmployeeRead(EmployeeBase):
    id: str






















    # weekday: Optional[int] = Field(
    #     default=None,
    #     ge=1,
    #     le=7,
    #     description="The day of the week as a number (1 for Monday, 7 for Sunday)."
    # )
    # month: Optional[int] = Field(
    #     default=None,
    #     ge=1,
    #     le=12,
    #     description="The month of the year as a number (1 for January, 12 for December)."
    # )
    # year: Optional[int] = Field(
    #     default=None,
    #     ge=1,
    #     le=9999,
    #     description="The year in YYYY format."
    # )


# from pydantic import BaseModel, Field, root_validator
# from typing import Optional, Literal, Union

# class DateSelector(BaseModel):
#     specific_day: Optional[int] = Field(
#         default=None,
#         ge=1,
#         le=7,
#         description="Specific day of the week as a number (1 for Monday, 7 for Sunday)."
#     )
#     recurring_last_week: Optional[Literal["last_week"]] = Field(
#         default=None,
#         description="Recurring event on the specified day of the last week of the month."
#     )
#     recurring_day: Optional[int] = Field(
#         default=None,
#         ge=1,
#         le=7,
#         description="The day of the week for recurring events (1 for Monday, 7 for Sunday)."
#     )

#     @root_validator
#     def validate_choices(cls, values):
#         specific_day = values.get("specific_day")
#         recurring_last_week = values.get("recurring_last_week")
#         recurring_day = values.get("recurring_day")

#         if specific_day and (recurring_last_week or recurring_day):
#             raise ValueError("You can only select a specific day OR a recurring event, not both.")
#         if recurring_last_week and not recurring_day:
#             raise ValueError("Recurring last week option requires specifying a day (recurring_day).")
#         return values
