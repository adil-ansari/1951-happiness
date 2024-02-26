from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from models import Employee
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/api", tags=["employees"])

@router.get("/get", response_model=Employee)
def get_employee(cursor = Depends(get_db)):
    cursor.execute("SELECT * FROM employee")
    employee = cursor.fetchone()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


class EmployeeRating(BaseModel):
    employee_id: int
    employee_name: str
    employee_avatar: str
    average_rating: int

@router.get("/chart/topPerformer", response_model=List[EmployeeRating])
def get_top_rated_employees(cursor = Depends(get_db)):
    cursor.execute("""
        SELECT e.id AS employee_id, e.name AS employee_name, ROUND(AVG(r.rating_val))::INT AS average_rating,e.employee_avatar
        FROM Rating r
        JOIN Employee e ON r.employee_id = e.id
        WHERE r.rating_date >= CURRENT_DATE - INTERVAL '6 DAY' AND r.rating_date <= CURRENT_DATE
        GROUP BY e.id, e.name
        ORDER BY average_rating DESC
        LIMIT 3;
    """)
    top_rated_employees = cursor.fetchall()
    return top_rated_employees

class TopDrink(BaseModel):
    drink_name: str
    drink_count: int

@router.get("/chart/bestSellers", response_model=List[TopDrink])
def get_top_drinks(cursor = Depends(get_db)):
    cursor.execute("""
        SELECT drink_name, COUNT(*) AS drink_count
        FROM "order"
        GROUP BY drink_name
        ORDER BY drink_count DESC
        LIMIT 3
    """)
    top_drinks = cursor.fetchall()
    return top_drinks