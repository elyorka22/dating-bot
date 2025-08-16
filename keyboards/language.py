"""
Клавиатуры для выбора языка
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_language_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора языка"""
    builder = InlineKeyboardBuilder()
    
    builder.add(InlineKeyboardButton(
        text="🇷🇺 Русский",
        callback_data="language:ru"
    ))
    builder.add(InlineKeyboardButton(
        text="🇺🇿 O'zbekcha",
        callback_data="language:uz"
    ))
    
    builder.adjust(2)
    return builder.as_markup()

def get_language_settings_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура настроек языка"""
    builder = InlineKeyboardBuilder()
    
    builder.add(InlineKeyboardButton(
        text="🇷🇺 Русский",
        callback_data="set_language:ru"
    ))
    builder.add(InlineKeyboardButton(
        text="🇺🇿 O'zbekcha", 
        callback_data="set_language:uz"
    ))
    builder.add(InlineKeyboardButton(
        text="🔙 Назад / Orqaga",
        callback_data="back_to_main"
    ))
    
    builder.adjust(2, 1)
    return builder.as_markup() 