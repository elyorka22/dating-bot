import json
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime

from database.database import get_db
from database.models import User, SearchSettings, AccessRequest
from keyboards.inline import get_search_action_keyboard, get_main_menu_keyboard
from locales.translations import get_text
from config import MAX_REQUESTS_PER_DAY

router = Router()

def get_user_language(telegram_id: int, db: Session) -> str:
    """Получить язык пользователя"""
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    return user.language if user else 'ru'

@router.callback_query(F.data == "search")
async def start_search(callback: CallbackQuery):
    """Начало поиска пользователей"""
    db = next(get_db())
    
    try:
        # Получаем язык пользователя
        lang = get_user_language(callback.from_user.id, db)
        
        # Получаем текущего пользователя
        current_user = db.query(User).filter(User.telegram_id == callback.from_user.id).first()
        if not current_user:
            await callback.message.edit_text(
                get_text('error_not_registered', lang),
                reply_markup=get_main_menu_keyboard(lang)
            )
            return
        
        # Получаем настройки поиска
        search_settings = db.query(SearchSettings).filter(SearchSettings.user_id == current_user.id).first()
        if not search_settings:
            await callback.message.edit_text(
                get_text('error_not_registered', lang),
                reply_markup=get_main_menu_keyboard(lang)
            )
            return
        
        # Ищем подходящих пользователей
        suitable_users = find_suitable_users(db, current_user, search_settings)
        
        if not suitable_users:
            await callback.message.edit_text(
                get_text('search_no_results', lang),
                reply_markup=get_main_menu_keyboard(lang)
            )
            return
        
        # Показываем первого пользователя
        await show_user_profile(callback, suitable_users[0], suitable_users[1:], lang)
        
    except Exception as e:
        lang = get_user_language(callback.from_user.id, db)
        await callback.message.edit_text(
            get_text('error_occurred', lang),
            reply_markup=get_main_menu_keyboard(lang)
        )
        print(f"Search error: {e}")
    finally:
        db.close()

def find_suitable_users(db: Session, current_user: User, search_settings: SearchSettings):
    """Поиск подходящих пользователей"""
    # Базовый запрос
    query = db.query(User).filter(
        and_(
            User.id != current_user.id,
            User.is_active == True
        )
    )
    
    # Фильтр по полу
    if search_settings.gender_preference == "Мужчины":
        query = query.filter(User.gender == "Мужчина")
    elif search_settings.gender_preference == "Женщины":
        query = query.filter(User.gender == "Женщина")
    
    # Фильтр по возрасту
    query = query.filter(
        and_(
            User.age >= search_settings.min_age,
            User.age <= search_settings.max_age
        )
    )
    
    # Фильтр по росту
    query = query.filter(
        and_(
            User.height >= search_settings.min_height,
            User.height <= search_settings.max_height
        )
    )
    
    # Фильтр по весу
    query = query.filter(
        and_(
            User.weight >= search_settings.min_weight,
            User.weight <= search_settings.max_weight
        )
    )
    
    # Фильтр по семейному положению
    if search_settings.marital_status_preference:
        try:
            preferred_statuses = json.loads(search_settings.marital_status_preference)
            query = query.filter(User.marital_status.in_(preferred_statuses))
        except:
            pass
    
    # Исключаем пользователей, которым уже отправляли запросы
    sent_requests = db.query(AccessRequest.from_user_id).filter(
        AccessRequest.from_user_id == current_user.id
    ).subquery()
    
    query = query.filter(~User.id.in_(sent_requests))
    
    # Сортируем по дате создания (новые сначала)
    query = query.order_by(User.created_at.desc())
    
    return query.all()

async def show_user_profile(callback: CallbackQuery, user: User, remaining_users: list, lang: str = 'ru'):
    """Показать профиль пользователя"""
    # Формируем текст профиля
    profile_text = f"{get_text('profile_title', lang)}\n\n"
    profile_text += f"{get_text('profile_gender', lang, gender=user.gender)}\n"
    profile_text += f"{get_text('profile_age', lang, age=user.age)}\n"
    profile_text += f"{get_text('profile_height', lang, height=user.height)}\n"
    profile_text += f"{get_text('profile_weight', lang, weight=user.weight)}\n"
    profile_text += f"{get_text('profile_marital', lang, status=user.marital_status)}\n"
    
    if user.interests:
        try:
            interests = json.loads(user.interests)
            if interests:
                profile_text += f"{get_text('profile_interests', lang, interests=', '.join(interests))}\n"
        except:
            pass
    
    if user.bio:
        profile_text += f"\n{get_text('profile_bio', lang, bio=user.bio)}\n"
    
    # Сохраняем оставшихся пользователей в callback data
    remaining_ids = [str(u.id) for u in remaining_users]
    remaining_data = ",".join(remaining_ids) if remaining_ids else ""
    
    await callback.message.edit_text(
        profile_text,
        reply_markup=get_search_action_keyboard(user.id, lang)
    )

@router.callback_query(F.data.startswith("request_access:"))
async def request_access(callback: CallbackQuery):
    """Запрос доступа к пользователю"""
    target_user_id = int(callback.data.split(":")[1])
    db = next(get_db())
    
    try:
        # Получаем язык пользователя
        lang = get_user_language(callback.from_user.id, db)
        
        # Получаем пользователей
        current_user = db.query(User).filter(User.telegram_id == callback.from_user.id).first()
        target_user = db.query(User).filter(User.id == target_user_id).first()
        
        if not current_user or not target_user:
            await callback.answer(get_text('error_occurred', lang), show_alert=True)
            return
        
        # Проверяем лимит запросов
        today_requests = db.query(AccessRequest).filter(
            and_(
                AccessRequest.from_user_id == current_user.id,
                AccessRequest.created_at >= datetime.utcnow().date()
            )
        ).count()
        
        if today_requests >= MAX_REQUESTS_PER_DAY:
            await callback.answer(
                get_text('error_daily_limit', lang, limit=MAX_REQUESTS_PER_DAY),
                show_alert=True
            )
            return
        
        # Проверяем, не отправляли ли уже запрос
        existing_request = db.query(AccessRequest).filter(
            and_(
                AccessRequest.from_user_id == current_user.id,
                AccessRequest.to_user_id == target_user_id
            )
        ).first()
        
        if existing_request:
            await callback.answer(get_text('error_already_requested', lang), show_alert=True)
            return
        
        # Создаем запрос
        access_request = AccessRequest(
            from_user_id=current_user.id,
            to_user_id=target_user_id
        )
        db.add(access_request)
        db.commit()
        db.refresh(access_request)
        
        await callback.answer(get_text('requests_accepted', lang), show_alert=True)
        
        # Отправляем уведомление получателю
        from services.notifications import NotificationService
        notification_service = NotificationService(callback.bot)
        await notification_service.send_new_request_notification(access_request.id)
        
        # Показываем следующего пользователя или возвращаем в меню
        await show_next_user_or_menu(callback, db, current_user, lang)
        
    except Exception as e:
        lang = get_user_language(callback.from_user.id, db)
        await callback.answer(get_text('error_occurred', lang), show_alert=True)
        print(f"Request access error: {e}")
    finally:
        db.close()

@router.callback_query(F.data == "skip_profile")
async def skip_profile(callback: CallbackQuery):
    """Пропустить профиль"""
    db = next(get_db())
    
    try:
        lang = get_user_language(callback.from_user.id, db)
        current_user = db.query(User).filter(User.telegram_id == callback.from_user.id).first()
        if not current_user:
            await callback.message.edit_text(
                get_text('error_not_registered', lang),
                reply_markup=get_main_menu_keyboard(lang)
            )
            return
        
        await show_next_user_or_menu(callback, db, current_user, lang)
        
    except Exception as e:
        lang = get_user_language(callback.from_user.id, db)
        await callback.message.edit_text(
            get_text('error_occurred', lang),
            reply_markup=get_main_menu_keyboard(lang)
        )
        print(f"Skip profile error: {e}")
    finally:
        db.close()

async def show_next_user_or_menu(callback: CallbackQuery, db: Session, current_user: User, lang: str = 'ru'):
    """Показать следующего пользователя или вернуться в меню"""
    # Получаем настройки поиска
    search_settings = db.query(SearchSettings).filter(SearchSettings.user_id == current_user.id).first()
    if not search_settings:
        await callback.message.edit_text(
            get_text('error_not_registered', lang),
            reply_markup=get_main_menu_keyboard(lang)
        )
        return
    
    # Ищем следующих пользователей
    suitable_users = find_suitable_users(db, current_user, search_settings)
    
    if suitable_users:
        await show_user_profile(callback, suitable_users[0], suitable_users[1:], lang)
    else:
        await callback.message.edit_text(
            get_text('search_no_more', lang),
            reply_markup=get_main_menu_keyboard(lang)
        ) 