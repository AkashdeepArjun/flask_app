
# from data.Product import Product
from database import db 

from decimal import Decimal
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Numeric, Boolean,func
# from data.User import User

class Cart(db.Model):

    __tablename__='carts'

    id:Mapped[int]=mapped_column(db.Integer,primary_key=True)
    user_id:Mapped[int] = mapped_column(db.ForeignKey('users.id'))
    created_at:Mapped[datetime] =mapped_column(server_default=func.now())


#relationship 

    # items:Mapped[list['Product']] = db.relationship('Product',secondary=cart_product_relation,back_populates='cart_from')

    user:Mapped["User"] = db.relationship('User',back_populates="cart")
    
    product_items:Mapped[list['CartProduct']] = db.relationship("CartProduct",back_populates="cart",cascade="all, delete-orphan")
