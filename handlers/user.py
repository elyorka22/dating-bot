from sqlalchemy.orm import Session
from database.models import User
from database.database import get_db
from locales.translations import get_text
import logging

logger = logging.getLogger(__name__)

def get_user_by_telegram_id(telegram_id: int, db: Session) -> User:
    """Получить пользователя по Telegram ID"""
    try:
        user = db.query(User).filter(User.telegram_id == telegram_id).first()
        if user:
            logger.info(f"👤 Пользователь найден: {telegram_id}")
        else:
            logger.info(f"❌ Пользователь не найден: {telegram_id}")
        return user
    except Exception as e:
        logger.error(f"❌ Ошибка поиска пользователя {telegram_id}: {e}")
        return None

def create_user(telegram_id: int, username: str = None, first_name: str = None, last_name: str = None, db: Session = None) -> User:
    """Создать нового пользователя"""
    try:
        if db is None:
            db = next(get_db())
        
        logger.info(f"🆕 Создание пользователя: {telegram_id}")
        
        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info(f"✅ Пользователь создан: {telegram_id} (ID: {user.id})")
        return user
    except Exception as e:
        logger.error(f"❌ Ошибка создания пользователя {telegram_id}: {e}")
        if db:
            db.rollback()
        raise

def update_user_profile(user_id: int, **kwargs) -> bool:
    """Обновить профиль пользователя"""
    try:
        db = next(get_db())
        user = db.query(User).filter(User.id == user_id).first()
        
        if user:
            logger.info(f"🔄 Обновление профиля пользователя: {user_id}")
            logger.info(f"📝 Данные для обновления: {kwargs}")
            
            for key, value in kwargs.items():
                if hasattr(user, key):
                    old_value = getattr(user, key)
                    setattr(user, key, value)
                    logger.info(f"📝 {key}: {old_value} → {value}")
                else:
                    logger.warning(f"⚠️ Поле {key} не существует в модели User")
            
            db.commit()
            logger.info(f"✅ Профиль пользователя {user_id} обновлен успешно")
            return True
        else:
            logger.error(f"❌ Пользователь {user_id} не найден")
            return False
    except Exception as e:
        logger.error(f"❌ Ошибка обновления профиля {user_id}: {e}")
        if db:
            db.rollback()
        return False

def get_user_profile_text(user: User, lang: str = 'ru') -> str:
    """Получить текст профиля пользователя"""
    if not user:
        return get_text('no_profile', lang)
    
    profile_text = f"👤 {get_text('user_profile', lang)}\n\n"
    
    if user.gender:
        profile_text += f"👤 {get_text('gender', lang)}: {user.gender}\n"
    if user.age:
        profile_text += f"🎂 {get_text('age', lang)}: {user.age}\n"
    if user.height:
        profile_text += f"📏 {get_text('height', lang)}: {user.height} см\n"
    if user.weight:
        profile_text += f"⚖️ {get_text('weight', lang)}: {user.weight} кг\n"
    if user.marital_status:
        profile_text += f"💍 {get_text('marital_status', lang)}: {user.marital_status}\n"
    if user.bio:
        profile_text += f"📝 {get_text('bio', lang)}: {user.bio}\n"
    
    return profile_text

def search_users(user_id: int, db: Session, limit: int = 10):
    """Поиск пользователей по критериям"""
    current_user = db.query(User).filter(User.id == user_id).first()
    if not current_user:
        return []
    
    query = db.query(User).filter(
        User.id != user_id,
        User.is_active == True
    )
    
    # Фильтр по полу
    if current_user.search_gender and current_user.search_gender != 'all':
        query = query.filter(User.gender == current_user.search_gender)
    
    # Фильтр по возрасту
    if current_user.min_age:
        query = query.filter(User.age >= current_user.min_age)
    if current_user.max_age:
        query = query.filter(User.age <= current_user.max_age)
    
    # Фильтр по росту
    if current_user.min_height:
        query = query.filter(User.height >= current_user.min_height)
    if current_user.max_height:
        query = query.filter(User.height <= current_user.max_height)
    
    # Фильтр по весу
    if current_user.min_weight:
        query = query.filter(User.weight >= current_user.min_weight)
    if current_user.max_weight:
        query = query.filter(User.weight <= current_user.max_weight)
    
    return query.limit(limit).all()

def is_profile_complete(user: User) -> bool:
    """Проверить, заполнен ли профиль полностью"""
    required_fields = ['gender', 'age', 'height', 'weight', 'marital_status']
    return all(getattr(user, field) for field in required_fields) 