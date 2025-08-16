import json
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from sqlalchemy.orm import Session
from sqlalchemy import and_

from database.database import get_db
from database.models import User, AccessRequest, AllowedContact
from keyboards.inline import get_access_request_keyboard, get_main_menu_keyboard
from locales.translations import get_text

router = Router()

def get_user_language(telegram_id: int, db: Session) -> str:
    """Получить язык пользователя"""
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    return user.language if user else 'ru'

@router.callback_query(F.data == "back_to_main")
async def back_to_main_menu(callback: CallbackQuery):
    """Вернуться в главное меню"""
    db = next(get_db())
    lang = get_user_language(callback.from_user.id, db)
    db.close()
    
    await callback.message.edit_text(
        get_text('main_menu', lang),
        reply_markup=get_main_menu_keyboard(lang)
    )

@router.callback_query(F.data == "requests")
async def show_requests(callback: CallbackQuery):
    """Показать входящие запросы на доступ"""
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
        
        # Получаем входящие запросы
        incoming_requests = db.query(AccessRequest).filter(
            and_(
                AccessRequest.to_user_id == current_user.id,
                AccessRequest.status == "pending"
            )
        ).all()
        
        if not incoming_requests:
            await callback.message.edit_text(
                get_text('requests_empty', lang),
                reply_markup=get_main_menu_keyboard(lang)
            )
            return
        
        # Показываем первый запрос
        await show_request(callback, incoming_requests[0], incoming_requests[1:], lang)
        
    except Exception as e:
        lang = get_user_language(callback.from_user.id, db)
        await callback.message.edit_text(
            get_text('error_occurred', lang),
            reply_markup=get_main_menu_keyboard(lang)
        )
        print(f"Show requests error: {e}")
    finally:
        db.close()

async def show_request(callback: CallbackQuery, request: AccessRequest, remaining_requests: list, lang: str = 'ru'):
    """Показать запрос на доступ"""
    db = next(get_db())
    
    try:
        # Получаем информацию о пользователе, отправившем запрос
        from_user = db.query(User).filter(User.id == request.from_user_id).first()
        if not from_user:
            await callback.message.edit_text(
                get_text('error_occurred', lang),
                reply_markup=get_main_menu_keyboard(lang)
            )
            return
        
        # Формируем текст запроса
        request_text = f"{get_text('requests_from', lang, name=f'{from_user.gender}, {from_user.age}')}\n\n"
        request_text += f"{get_text('profile_height', lang, height=from_user.height)}\n"
        request_text += f"{get_text('profile_weight', lang, weight=from_user.weight)}\n"
        request_text += f"{get_text('profile_marital', lang, status=from_user.marital_status)}\n"
        
        if from_user.interests:
            try:
                interests = json.loads(from_user.interests)
                if interests:
                    request_text += f"{get_text('profile_interests', lang, interests=', '.join(interests))}\n"
            except:
                pass
        
        if from_user.bio:
            request_text += f"\n{get_text('profile_bio', lang, bio=from_user.bio)}\n"
        
        request_text += f"\n{get_text('requests_access_granted', lang)}"
        
        await callback.message.edit_text(
            request_text,
            reply_markup=get_access_request_keyboard(request.id, lang)
        )
        
    except Exception as e:
        await callback.message.edit_text(
            get_text('error_occurred', lang),
            reply_markup=get_main_menu_keyboard(lang)
        )
        print(f"Show request error: {e}")
    finally:
        db.close()

@router.callback_query(F.data.startswith("accept_request:"))
async def accept_request(callback: CallbackQuery):
    """Принять запрос на доступ"""
    request_id = int(callback.data.split(":")[1])
    db = next(get_db())
    
    try:
        # Получаем язык пользователя
        lang = get_user_language(callback.from_user.id, db)
        
        # Получаем запрос и пользователей
        access_request = db.query(AccessRequest).filter(AccessRequest.id == request_id).first()
        if not access_request:
            await callback.answer(get_text('error_occurred', lang), show_alert=True)
            return
        
        current_user = db.query(User).filter(User.telegram_id == callback.from_user.id).first()
        from_user = db.query(User).filter(User.id == access_request.from_user_id).first()
        
        if not current_user or not from_user:
            await callback.answer(get_text('error_occurred', lang), show_alert=True)
            return
        
        # Обновляем статус запроса
        access_request.status = "accepted"
        db.commit()
        
        # Создаем разрешенный контакт
        allowed_contact = AllowedContact(
            user1_id=current_user.id,
            user2_id=from_user.id
        )
        db.add(allowed_contact)
        db.commit()
        
        await callback.answer(get_text('requests_accepted', lang), show_alert=True)
        
        # Отправляем уведомление пользователю, который запрашивал доступ
        from services.notifications import NotificationService
        notification_service = NotificationService(callback.bot)
        await notification_service.send_access_granted_notification(request_id)
        
        # Показываем следующий запрос или возвращаем в меню
        await show_next_request_or_menu(callback, db, current_user, lang)
        
    except Exception as e:
        lang = get_user_language(callback.from_user.id, db)
        await callback.answer(get_text('error_occurred', lang), show_alert=True)
        print(f"Accept request error: {e}")
    finally:
        db.close()

@router.callback_query(F.data.startswith("reject_request:"))
async def reject_request(callback: CallbackQuery):
    """Отклонить запрос на доступ"""
    request_id = int(callback.data.split(":")[1])
    db = next(get_db())
    
    try:
        # Получаем язык пользователя
        lang = get_user_language(callback.from_user.id, db)
        
        # Получаем запрос
        access_request = db.query(AccessRequest).filter(AccessRequest.id == request_id).first()
        if not access_request:
            await callback.answer(get_text('error_occurred', lang), show_alert=True)
            return
        
        current_user = db.query(User).filter(User.telegram_id == callback.from_user.id).first()
        if not current_user:
            await callback.answer(get_text('error_occurred', lang), show_alert=True)
            return
        
        # Обновляем статус запроса
        access_request.status = "rejected"
        db.commit()
        
        await callback.answer(get_text('requests_declined', lang), show_alert=True)
        
        # Показываем следующий запрос или возвращаем в меню
        await show_next_request_or_menu(callback, db, current_user, lang)
        
    except Exception as e:
        lang = get_user_language(callback.from_user.id, db)
        await callback.answer(get_text('error_occurred', lang), show_alert=True)
        print(f"Reject request error: {e}")
    finally:
        db.close()

async def show_next_request_or_menu(callback: CallbackQuery, db: Session, current_user: User, lang: str = 'ru'):
    """Показать следующий запрос или вернуться в меню"""
    # Получаем оставшиеся запросы
    remaining_requests = db.query(AccessRequest).filter(
        and_(
            AccessRequest.to_user_id == current_user.id,
            AccessRequest.status == "pending"
        )
    ).all()
    
    if remaining_requests:
        await show_request(callback, remaining_requests[0], remaining_requests[1:], lang)
    else:
        await callback.message.edit_text(
            get_text('requests_empty', lang),
            reply_markup=get_main_menu_keyboard(lang)
        ) 