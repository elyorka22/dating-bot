"""
Хендлеры для управления языком
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import User
from keyboards.language import get_language_keyboard, get_language_settings_keyboard
from keyboards.inline import get_main_menu_keyboard
from locales.translations import get_text, is_supported_language

router = Router()

@router.message(F.text == "/language")
async def language_command(message: Message):
    """Команда для смены языка"""
    await show_language_settings(message)

@router.callback_query(F.data == "language_settings")
async def show_language_settings(callback: CallbackQuery):
    """Показать настройки языка"""
    await callback.message.edit_text(
        "🌍 Выберите язык / Tilni tanlang:",
        reply_markup=get_language_settings_keyboard()
    )

@router.callback_query(F.data.startswith("language:"))
async def select_language(callback: CallbackQuery):
    """Выбор языка при первом запуске"""
    lang = callback.data.split(":")[1]
    
    if not is_supported_language(lang):
        await callback.answer("❌ Неподдерживаемый язык")
        return
    
    # Сохраняем выбранный язык в FSM
    await callback.message.edit_text(
        get_text('language_changed', lang),
        reply_markup=get_main_menu_keyboard(lang)
    )
    
    # Показываем главное меню на выбранном языке
    await show_main_menu(callback, lang)

@router.callback_query(F.data.startswith("set_language:"))
async def set_language(callback: CallbackQuery):
    """Установка языка в настройках"""
    lang = callback.data.split(":")[1]
    
    if not is_supported_language(lang):
        await callback.answer("❌ Неподдерживаемый язык")
        return
    
    # Получаем пользователя из базы данных
    db = next(get_db())
    user = db.query(User).filter(User.telegram_id == callback.from_user.id).first()
    
    if user:
        # Обновляем язык пользователя
        user.language = lang
        db.commit()
        db.close()
        
        await callback.answer(get_text('language_changed', lang), show_alert=True)
        
        # Показываем главное меню на новом языке
        await show_main_menu(callback, lang)
    else:
        await callback.answer("❌ Пользователь не найден", show_alert=True)

async def show_main_menu(callback: CallbackQuery, lang: str):
    """Показать главное меню на выбранном языке"""
    await callback.message.edit_text(
        get_text('main_menu', lang),
        reply_markup=get_main_menu_keyboard(lang)
    )

def get_user_language(telegram_id: int, db: Session) -> str:
    """Получить язык пользователя из базы данных"""
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    return user.language if user else 'ru' 