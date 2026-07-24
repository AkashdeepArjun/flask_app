from .InstanceManager import InstanceManager 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import String, Text, Numeric, Boolean

db = SQLAlchemy()

# data/__init__.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# order_product_relation = db.Table(
#     'order_product',
#     db.metadata,  # Crucial context for core metadata tracking
#     db.Column('order_id', db.Integer, db.ForeignKey('orders.order_id', ondelete='CASCADE'), primary_key=True),
#     db.Column('product_id', db.Integer, db.ForeignKey('products.product_id', ondelete='CASCADE'), primary_key=True)
# )

# cart_product_relation =db.Table(

#     'cart_product',
#     db.metadata,  # Crucial context for core metadata tracking
#     db.Column('id', db.Integer, db.ForeignKey('carts.id', ondelete='CASCADE'), primary_key=True),
#     db.Column('product_id', db.Integer, db.ForeignKey('products.product_id', ondelete='CASCADE'), primary_key=True)

# )