# from data.Cart import Cart
# from data.Order import Order
# from data.Product import Product
from database import db
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Numeric, Boolean
from decimal import Decimal





from database import db

class CartProduct(db.Model):
        
        __tablename__='cart_product'

        cart_id:Mapped[int] = mapped_column(db.ForeignKey('carts.id',ondelete='CASCADE'),primary_key=True)
        
        product_id:Mapped[int] =mapped_column(db.ForeignKey('products.product_id',ondelete='CASCADE'),primary_key=True)

        quantity:Mapped[int] = mapped_column(db.Integer,default=1)

        #relationships 

        cart:Mapped["Cart"] = db.relationship("Cart",back_populates='product_items')

        product:Mapped['Product'] = db.relationship("Product",back_populates='cart_items')





        


