from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class Buyer(Base):
    __tablename__ = 'buyer'

    buyer_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    address = Column(String(200), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    sex = Column(String(6), nullable=False )
    city = Column(String(50), nullable=False)
    phone_number = Column(String(15), nullable=False)
    registry_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    update_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Define one-to-many relationship with GroupChatParticipants
    # group_chat_participants = relationship("GroupChatParticipants", back_populates="user")


class Company(Base):
    __tablename__ = 'company'

    company_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    city = Column(String(50), nullable=False)
    address = Column(String(200), nullable=False)
    rating = Column(Float, nullable=True)
    phone_number = Column(String(15), nullable=False)
    registry_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    update_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Define one-to-many relationship with GroupChatParticipants
    # group_chat_participants = relationship("GroupChatParticipants", back_populates="group_chat")

    # Define one-to-many relationship with GroupChatMessage
    # item_cards = relationship("ItemCard", back_populates="item_card")


class ItemCard(Base):
    __tablename__ = 'item_card'

    item_id = Column(Integer, primary_key=True, autoincrement=True)
    item_name = Column(String(100), nullable=False, unique=True)
    seller_id = Column(Integer, ForeignKey('company.company_id'), nullable=False)
    category_name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    rating = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    create_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    update_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Define many-to-one relationships
    # group_chat = relationship("GroupChat", back_populates="group_chat_participants")
    # seller = relationship("Company", back_populates="item_card")

