# from data.Product import Product
from database import db
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Numeric, Boolean
from decimal import Decimal
# from data.User import User
class Order(db.Model):

    __tablename__="orders" 

    order_id:Mapped[int]=mapped_column(primary_key=True) 
    
    user_id:Mapped[int] = mapped_column(db.ForeignKey('users.id',ondelete='CASCADE'))

    amount:Mapped[Decimal] =mapped_column(Numeric(10,2))

    created_at:Mapped[datetime] = mapped_column(db.DateTime())

    

    #relationship 
    order_by:Mapped["User"]=db.relationship("User",back_populates="orders")

    # items:Mapped[list['Product']] = db.relationship('Product',secondry=order_product_relation,back_populates='order_from')

    product_items:Mapped[list['OrderProduct']] = db.relationship("OrderProduct",back_populates="order")

    