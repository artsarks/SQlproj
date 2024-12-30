from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import SessionLocal
import crud

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/cars/")
def create_new_car(brand: str, license_plate: str, year: int, owner_name: str, db: Session = Depends(get_db)):
    try:
        return crud.create_car(db, brand=brand, license_plate=license_plate, year=year, owner_name=owner_name)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Car with license plate '{license_plate}' already exists.",
        )

@app.get("/cars/")
def read_cars(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_cars(db, skip=skip, limit=limit)

@app.post("/mechanics/")
def create_new_mechanic(name: str, experience: int, rank: int, db: Session = Depends(get_db)):
    try:
        return crud.create_mechanic(db, name=name, experience=experience, rank=rank)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Mechanic with name '{name}' might already exist or violates constraints.",
        )

@app.get("/mechanics/")
def read_mechanics(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_mechanics(db, skip=skip, limit=limit)

@app.post("/orders/")
def create_new_order(cost: float, issue_date, work_type: str, planned_end_date, car_id: int, mechanic_id: int, db: Session = Depends(get_db)):
    try:
        return crud.create_order(
            db,
            cost=cost,
            issue_date=issue_date,
            work_type=work_type,
            planned_end_date=planned_end_date,
            car_id=car_id,
            mechanic_id=mechanic_id,
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Order violates constraints. Please check car_id or mechanic_id.",
        )

@app.get("/orders/")
def read_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_orders(db, skip=skip, limit=limit)
