from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://admin:smart@localhost/ProjectAS_DB"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Car(db.Model):
    __tablename__ = "cars"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.String, unique=True, nullable=False)
    brand = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    owner_name = db.Column(db.String, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/cars', methods=['POST'])
def create_car():
    data = request.get_json()
    new_car = Car(
        number=data['number'],
        brand=data['brand'],
        year=data['year'],
        owner_name=data['owner_name']
    )
    db.session.add(new_car)
    db.session.commit()
    return jsonify({"message": "Car created successfully"}), 201

@app.route('/cars', methods=['GET'])
def get_cars():
    cars = Car.query.all()
    return jsonify([{
        "id": car.id,
        "number": car.number,
        "brand": car.brand,
        "year": car.year,
        "owner_name": car.owner_name
    } for car in cars])

@app.route('/cars/<int:car_id>', methods=['GET'])
def get_car(car_id):
    car = Car.query.get(car_id)
    if not car:
        return jsonify({"message": "Car not found"}), 404
    return jsonify({
        "id": car.id,
        "number": car.number,
        "brand": car.brand,
        "year": car.year,
        "owner_name": car.owner_name
    })

@app.route('/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    data = request.get_json()
    car = Car.query.get(car_id)
    if not car:
        return jsonify({"message": "Car not found"}), 404
    car.number = data.get('number', car.number)
    car.brand = data.get('brand', car.brand)
    car.year = data.get('year', car.year)
    car.owner_name = data.get('owner_name', car.owner_name)
    db.session.commit()
    return jsonify({"message": "Car updated successfully"})

@app.route('/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    car = Car.query.get(car_id)
    if not car:
        return jsonify({"message": "Car not found"}), 404
    db.session.delete(car)
    db.session.commit()
    return jsonify({"message": "Car deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)


"""
~ curl -X POST http://127.0.0.1:5000/cars -H "Content-Type: application/json" -d '{
  "number": "A123BC",
  "brand": "Toyota",
  "year": 2015,
  "owner_name": "John Doe"
}'
{
  "message": "Car created successfully"
}
➜  ~ curl http://127.0.0.1:5000/cars

[
  {
    "brand": "Toyota",
    "id": 1,
    "number": "A123BC",
    "owner_name": "John Doe",
    "year": 2015
  }
]
➜  ~ curl http://127.0.0.1:5000/cars/1

{
  "brand": "Toyota",
  "id": 1,
  "number": "A123BC",
  "owner_name": "John Doe",
  "year": 2015
}
➜  ~ 
"""