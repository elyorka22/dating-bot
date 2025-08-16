from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import INTERESTS
from locales.translations import get_text

def get_profile_edit_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Клавиатура для редактирования профиля"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text=get_text('settings_change_age', lang),
        callback_data="edit_age"
    ))
    builder.add(InlineKeyboardButton(
        text=get_text('settings_change_height', lang),
        callback_data="edit_height"
    ))
    builder.add(InlineKeyboardButton(
        text=get_text('settings_change_weight', lang),
        callback_data="edit_weight"
    ))
    builder.add(InlineKeyboardButton(
        text=get_text('settings_change_marital', lang),
        callback_data="edit_marital"
    ))
    builder.add(InlineKeyboardButton(
        text="🎯 Изменить интересы",  # Добавим перевод в translations.py
        callback_data="edit_interests"
    ))
    builder.add(InlineKeyboardButton(
        text="💬 Изменить описание",  # Добавим перевод в translations.py
        callback_data="edit_bio"
    ))
    builder.add(InlineKeyboardButton(
        text=get_text('back_to_main', lang),
        callback_data="back_to_main"
    ))
    builder.adjust(2)
    return builder.as_markup()

def get_interests_edit_keyboard(selected_interests: list = None, lang: str = 'ru') -> InlineKeyboardMarkup:
    """Клавиатура для редактирования интересов"""
    if selected_interests is None:
        selected_interests = []
    
    builder = InlineKeyboardBuilder()
    
    # Словарь переводов для интересов
    interest_translations = {
        "Спорт": get_text('interests_sport', lang),
        "Музыка": get_text('interests_music', lang),
        "Кино": get_text('interests_movies', lang),
        "Книги": get_text('interests_books', lang),
        "Путешествия": get_text('interests_travel', lang),
        "Кулинария": get_text('interests_cooking', lang),
        "Искусство": get_text('interests_art', lang),
        "Технологии": get_text('interests_tech', lang),
        "Природа": get_text('interests_nature', lang),
        "Фотография": get_text('interests_photo', lang),
        "Танцы": get_text('interests_dance', lang),
        "Йога": get_text('interests_yoga', lang),
        "Игры": get_text('interests_games', lang),
        "Наука": get_text('interests_science', lang)
    }
    
    for interest in INTERESTS:
        translated_interest = interest_translations.get(interest, interest)
        if interest in selected_interests:
            text = f"✅ {translated_interest}"
        else:
            text = f"⬜ {translated_interest}"
        
        builder.add(InlineKeyboardButton(
            text=text,
            callback_data=f"interest_edit:{interest}"
        ))
    
    builder.add(InlineKeyboardButton(
        text=get_text('btn_save', lang),
        callback_data="interests_save"
    ))
    builder.add(InlineKeyboardButton(
        text=get_text('back_to_main', lang),
        callback_data="edit_profile"
    ))
    
    builder.adjust(2)
    return builder.as_markup() 