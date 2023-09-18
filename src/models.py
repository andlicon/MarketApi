from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import enum

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime , default=datetime.now)
    updated_at = db.Column(db.DateTime , default=datetime.now, onupdate=datetime.now)
    # relationship
    orders = db.relationship('Order', backref='user')

    def __repr__(self):
        return f'<User {self.username}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    price = db.Column(db.Float, unique=False, nullable=False)
    created_at = db.Column(db.DateTime , default=datetime.now)
    updated_at = db.Column(db.DateTime , default=datetime.now, onupdate=datetime.now)
    # relationship
    orders = db.relationship('Order', backref='product')

    def __repr__(self):
        return f'<Product {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class OrderStatus(enum.Enum):
    ORDERED = 'ordered'
    SALE = 'sale'


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum(OrderStatus), nullable=False, default=OrderStatus.ORDERED)
    created_at = db.Column(db.DateTime , default=datetime.now)
    updated_at = db.Column(db.DateTime , default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f'<Order {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "amount": self.amount,
            "status": self.status.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }