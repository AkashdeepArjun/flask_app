# from data.Cart import Cart
# from data.Order import Order
# from data.OrderProduct import OrderProduct
from database import db 
from decimal import Decimal

from database import db
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Numeric, Boolean
# from data.User import User

class Product(db.Model):

    __tablename__='products'

    product_id:Mapped[int] = mapped_column(primary_key=True,unique=True)
    description:Mapped[str] = mapped_column(String(255),nullable=True)
    created_at:Mapped[datetime] =  mapped_column(db.DateTime())
    category_id:Mapped[Optional[int]] = mapped_column(Numeric(10))
    price:Mapped[Decimal] = mapped_column(Numeric(10,2))
    image_url:Mapped[Optional[str]] = mapped_column(String(255))
    is_active:Mapped[Optional[bool]]= mapped_column(Boolean,default=True)
    deleted_at:Mapped[Optional[datetime]] = mapped_column(db.DateTime)
    name:Mapped[str] = mapped_column(db.String(255))
    slug:Mapped[str] = mapped_column(db.String(255))
    brand:Mapped[str] = mapped_column(db.String(255))
    category:Mapped[str] = mapped_column(db.String(255))
    specs:Mapped[dict] = mapped_column(db.JSON())

    # relationships 

    # order_from:Mapped['Order']=db.relationship('Order',secondary=order_product_relation,back_populates='items')
    
    # cart_from:Mapped['Cart'] = db.relationship('Cart',secondary=cart_product_relation,back_populates='items')

    order_items:Mapped[list['OrderProduct']] = db.relationship("OrderProduct",back_populates="product")
    # product_items:Mapped[list:['OrderProduct']] = db.relationship("OrderProduct",back_populates="order")
    cart_items:Mapped[list:['CartProduct']] = db.relationship("CartProduct",back_populates="product")




