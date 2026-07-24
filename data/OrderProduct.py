# from data.Order import Order
# from data.Product import Product
from database import db
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Numeric, Boolean
from decimal import Decimal





from database import db

class OrderProduct(db.Model):
        
        __tablename__='order_product'

        order_id:Mapped[int] = mapped_column(db.ForeignKey('orders.order_id',ondelete='CASCADE'),primary_key=True)
        
        product_id:Mapped[int] =mapped_column(db.ForeignKey('products.product_id',ondelete='CASCADE'),primary_key=True)

        quantity:Mapped[int] = mapped_column(db.Integer,default=1)

        unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))

        #relationships 

        order:Mapped["Order"] = db.relationship("Order",back_populates='product_items')

        product:Mapped['Product'] = db.relationship("Product",back_populates='order_items')





        


