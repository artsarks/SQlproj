from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Car(Base):
    __tablename__ = "cars"
    __table_args__ = {'schema': 'public'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String, unique=True, nullable=False)
    brand = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    owner_name = Column(String, nullable=False)
    orders = relationship("Order", back_populates="car")

class Order(Base):
    __tablename__ = "orders"
    __table_args__ = {'schema': 'public'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    car_id = Column(Integer, ForeignKey("public.cars.id"), nullable=False)  # Указание схемы в ForeignKey
    mechanic_id = Column(Integer, ForeignKey("public.mechanics.id"), nullable=False)  # Указание схемы
    issue_date = Column(Date, nullable=False)
    work_type = Column(String, nullable=False)
    cost = Column(Float, nullable=False)
    planned_end_date = Column(Date, nullable=False)
    actual_end_date = Column(Date, nullable=True)
    car = relationship("Car", back_populates="orders")
    mechanic = relationship("Mechanic", back_populates="orders")

class Mechanic(Base):
    __tablename__ = "mechanics"
    __table_args__ = {'schema': 'public'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    experience = Column(Integer, nullable=False)
    rank = Column(Integer, nullable=False)
    orders = relationship("Order", back_populates="mechanic")
