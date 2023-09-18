"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Product, Order, OrderStatus

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# get All users
@app.route('/users', methods=['GET'])
def get_all_user():

    user_list = User.query.all()
    serialized = list(map(lambda user: user.serialize(), user_list))

    return jsonify(serialized), 200

# add a new user
@app.route('/users', methods=['POST'])
def add_user():
    if not request.is_json:
        return jsonify({'msg': 'Body must be a JSON object'}), 400

    body = request.get_json()
    name = body.get('name')
    email = body.get('email')
    if None in [name, email]:
        return jsonify({'msg': 'Wrong properties'}), 400

    any_user = User.query.filter_by(email=email).one_or_none()
    if any_user is not None:
        return jsonify({'msg': 'Email already chosen'}), 400

    user = User(name=name, email=email)

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'msg': 'Some internal error'}), 500

    return jsonify({'msg': 'User added'}), 202


# get All products
@app.route('/products', methods=['GET'])
def get_all_products():

    product_list = Product.query.all()
    serialized = list(map(lambda product: product.serialize(), product_list))

    return jsonify(serialized), 200

# add a new product
@app.route('/products', methods=['POST'])
def add_product():
    if not request.is_json:
        return jsonify({'msg': 'Body must be a JSON object'}), 400

    body = request.get_json()
    name = body.get('name')
    price = body.get('price')
    if None in [name, price]:
        return jsonify({'msg': 'Wrong properties'}), 400

    any_product = Product.query.filter_by(name=name).one_or_none()
    if any_product is not None:
        return jsonify({'msg': 'There is a product already.'}), 400

    product = Product(name=name, price=price)

    try:
        db.session.add(product)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'msg': 'Some internal error'}), 500

    return jsonify({'msg': 'Product added'}), 202


# add a new product
@app.route('/products/<int:id>', methods=['DELETE'])
def remove_product(id):
    product = Product.query.filter_by(id=id).one_or_none()
    if product is None:
        return jsonify({'msg': 'Product not found'}), 404

    try:
        db.session.delete(product)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'msg': 'Some internal error'}), 500

    return jsonify({'msg': 'Product deleted'}), 200


# put a new product
@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    if not request.is_json:
        return jsonify({'msg': 'Body must be a JSON object'}), 400

    product = Product.query.filter_by(id=id).one_or_none()
    if product is None:
        return jsonify({'msg': 'Product not found'}), 404

    body = request.get_json()
    name = body.get('name')
    price = body.get('price')
    if None in [name, price]:
        return jsonify({'msg': 'Wrong properties'}), 400

    product.name = name
    product.price = price

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'msg': 'Some internal error'}), 500

    return jsonify({'msg': 'Product updated'}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
