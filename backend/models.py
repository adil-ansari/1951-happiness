from pydantic import BaseModel
from typing import Optional
from datetime import date

class Employee(BaseModel):
    id: int
    name: str
    age: int
    native_language: str

class Rating(BaseModel):
    id: int
    rating_val: int
    employee_id: int
    order_id: int
    comments: Optional[str]
    rating_date: date

class Order(BaseModel):
    id: int
    drink_name: str
    order_date: date
