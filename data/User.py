# from data.Cart import Cart
# from data.Order import Order
from database import db

from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column,relationship
# from data.Order import Order

class User(db.Model):

    # id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(100), nullable=False)
    # price = db.Column(db.Float, default=0.0)


    __tablename__ = 'users'

    # id = db.Column(db.Integer,primary_key=True,name='id')
    
    # email = db.Column(db.String(255), unique=True, nullable=False)

    # email_verified_at  = db.Column(db.DateTime,nullable=True)

    # password = db.Column(db.String(255),nullable=False)

    # remember_token = db.Column(db.String(100), unique=True, nullable=True) 

    # created_at = db.Column(db.DateTime,nullable=True)

    # updated_at = db.Column(db.DateTime,nullable=True)

    # role = db.Column(db.String(255), nullable=False, default='user')


    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(db.String(190), unique=True)
    email_verified_at: Mapped[Optional[datetime]] = mapped_column()
    password: Mapped[str] = mapped_column(db.String(255))
    remember_token: Mapped[Optional[str]] = mapped_column(db.String(100), unique=True) 
        
    # Handled cleanly via datetime types
    created_at: Mapped[Optional[datetime]] = mapped_column(default=datetime.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=datetime.now())
    
    # Default values map cleanly
    role: Mapped[str] = mapped_column(db.String(255), default='user')

    profile_url:Mapped[Optional[str]] = mapped_column(db.String(255))

    username:Mapped[Optional[str]] = mapped_column(db.String(255))






    #relationship
    orders:Mapped[list["Order"]] = db.relationship("Order",back_populates="order_by",lazy='dynamic')
    cart:Mapped["Cart"] = db.relationship("Cart",back_populates="user",uselist=False)    
    
    
  

    
    def to_dict(self):

        dict_format = {column.name:getattr(self,column.name) for column in self.__table__.columns}

        return dict_format 
    
