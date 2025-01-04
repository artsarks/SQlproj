from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import json

app = Flask(__name__)

# Конфигурация приложения и базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://admin:smart@localhost/ProjectAS_DB"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Модели базы данных
class Car(db.Model):
    __tablename__ = "cars"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.String, unique=True, nullable=False)
    brand = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    owner_name = db.Column(db.String, nullable=False)


class Mechanic(db.Model):
    __tablename__ = "mechanics"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    rank = db.Column(db.Integer, nullable=False)


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    mechanic_id = db.Column(db.Integer, db.ForeignKey('mechanics.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    service = db.Column(db.String, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    details = db.Column(db.JSON, nullable=True)  # Поле для хранения JSON
    car = db.relationship('Car', backref='orders')
    mechanic = db.relationship('Mechanic', backref='orders')


# Создание всех таблиц
with app.app_context():
    db.create_all()


# SELECT ... WHERE (с несколькими условиями)
@app.route('/cars/filter', methods=['GET'])
def filter_cars():
    filters = []
    if 'brand' in request.args:
        filters.append(Car.brand == request.args['brand'])
    if 'year' in request.args:
        filters.append(Car.year == request.args['year'])
    cars = Car.query.filter(*filters).all()
    return jsonify([{
        "id": car.id,
        "number": car.number,
        "brand": car.brand,
        "year": car.year,
        "owner_name": car.owner_name
    } for car in cars])


# JOIN (связь машины с таблицей заказов)
@app.route('/cars_with_orders', methods=['GET'])
def cars_with_orders():
    records = db.session.query(Car, Order).join(Order, Car.id == Order.car_id).all()
    result = []
    for car, order in records:
        result.append({
            "car": {
                "id": car.id,
                "number": car.number,
                "brand": car.brand,
                "year": car.year,
                "owner_name": car.owner_name
            },
            "order": {
                "id": order.id,
                "car_id": order.car_id,
                "mechanic_id": order.mechanic_id,
                "date": order.date,
                "service": order.service,
                "cost": order.cost,
                "details": order.details
            }
        })
    return jsonify(result)


# UPDATE с нетривиальным условием
@app.route('/cars/update_year', methods=['POST'])
def update_car_year():
    data = request.get_json()
    car_id = data.get('car_id')
    new_year = data.get('new_year')
    car = Car.query.filter(Car.id == car_id, Car.year < new_year).first()
    if not car:
        return jsonify({"message": "Car not found or condition not met"}), 404
    car.year = new_year
    db.session.commit()
    return jsonify({"message": "Car year updated successfully"})


# GROUP BY (группировка машин по марке)
@app.route('/cars/group_by_brand', methods=['GET'])
def group_by_brand():
    records = db.session.query(Car.brand, db.func.count(Car.id)).group_by(Car.brand).all()
    result = {record[0]: record[1] for record in records}
    return jsonify(result)


# Сортировка по полям (например, по году)
@app.route('/cars/sort', methods=['GET'])
def sort_cars():
    sort_by = request.args.get('field')
    if sort_by not in ['number', 'brand', 'year', 'owner_name']:
        return jsonify({"message": "Invalid field for sorting"}), 400
    cars = Car.query.order_by(getattr(Car, sort_by)).all()
    return jsonify([{
        "id": car.id,
        "number": car.number,
        "brand": car.brand,
        "year": car.year,
        "owner_name": car.owner_name
    } for car in cars])


# Поиск в JSONB
@app.route('/orders/search', methods=['GET'])
def search_orders():
    query = request.args.get('q')  # Получаем поисковый запрос
    if not query:
        return jsonify({"message": "Query parameter 'q' is required"}), 400

    try:
        query_json = json.loads(query)  # Преобразуем строку в JSON
    except json.JSONDecodeError:
        return jsonify({"message": "Invalid JSON format"}), 400

    # Выполняем поиск по JSONB
    sql_query = text("""
        SELECT *
        FROM public.orders
        WHERE details::jsonb @> :query
    """)
    results = db.session.execute(sql_query, {"query": json.dumps(query_json)}).fetchall()

    # Преобразуем результаты в JSON
    result_list = [{
        "id": row.id,
        "car_id": row.car_id,
        "mechanic_id": row.mechanic_id,
        "cost": row.cost,
        "details": row.details
    } for row in results]

    return jsonify(result_list)


@app.route('/orders/search_fulltext', methods=['GET'])
def search_orders_fulltext():
    regex = request.args.get('q')
    if not regex:
        return jsonify({"message": "No query parameter provided"}), 400

    sql = text("SELECT * FROM orders WHERE details::text ~ :regex")
    results = db.session.execute(sql, {'regex': regex}).fetchall()

    return jsonify([{
        "id": row.id,
        "car_id": row.car_id,
        "mechanic_id": row.mechanic_id,
        "issue_date": row.issue_date,
        "work_type": row.work_type,
        "cost": row.cost,
        "planned_end_date": row.planned_end_date,
        "actual_end_date": row.actual_end_date,
        "details": row.details
    } for row in results])

if __name__ == '__main__':
    app.run(debug=True, port=5002)
