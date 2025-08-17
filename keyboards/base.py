from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from locales.translations import get_text
from config import GENDERS, MARITAL_STATUSES, INTERESTS

def get_language_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора языка"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz")
        ]
    ])
    return keyboard

def get_gender_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Клавиатура выбора пола"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👨 Мужчина", callback_data="gender_male"),
            InlineKeyboardButton(text="👩 Женщина", callback_data="gender_female")
        ] if lang == 'ru' else [
            InlineKeyboardButton(text="👨 Erkak", callback_data="gender_male"),
            InlineKeyboardButton(text="👩 Ayol", callback_data="gender_female")
        ],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
    ])
    return keyboard

def get_marital_status_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Клавиатура семейного положения"""
    if lang == 'ru':
        buttons = [
            [InlineKeyboardButton(text="💚 Холост/Не замужем", callback_data="marital_single")],
            [InlineKeyboardButton(text="💍 Женат/Замужем", callback_data="marital_married")],
            [InlineKeyboardButton(text="💔 Разведен/Разведена", callback_data="marital_divorced")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
        ]
    else:
        buttons = [
            [InlineKeyboardButton(text="💚 Bekor/Erkak emas", callback_data="marital_single")],
            [InlineKeyboardButton(text="💍 Uylangan/Turmush qurgan", callback_data="marital_married")],
            [InlineKeyboardButton(text="💔 Ajrashgan/Ajrashgan", callback_data="marital_divorced")],
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel")]
        ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_interests_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Клавиатура интересов"""
    interests_ru = ["Спорт", "Музыка", "Кино", "Книги", "Путешествия", "Кулинария", "Искусство", "Технологии", "Природа", "Фотография", "Танцы", "Йога", "Игры", "Наука"]
    interests_uz = ["Sport", "Musiqa", "Kino", "Kitoblar", "Sayohat", "Oshpazlik", "San'at", "Texnologiya", "Tabiat", "Fotografiya", "Raqs", "Yoga", "O'yinlar", "Fan"]
    
    interests = interests_ru if lang == 'ru' else interests_uz
    
    buttons = []
    for i in range(0, len(interests), 2):
        row = []
        row.append(InlineKeyboardButton(text=interests[i], callback_data=f"interest_{interests[i]}"))
        if i + 1 < len(interests):
            row.append(InlineKeyboardButton(text=interests[i + 1], callback_data=f"interest_{interests[i + 1]}"))
        buttons.append(row)
    
    # Кнопка "Готово"
    done_text = "✅ Готово" if lang == 'ru' else "✅ Tayyor"
    buttons.append([InlineKeyboardButton(text=done_text, callback_data="interests_done")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_main_menu_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Главное меню"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text('create_profile', lang), callback_data="create_profile")],
        [InlineKeyboardButton(text=get_text('search', lang), callback_data="menu_search")],
        [InlineKeyboardButton(text=get_text('profile', lang), callback_data="menu_profile")],
        [InlineKeyboardButton(text=get_text('requests', lang), callback_data="menu_requests")],
        [InlineKeyboardButton(text=get_text('settings', lang), callback_data="menu_settings")]
    ])
    return keyboard

def get_profile_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Клавиатура профиля"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text('edit_profile', lang), callback_data="profile_edit")],
        [InlineKeyboardButton(text=get_text('back_to_menu', lang), callback_data="back_to_main")]
    ])
    return keyboard

def get_search_gender_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Клавиатура поиска по полу"""
    if lang == 'ru':
        buttons = [
            [InlineKeyboardButton(text="👨 Мужчин", callback_data="search_gender_male")],
            [InlineKeyboardButton(text="👩 Женщин", callback_data="search_gender_female")],
            [InlineKeyboardButton(text="👥 Всех", callback_data="search_gender_all")]
        ]
    else:
        buttons = [
            [InlineKeyboardButton(text="👨 Erkaklar", callback_data="search_gender_male")],
            [InlineKeyboardButton(text="👩 Ayollar", callback_data="search_gender_female")],
            [InlineKeyboardButton(text="👥 Hammasi", callback_data="search_gender_all")]
        ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_user_profile_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Клавиатура профиля пользователя"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text('send_request', lang), callback_data="send_request")],
        [InlineKeyboardButton(text=get_text('next_user', lang), callback_data="next_user")],
        [InlineKeyboardButton(text=get_text('back_to_menu', lang), callback_data="back_to_main")]
    ])
    return keyboard

def get_request_actions_keyboard(request_id: int, lang: str = 'ru') -> InlineKeyboardMarkup:
    """Клавиатура действий с запросом"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text('accept_request', lang), callback_data=f"accept_request_{request_id}"),
            InlineKeyboardButton(text=get_text('decline_request', lang), callback_data=f"decline_request_{request_id}")
        ],
        [InlineKeyboardButton(text=get_text('back_to_menu', lang), callback_data="back_to_main")]
    ])
    return keyboard

def get_settings_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Клавиатура настроек"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text('search_settings', lang), callback_data="settings_search")],
        [InlineKeyboardButton(text=get_text('change_language', lang), callback_data="settings_language")],
        [InlineKeyboardButton(text=get_text('back_to_menu', lang), callback_data="back_to_main")]
    ])
    return keyboard

def get_cancel_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Клавиатура отмены"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text('cancel', lang), callback_data="cancel")]
    ])
    return keyboard 