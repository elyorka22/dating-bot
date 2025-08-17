import json
from sqlalchemy.orm import Session
from database.models import Request, User
from database.database import get_db
from locales.translations import get_text
from config import MAX_REQUESTS_PER_DAY
from datetime import datetime

def create_request(from_user_id: int, to_user_id: int, db: Session) -> Request:
    """Создать новый запрос"""
    # Проверяем, не отправлял ли уже запрос
    existing_request = db.query(Request).filter(
        Request.from_user_id == from_user_id,
        Request.to_user_id == to_user_id
    ).first()
    
    if existing_request:
        return None
    
    request = Request(
        from_user_id=from_user_id,
        to_user_id=to_user_id
    )
    db.add(request)
    db.commit()
    db.refresh(request)
    return request

def get_user_requests(user_id: int, db: Session, status: str = None):
    """Получить запросы пользователя"""
    query = db.query(Request).filter(Request.to_user_id == user_id)
    if status:
        query = query.filter(Request.status == status)
    return query.all()

def update_request_status(request_id: int, status: str, db: Session) -> bool:
    """Обновить статус запроса"""
    try:
        request = db.query(Request).filter(Request.id == request_id).first()
        if request:
            request.status = status
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        print(f"Ошибка обновления статуса запроса: {e}")
        return False

def get_request_by_id(request_id: int, db: Session) -> Request:
    """Получить запрос по ID"""
    return db.query(Request).filter(Request.id == request_id).first()

def get_user_sent_requests(user_id: int, db: Session):
    """Получить отправленные запросы пользователя"""
    return db.query(Request).filter(Request.from_user_id == user_id).all()

def can_send_request(user_id: int, db: Session) -> bool:
    """Проверить, может ли пользователь отправить запрос (лимит)"""
    today = datetime.now().date()
    today_requests = db.query(Request).filter(
        Request.from_user_id == user_id,
        Request.created_at >= today
    ).count()
    
    return today_requests < MAX_REQUESTS_PER_DAY

def get_requests_count(user_id: int, db: Session) -> dict:
    """Получить количество запросов пользователя"""
    today = datetime.now().date()
    today_requests = db.query(Request).filter(
        Request.from_user_id == user_id,
        Request.created_at >= today
    ).count()
    
    total_requests = db.query(Request).filter(Request.from_user_id == user_id).count()
    
    return {
        'today': today_requests,
        'total': total_requests,
        'limit': MAX_REQUESTS_PER_DAY
    }

def get_user_language(telegram_id: int, db: Session) -> str:
    """Получить язык пользователя"""
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    return user.language if user else 'ru' 