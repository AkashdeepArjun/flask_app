# from data.Product import Product
import decimal

from database import db
from datetime import date, datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Numeric, Boolean
from decimal import Decimal
# from data.User import User
class ProductImage(db.Model):

    __tablename__ = 'product_images'

    id:Mapped[int] = mapped_column(db.Integer,primary_key=True)

    product_id:Mapped[int] = mapped_column(db.ForeignKey('products.product_id',ondelete='CASCADE'))

    image_url:Mapped[String] = mapped_column(db.String(255),nullable=False)


    #relationship 


    product:Mapped['Product'] = db.relationship('Product',back_populates='gallary_images')

    
