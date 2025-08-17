from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# Таблица связи пользователей и интересов
user_interests = Table(
    'user_interests',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('interest', String(50))
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String(100), nullable=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    
    # Профиль
    gender = Column(String(20), nullable=True)
    age = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    weight = Column(Integer, nullable=True)
    marital_status = Column(String(50), nullable=True)
    bio = Column(Text, nullable=True)
    language = Column(String(10), default='ru')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Поисковые предпочтения
    search_gender = Column(String(20), nullable=True)
    min_age = Column(Integer, nullable=True)
    max_age = Column(Integer, nullable=True)
    min_height = Column(Integer, nullable=True)
    max_height = Column(Integer, nullable=True)
    min_weight = Column(Integer, nullable=True)
    max_weight = Column(Integer, nullable=True)
    
    # Связи
    sent_requests = relationship("Request", foreign_keys="Request.from_user_id", back_populates="from_user")
    received_requests = relationship("Request", foreign_keys="Request.to_user_id", back_populates="to_user")

class Request(Base):
    __tablename__ = "requests"
    
    id = Column(Integer, primary_key=True, index=True)
    from_user_id = Column(Integer, ForeignKey("users.id"))
    to_user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String(20), default="pending")  # pending, accepted, declined
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    from_user = relationship("User", foreign_keys=[from_user_id], back_populates="sent_requests")
    to_user = relationship("User", foreign_keys=[to_user_id], back_populates="received_requests") 