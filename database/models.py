from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(100), nullable=True)
    gender = Column(String(20), nullable=False)
    age = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    marital_status = Column(String(50), nullable=False)
    interests = Column(Text, nullable=True)  # JSON строка с интересами
    bio = Column(Text, nullable=True)
    language = Column(String(10), default='ru')  # Язык пользователя ('ru' или 'uz')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Отношения
    search_settings = relationship("SearchSettings", back_populates="user", uselist=False)
    sent_requests = relationship("AccessRequest", foreign_keys="AccessRequest.from_user_id", back_populates="from_user")
    received_requests = relationship("AccessRequest", foreign_keys="AccessRequest.to_user_id", back_populates="to_user")

class SearchSettings(Base):
    __tablename__ = "search_settings"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    gender_preference = Column(String(20), nullable=False)  # "Мужчины", "Женщины", "Все"
    min_age = Column(Integer, nullable=False)
    max_age = Column(Integer, nullable=False)
    min_height = Column(Integer, nullable=False)
    max_height = Column(Integer, nullable=False)
    min_weight = Column(Integer, nullable=False)
    max_weight = Column(Integer, nullable=False)
    marital_status_preference = Column(Text, nullable=True)  # JSON строка с предпочтениями
    
    # Отношения
    user = relationship("User", back_populates="search_settings")

class AccessRequest(Base):
    __tablename__ = "access_requests"
    
    id = Column(Integer, primary_key=True)
    from_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    to_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(20), default="pending")  # "pending", "accepted", "rejected"
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Отношения
    from_user = relationship("User", foreign_keys=[from_user_id], back_populates="sent_requests")
    to_user = relationship("User", foreign_keys=[to_user_id], back_populates="received_requests")

class AllowedContact(Base):
    __tablename__ = "allowed_contacts"
    
    id = Column(Integer, primary_key=True)
    user1_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user2_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow) 