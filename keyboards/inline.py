from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import GENDERS, MARITAL_STATUSES, INTERESTS
from locales.translations import get_text

def get_gender_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Клавиатура для выбора пола"""
    builder = InlineKeyboardBuilder()
    for gender in GENDERS:
        # Переводим текст кнопки
        if gender == "Мужчина":
            text = get_text('btn_male', lang)
        elif gender == "Женщина":
            text = get_text('btn_female', lang)
        else:
            text = gender
            
        builder.add(InlineKeyboardButton(
            text=text,
            callback_data=f"gender:{gender}"
        ))
    builder.adjust(2)
    return builder.as_markup()

def get_age_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Клавиатура для выбора возрастных групп"""
    builder = InlineKeyboardBuilder()
    age_groups = [
        ("18-25", "18-25"),
        ("26-35", "26-35"),
        ("36-45", "36-45"),
        ("46+", "46+")
    ]
    for text, data in age_groups:
        builder.add(InlineKeyboardButton(
            text=text,
            callback_data=f"age_group:{data}"
        ))
    builder.adjust(2)
    return builder.as_markup()

def get_marital_status_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Клавиатура для выбора семейного положения"""
    builder = InlineKeyboardBuilder()
    
    # Словарь переводов для семейного положения
    marital_translations = {
        "Холост/Не замужем": get_text('btn_single', lang),
        "Женат/Замужем": get_text('btn_married', lang),
        "Разведен/Разведена": get_text('btn_divorced', lang)
    }
    
    for status in MARITAL_STATUSES:
        text = marital_translations.get(status, status)
        builder.add(InlineKeyboardButton(
            text=text,
            callback_data=f"marital:{status}"
        ))
    builder.adjust(1)
    return builder.as_markup()

def get_interests_keyboard(selected_interests: list = None, lang: str = 'ru') -> InlineKeyboardMarkup:
    """Клавиатура для выбора интересов"""
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
            callback_data=f"interest:{interest}"
        ))
    
    builder.add(InlineKeyboardButton(
        text=get_text('btn_done', lang),
        callback_data="interests_done"
    ))
    
    builder.adjust(2)
    return builder.as_markup()

def get_search_action_keyboard(user_id: int, lang: str = 'ru') -> InlineKeyboardMarkup:
    """Клавиатура для действий поиска"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text=get_text('search_request_access', lang),
        callback_data=f"request_access:{user_id}"
    ))
    builder.add(InlineKeyboardButton(
        text=get_text('search_next', lang),
        callback_data="skip_profile"
    ))
    builder.adjust(1)
    return builder.as_markup()

def get_access_request_keyboard(request_id: int, lang: str = 'ru') -> InlineKeyboardMarkup:
    """Клавиатура для ответа на запрос доступа"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text=get_text('requests_accept', lang),
        callback_data=f"accept_request:{request_id}"
    ))
    builder.add(InlineKeyboardButton(
        text=get_text('requests_decline', lang),
        callback_data=f"reject_request:{request_id}"
    ))
    builder.adjust(2)
    return builder.as_markup()

def get_main_menu_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Главное меню"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text=get_text('search_people', lang),
        callback_data="search"
    ))
    builder.add(InlineKeyboardButton(
        text=get_text('my_profile', lang),
        callback_data="profile"
    ))
    builder.add(InlineKeyboardButton(
        text=get_text('edit_profile', lang),
        callback_data="edit_profile"
    ))
    builder.add(InlineKeyboardButton(
        text=get_text('search_settings', lang),
        callback_data="search_settings"
    ))
    builder.add(InlineKeyboardButton(
        text=get_text('requests', lang),
        callback_data="requests"
    ))
    builder.add(InlineKeyboardButton(
        text=get_text('language_settings', lang),
        callback_data="language_settings"
    ))
    builder.adjust(2)
    return builder.as_markup() 