"""
Переводы для бота знакомств
Поддерживаемые языки: русский, узбекский
"""

TRANSLATIONS = {
    'ru': {
        # Общие фразы
        'welcome': '👋 Добро пожаловать в бот знакомств!',
        'choose_language': '🌍 Выберите язык / Tilni tanlang:',
        'language_changed': '✅ Язык изменен на русский',
        'back_to_main': '🔙 Вернуться в главное меню',
        'error_occurred': '❌ Произошла ошибка',
        'loading': '⏳ Загрузка...',
        
        # Регистрация
        'registration_start': '🎯 Начнем регистрацию! Сначала укажите ваш пол:',
        'registration_gender': 'Выберите ваш пол:',
        'registration_age': 'Введите ваш возраст (от 18 до 100):',
        'registration_height': 'Введите ваш рост в см (от 140 до 220):',
        'registration_weight': 'Введите ваш вес в кг (от 40 до 200):',
        'registration_marital': 'Выберите ваше семейное положение:',
        'registration_interests': 'Выберите ваши интересы (можно выбрать несколько):',
        'registration_bio': 'Расскажите о себе (необязательно):',
        'registration_complete': '✅ Регистрация завершена! Теперь вы можете искать людей.',
        
        # Главное меню
        'main_menu': '👋 Выберите действие:',
        'search_people': '🔍 Найти людей',
        'my_profile': '👤 Мой профиль',
        'edit_profile': '✏️ Редактировать профиль',
        'search_settings': '⚙️ Настройки поиска',
        'requests': '📨 Запросы',
        'language_settings': '🌍 Язык',
        
        # Поиск
        'search_start': '🔍 Начинаем поиск подходящих людей...',
        'search_no_results': '😔 К сожалению, не найдено подходящих людей. Попробуйте изменить настройки поиска.',
        'search_found': '✅ Найдено подходящих людей: {count}',
        'search_next': '➡️ Следующий',
        'search_previous': '⬅️ Предыдущий',
        'search_request_access': '💬 Запросить доступ',
        'search_no_more': '😔 Больше людей не найдено',
        
        # Профиль
        'profile_title': '👤 Мой профиль:',
        'profile_gender': 'Пол: {gender}',
        'profile_age': 'Возраст: {age}',
        'profile_height': 'Рост: {height} см',
        'profile_weight': 'Вес: {weight} кг',
        'profile_marital': 'Семейное положение: {status}',
        'profile_interests': 'Интересы: {interests}',
        'profile_bio': 'О себе: {bio}',
        'profile_no_bio': 'О себе: не указано',
        
        # Настройки поиска
        'settings_title': '⚙️ Настройки поиска:',
        'settings_gender': 'Предпочитаемый пол: {preference}',
        'settings_age': 'Возраст: от {min} до {max}',
        'settings_height': 'Рост: от {min} до {max} см',
        'settings_weight': 'Вес: от {min} до {max} кг',
        'settings_marital': 'Семейное положение: {preference}',
        'settings_change_gender': 'Изменить предпочитаемый пол',
        'settings_change_age': 'Изменить возрастной диапазон',
        'settings_change_height': 'Изменить диапазон роста',
        'settings_change_weight': 'Изменить диапазон веса',
        'settings_change_marital': 'Изменить семейное положение',
        
        # Запросы
        'requests_title': '📨 Входящие запросы:',
        'requests_empty': 'У вас пока нет входящих запросов',
        'requests_from': 'Запрос от: {name}',
        'requests_accept': '✅ Принять',
        'requests_decline': '❌ Отклонить',
        'requests_accepted': '✅ Запрос принят!',
        'requests_declined': '❌ Запрос отклонен',
        'requests_access_granted': '✅ Вам предоставлен доступ к профилю!',
        'requests_username_sent': '👤 Имя пользователя отправлено',
        
        # Уведомления
        'notification_new_request': '📨 Новый запрос на доступ!',
        'notification_request_from': 'От: {name}',
        'notification_access_granted': '✅ Вам предоставлен доступ к профилю!',
        'notification_username': '👤 Имя пользователя: @{username}',
        
        # Ошибки
        'error_invalid_age': '❌ Возраст должен быть от 18 до 100',
        'error_invalid_height': '❌ Рост должен быть от 140 до 220 см',
        'error_invalid_weight': '❌ Вес должен быть от 40 до 200 кг',
        'error_already_registered': '❌ Вы уже зарегистрированы',
        'error_not_registered': '❌ Вы не зарегистрированы. Начните с /start',
        'error_daily_limit': '❌ Достигнут дневной лимит запросов ({limit})',
        'error_already_requested': '❌ Вы уже отправляли запрос этому пользователю',
        
        # Кнопки
        'btn_male': 'Мужчина',
        'btn_female': 'Женщина',
        'btn_single': 'Холост/Не замужем',
        'btn_married': 'Женат/Замужем',
        'btn_divorced': 'Разведен/Разведена',
        'btn_all': 'Все',
        'btn_males': 'Мужчины',
        'btn_females': 'Женщины',
        'btn_done': 'Готово',
        'btn_cancel': 'Отмена',
        'btn_save': 'Сохранить',
        'btn_edit': 'Изменить',
        'btn_delete': 'Удалить',
        'btn_yes': 'Да',
        'btn_no': 'Нет',
        
        # Дополнительные кнопки
        'edit_interests': '🎯 Изменить интересы',
        'edit_bio': '💬 Изменить описание',
        
        # Интересы
        'interests_sport': 'Спорт',
        'interests_music': 'Музыка',
        'interests_movies': 'Кино',
        'interests_books': 'Книги',
        'interests_travel': 'Путешествия',
        'interests_cooking': 'Кулинария',
        'interests_art': 'Искусство',
        'interests_tech': 'Технологии',
        'interests_nature': 'Природа',
        'interests_photo': 'Фотография',
        'interests_dance': 'Танцы',
        'interests_yoga': 'Йога',
        'interests_games': 'Игры',
        'interests_science': 'Наука',
    },
    
    'uz': {
        # Общие фразы
        'welcome': '👋 Tanishuv botiga xush kelibsiz!',
        'choose_language': '🌍 Tilni tanlang / Выберите язык:',
        'language_changed': '✅ Til o\'zbekchaga o\'zgartirildi',
        'back_to_main': '🔙 Bosh menyuga qaytish',
        'error_occurred': '❌ Xatolik yuz berdi',
        'loading': '⏳ Yuklanmoqda...',
        
        # Регистрация
        'registration_start': '🎯 Ro\'yxatdan o\'tishni boshlaymiz! Avval jinsingizni ko\'rsating:',
        'registration_gender': 'Jinsingizni tanlang:',
        'registration_age': 'Yoshingizni kiriting (18 dan 100 gacha):',
        'registration_height': 'Bo\'yingizni sm da kiriting (140 dan 220 gacha):',
        'registration_weight': 'Vazningizni kg da kiriting (40 dan 200 gacha):',
        'registration_marital': 'Oilaviy ahvolingizni tanlang:',
        'registration_interests': 'Qiziqishlaringizni tanlang (bir nechtasini tanlash mumkin):',
        'registration_bio': 'O\'zingiz haqida gapirib bering (ixtiyoriy):',
        'registration_complete': '✅ Ro\'yxatdan o\'tish tugallandi! Endi odamlarni qidirishingiz mumkin.',
        
        # Главное меню
        'main_menu': '👋 Amalni tanlang:',
        'search_people': '🔍 Odamlarni qidirish',
        'my_profile': '👤 Mening profilim',
        'edit_profile': '✏️ Profilni tahrirlash',
        'search_settings': '⚙️ Qidiruv sozlamalari',
        'requests': '📨 So\'rovlar',
        'language_settings': '🌍 Til',
        
        # Поиск
        'search_start': '🔍 Mos odamlarni qidirishni boshlaymiz...',
        'search_no_results': '😔 Afsuski, mos odamlar topilmadi. Qidiruv sozlamalarini o\'zgartirib ko\'ring.',
        'search_found': '✅ Mos odamlar topildi: {count}',
        'search_next': '➡️ Keyingi',
        'search_previous': '⬅️ Oldingi',
        'search_request_access': '💬 Ruxsat so\'rash',
        'search_no_more': '😔 Boshqa odamlar topilmadi',
        
        # Профиль
        'profile_title': '👤 Mening profilim:',
        'profile_gender': 'Jins: {gender}',
        'profile_age': 'Yosh: {age}',
        'profile_height': 'Bo\'y: {height} sm',
        'profile_weight': 'Vazn: {weight} kg',
        'profile_marital': 'Oilaviy ahvol: {status}',
        'profile_interests': 'Qiziqishlar: {interests}',
        'profile_bio': 'O\'zim haqimda: {bio}',
        'profile_no_bio': 'O\'zim haqimda: ko\'rsatilmagan',
        
        # Настройки поиска
        'settings_title': '⚙️ Qidiruv sozlamalari:',
        'settings_gender': 'Afzal ko\'rilgan jins: {preference}',
        'settings_age': 'Yosh: {min} dan {max} gacha',
        'settings_height': 'Bo\'y: {min} dan {max} sm gacha',
        'settings_weight': 'Vazn: {min} dan {max} kg gacha',
        'settings_marital': 'Oilaviy ahvol: {preference}',
        'settings_change_gender': 'Afzal ko\'rilgan jinsni o\'zgartirish',
        'settings_change_age': 'Yosh oralig\'ini o\'zgartirish',
        'settings_change_height': 'Bo\'y oralig\'ini o\'zgartirish',
        'settings_change_weight': 'Vazn oralig\'ini o\'zgartirish',
        'settings_change_marital': 'Oilaviy ahvolni o\'zgartirish',
        
        # Запросы
        'requests_title': '📨 Kelgan so\'rovlar:',
        'requests_empty': 'Hozircha kelgan so\'rovlaringiz yo\'q',
        'requests_from': 'So\'rov kimdan: {name}',
        'requests_accept': '✅ Qabul qilish',
        'requests_decline': '❌ Rad etish',
        'requests_accepted': '✅ So\'rov qabul qilindi!',
        'requests_declined': '❌ So\'rov rad etildi',
        'requests_access_granted': '✅ Profilga ruxsat berildi!',
        'requests_username_sent': '👤 Foydalanuvchi nomi yuborildi',
        
        # Уведомления
        'notification_new_request': '📨 Ruxsat uchun yangi so\'rov!',
        'notification_request_from': 'Kimdan: {name}',
        'notification_access_granted': '✅ Profilga ruxsat berildi!',
        'notification_username': '👤 Foydalanuvchi nomi: @{username}',
        
        # Ошибки
        'error_invalid_age': '❌ Yosh 18 dan 100 gacha bo\'lishi kerak',
        'error_invalid_height': '❌ Bo\'y 140 dan 220 sm gacha bo\'lishi kerak',
        'error_invalid_weight': '❌ Vazn 40 dan 200 kg gacha bo\'lishi kerak',
        'error_already_registered': '❌ Siz allaqachon ro\'yxatdan o\'tgansiz',
        'error_not_registered': '❌ Siz ro\'yxatdan o\'tmagansiz. /start bilan boshlang',
        'error_daily_limit': '❌ Kunlik so\'rovlar chegarasiga yetildi ({limit})',
        'error_already_requested': '❌ Siz allaqachon bu foydalanuvchiga so\'rov yuborgansiz',
        
        # Кнопки
        'btn_male': 'Erkak',
        'btn_female': 'Ayol',
        'btn_single': 'Bekor/Erkak emas',
        'btn_married': 'Uylangan/Turmush qurgan',
        'btn_divorced': 'Ajrashgan/Ajrashgan',
        'btn_all': 'Hammasi',
        'btn_males': 'Erkaklar',
        'btn_females': 'Ayollar',
        'btn_done': 'Tayyor',
        'btn_cancel': 'Bekor qilish',
        'btn_save': 'Saqlash',
        'btn_edit': 'O\'zgartirish',
        'btn_delete': 'O\'chirish',
        'btn_yes': 'Ha',
        'btn_no': 'Yo\'q',
        
        # Дополнительные кнопки
        'edit_interests': '🎯 Qiziqishlarni o\'zgartirish',
        'edit_bio': '💬 Tavsifni o\'zgartirish',
        
        # Интересы
        'interests_sport': 'Sport',
        'interests_music': 'Musiqa',
        'interests_movies': 'Kino',
        'interests_books': 'Kitoblar',
        'interests_travel': 'Sayohat',
        'interests_cooking': 'Oshpazlik',
        'interests_art': 'San\'at',
        'interests_tech': 'Texnologiya',
        'interests_nature': 'Tabiat',
        'interests_photo': 'Fotografiya',
        'interests_dance': 'Raqs',
        'interests_yoga': 'Yoga',
        'interests_games': 'O\'yinlar',
        'interests_science': 'Fan',
    }
}

def get_text(key: str, lang: str = 'ru', **kwargs) -> str:
    """
    Получить переведенный текст
    
    Args:
        key: Ключ перевода
        lang: Язык ('ru' или 'uz')
        **kwargs: Параметры для форматирования
    
    Returns:
        Переведенный текст
    """
    if lang not in TRANSLATIONS:
        lang = 'ru'  # По умолчанию русский
    
    text = TRANSLATIONS[lang].get(key, TRANSLATIONS['ru'].get(key, key))
    
    # Форматируем текст с параметрами
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass
    
    return text

def get_supported_languages() -> list:
    """Получить список поддерживаемых языков"""
    return list(TRANSLATIONS.keys())

def is_supported_language(lang: str) -> bool:
    """Проверить, поддерживается ли язык"""
    return lang in TRANSLATIONS 