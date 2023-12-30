from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text, DECIMAL, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    is_seller = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    product_cards = relationship("ProductCard", back_populates="seller")
    purchase_history = relationship("PurchaseHistory", back_populates="buyer")
    item_cart = relationship("ItemCart", back_populates="user")

class ProductCard(Base):
    __tablename__ = 'ProductCards'

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    seller_id = Column(Integer, ForeignKey('Users.user_id'), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    category = Column(String(50), nullable=False)
    price = Column(DECIMAL(10, 2))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    seller = relationship("User", back_populates="product_cards")
    purchase_items = relationship("PurchaseItem", back_populates="product")
    item_cart = relationship("ItemCart", back_populates="product")

class PurchaseItem(Base):
    __tablename__ = 'PurchaseItems'

    purchase_item_id = Column(Integer, primary_key=True, autoincrement=True)
    purchase_id = Column(Integer, ForeignKey('PurchaseHistory.purchase_id'))
    product_id = Column(Integer, ForeignKey('ProductCards.product_id'), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)

    purchase = relationship("PurchaseHistory", back_populates="purchase_items")
    product = relationship("ProductCard", back_populates="purchase_items")

class PurchaseHistory(Base):
    __tablename__ = 'PurchaseHistory'

    purchase_id = Column(Integer, primary_key=True, autoincrement=True)
    buyer_id = Column(Integer, ForeignKey('Users.user_id'), nullable=False)
    purchase_date = Column(DateTime, default=datetime.utcnow)

    buyer = relationship("User", back_populates="purchase_history")
    purchase_items = relationship("PurchaseItem", back_populates="purchase")

class ItemCart(Base):
    __tablename__ = 'ItemCart'

    user_id = Column(Integer, ForeignKey('Users.user_id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('ProductCards.product_id'), primary_key=True)
    quantity = Column(Integer, nullable=False)
    
    user = relationship("User", back_populates="item_cart")
    product = relationship("ProductCard", back_populates="item_cart")