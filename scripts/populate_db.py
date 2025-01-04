import requests
from faker import Faker

fake = Faker()
url = "http://127.0.0.1:5000/cars"

def generate_car_data():
    return {
        "number": fake.license_plate(),
        "brand": fake.company(),
        "year": fake.year(),
        "owner_name": fake.name()
    }

def populate_db(n):
    for _ in range(n):
        car_data = generate_car_data()
        response = requests.post(url, json=car_data)
        if response.status_code == 201:
            print(f"Added: {car_data}")
        else:
            print(f"Failed to add: {car_data}, Error: {response.text}")

if __name__ == "__main__":
    populate_db(100)
