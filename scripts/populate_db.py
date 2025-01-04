from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
import random
from app.models import Base, Car, Mechanic, Order 


DATABASE_URL = "postgresql+psycopg2://admin:smart@localhost/ProjectAS_DB"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


fake = Faker()

def populate_mechanics(n=10):
    mechanics = []
    for _ in range(n):
        mechanic = Mechanic(
            name=fake.name(),
            experience=random.randint(1, 30), 
            rank=random.randint(1, 5)
        )
        mechanics.append(mechanic)
    session.add_all(mechanics)
    session.commit()
    print(f"{n} mechanics added.")
    return mechanics

def populate_cars(n=10):
    cars = []
    for _ in range(n):
        car = Car(
            number=fake.license_plate(),
            brand=fake.company(),
            year=random.randint(1990, 2023),
            owner_name=fake.name()
        )
        cars.append(car)
    session.add_all(cars)
    session.commit()
    print(f"{n} cars added.")
    return cars

def populate_orders(cars, mechanics, n=20):
    orders = []
    for _ in range(n):
        order = Order(
            car_id=random.choice(cars).id,
            mechanic_id=random.choice(mechanics).id,
            issue_date=fake.date_this_year(),
            work_type=fake.word(),
            cost=round(random.uniform(1000, 50000), 2),
            planned_end_date=fake.date_this_month(),
            actual_end_date=None if random.random() > 0.5 else fake.date_this_month()
        )
        orders.append(order)
    session.add_all(orders)
    session.commit()
    print(f"{n} orders added.")

if __name__ == "__main__":
    mechanics = populate_mechanics(10)
    cars = populate_cars(10)
    populate_orders(cars, mechanics, 20)
