from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from models import Rating

router = APIRouter(prefix="/dashboard", tags=["orders"])

class OrderLookupResponse(BaseModel):
    id: int
    drink_name: str
    employee_name: str
    employee_id: int

# class RatingCreate(BaseModel):
#     order_id: int = Field(alias='id')
#     rating_val: int
#     employee_id: int
#     comments: Optional[str] = None
#     rating_date: date

@router.get("/lookup/{order_id}", response_model=OrderLookupResponse)
def get_order_lookup(order_id: int, cursor = Depends(get_db)):
    cursor.execute("""
        SELECT o.id, o.drink_name, e.name AS employee_name, e.id AS employee_id
        FROM "order" o
        JOIN employee e ON o.employee_id = e.id
        WHERE o.id = %s
    """, (order_id,))
    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Order not found")
    return result

@router.post("/rate", response_model=Rating)
def create_rating(rating: Rating, cursor = Depends(get_db)):
    cursor.execute("""
        INSERT INTO rating (id, rating_val, employee_id, order_id, comments, rating_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id, rating_val, employee_id, order_id, comments, rating_date
    """, (rating.id, rating.rating_val, rating.employee_id, rating.order_id, rating.comments, rating.rating_date))
    new_rating = cursor.fetchone()
    cursor.connection.commit()
    return new_rating