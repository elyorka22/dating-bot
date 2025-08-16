from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import MARITAL_STATUSES
from locales.translations import get_text

def get_settings_menu_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Клавиатура меню настроек"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text=get_text('settings_change_gender', lang),
        callback_data="change_gender_preference"
    ))
    builder.add(InlineKeyboardButton(
        text=get_text('settings_change_age', lang),
        callback_data="change_age_range"
    ))
    builder.add(InlineKeyboardButton(
        text=get_text('settings_change_height', lang),
        callback_data="change_height_range"
    ))
    builder.add(InlineKeyboardButton(
        text=get_text('settings_change_weight', lang),
        callback_data="change_weight_range"
    ))
    builder.add(InlineKeyboardButton(
        text=get_text('settings_change_marital', lang),
        callback_data="change_marital_preference"
    ))
    builder.add(InlineKeyboardButton(
        text=get_text('back_to_main', lang),
        callback_data="back_to_main"
    ))
    builder.adjust(2)
    return builder.as_markup()

def get_gender_preference_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Клавиатура для выбора предпочтений по полу"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text=get_text('btn_males', lang),
        callback_data="gender_pref:Мужчины"
    ))
    builder.add(InlineKeyboardButton(
        text=get_text('btn_females', lang),
        callback_data="gender_pref:Женщины"
    ))
    builder.add(InlineKeyboardButton(
        text=get_text('btn_all', lang),
        callback_data="gender_pref:Все"
    ))
    builder.add(InlineKeyboardButton(
        text=get_text('back_to_main', lang),
        callback_data="search_settings"
    ))
    builder.adjust(2)
    return builder.as_markup()

def get_marital_preference_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Клавиатура для выбора предпочтений по семейному положению"""
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
            callback_data=f"marital_pref:{status}"
        ))
    
    builder.add(InlineKeyboardButton(
        text=get_text('btn_all', lang),
        callback_data="marital_pref:all"
    ))
    builder.add(InlineKeyboardButton(
        text=get_text('back_to_main', lang),
        callback_data="search_settings"
    ))
    builder.adjust(1)
    return builder.as_markup()

def get_age_range_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Клавиатура для быстрого выбора возрастных диапазонов"""
    builder = InlineKeyboardBuilder()
    age_ranges = [
        ("18-25", "18-25"),
        ("26-35", "26-35"),
        ("36-45", "36-45"),
        ("46-55", "46-55"),
        ("56+", "56-100")
    ]
    
    for text, data in age_ranges:
        builder.add(InlineKeyboardButton(
            text=text,
            callback_data=f"age_range:{data}"
        ))
    
    builder.add(InlineKeyboardButton(
        text=get_text('back_to_main', lang),
        callback_data="search_settings"
    ))
    builder.adjust(2)
    return builder.as_markup()

def get_height_range_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Клавиатура для быстрого выбора диапазонов роста"""
    builder = InlineKeyboardBuilder()
    height_ranges = [
        ("150-160", "150-160"),
        ("161-170", "161-170"),
        ("171-180", "171-180"),
        ("181-190", "181-190"),
        ("191+", "191-220")
    ]
    
    for text, data in height_ranges:
        builder.add(InlineKeyboardButton(
            text=text,
            callback_data=f"height_range:{data}"
        ))
    
    builder.add(InlineKeyboardButton(
        text=get_text('back_to_main', lang),
        callback_data="search_settings"
    ))
    builder.adjust(2)
    return builder.as_markup()

def get_weight_range_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Клавиатура для быстрого выбора диапазонов веса"""
    builder = InlineKeyboardBuilder()
    weight_ranges = [
        ("40-50", "40-50"),
        ("51-60", "51-60"),
        ("61-70", "61-70"),
        ("71-80", "71-80"),
        ("81-90", "81-90"),
        ("91+", "91-200")
    ]
    
    for text, data in weight_ranges:
        builder.add(InlineKeyboardButton(
            text=text,
            callback_data=f"weight_range:{data}"
        ))
    
    builder.add(InlineKeyboardButton(
        text=get_text('back_to_main', lang),
        callback_data="search_settings"
    ))
    builder.adjust(2)
    return builder.as_markup() 