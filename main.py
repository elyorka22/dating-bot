#!/usr/bin/env python3
import os
import sys
import asyncio
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.orm import Session

# Импорты из нашего проекта
from config import BOT_TOKEN, DATABASE_URL, GENDERS, MARITAL_STATUSES, MIN_AGE, MAX_AGE, MIN_HEIGHT, MAX_HEIGHT, MIN_WEIGHT, MAX_WEIGHT
from database.database import get_db, create_tables, check_database_connection
from database.models import User, Request
from handlers.user import get_user_by_telegram_id, create_user, update_user_profile, search_users, is_profile_complete, get_user_profile_text
from handlers.requests import create_request, get_user_requests, update_request_status, can_send_request, get_request_by_id
from keyboards.base import *
from locales.translations import get_text

print("=== ЗАПУСК TELEGRAM БОТА ЗНАКОМСТВ ===")
print(f"Python версия: {sys.version}")
print(f"Текущая директория: {os.getcwd()}")
print(f"PORT: {os.environ.get('PORT', 'НЕ УСТАНОВЛЕН')}")

# Состояния FSM
class RegistrationStates(StatesGroup):
    waiting_for_gender = State()
    waiting_for_age = State()
    waiting_for_height = State()
    waiting_for_weight = State()
    waiting_for_marital_status = State()
    waiting_for_bio = State()

class SearchStates(StatesGroup):
    waiting_for_gender = State()
    waiting_for_age_range = State()
    waiting_for_height_range = State()
    waiting_for_weight_range = State()

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()

# Хранилище для поиска пользователей
user_search_results = {}

# Обработчик команды /start
@router.message(Command("start"))
async def cmd_start(message: Message):
    db = next(get_db())
    user = get_user_by_telegram_id(message.from_user.id, db)
    
    if not user:
        # Создаем нового пользователя
        user = create_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            db=db
        )
        await message.answer(get_text('welcome', 'ru'), reply_markup=get_language_keyboard())
    else:
        # Показываем главное меню
        await message.answer(get_text('main_menu', user.language), reply_markup=get_main_menu_keyboard(user.language))

# Обработчик выбора языка
@router.callback_query(lambda c: c.data.startswith('lang_'))
async def process_language_selection(callback: CallbackQuery):
    lang = callback.data.split('_')[1]
    db = next(get_db())
    user = get_user_by_telegram_id(callback.from_user.id, db)
    
    if user:
        update_user_profile(user.id, language=lang)
        await callback.message.edit_text(
            get_text('language_changed', lang),
            reply_markup=get_main_menu_keyboard(lang)
        )
    else:
        await callback.message.edit_text(get_text('error', lang))

# Обработчик создания профиля
@router.callback_query(lambda c: c.data == 'create_profile')
async def start_profile_creation(callback: CallbackQuery, state: FSMContext):
    await state.set_state(RegistrationStates.waiting_for_gender)
    await callback.message.edit_text(
        get_text('enter_gender', 'ru'),
        reply_markup=get_gender_keyboard('ru')
    )

# Обработчик выбора пола
@router.callback_query(lambda c: c.data.startswith('gender_'))
async def process_gender_selection(callback: CallbackQuery, state: FSMContext):
    gender = callback.data.split('_')[1]
    await state.update_data(gender=gender)
    await state.set_state(RegistrationStates.waiting_for_age)
    
    # Получаем язык пользователя
    db = next(get_db())
    user = get_user_by_telegram_id(callback.from_user.id, db)
    lang = user.language if user else 'ru'
    
    gender_text = "Мужчина" if gender == "male" else "Женщина"
    if lang == 'uz':
        gender_text = "Erkak" if gender == "male" else "Ayol"
    
    await callback.message.edit_text(
        f"{get_text('you_selected', lang, value=gender_text)}\n\n{get_text('enter_age', lang)} ({MIN_AGE}-{MAX_AGE}):"
    )

# Обработчик ввода возраста
@router.message(RegistrationStates.waiting_for_age)
async def process_age_input(message: Message, state: FSMContext):
    try:
        age = int(message.text)
        if MIN_AGE <= age <= MAX_AGE:
            await state.update_data(age=age)
            await state.set_state(RegistrationStates.waiting_for_height)
            
            # Получаем язык пользователя
            db = next(get_db())
            user = get_user_by_telegram_id(message.from_user.id, db)
            lang = user.language if user else 'ru'
            
            await message.answer(
                f"{get_text('age_value', lang, age=age)}\n\n{get_text('enter_height', lang)} ({MIN_HEIGHT}-{MAX_HEIGHT} см):",
                reply_markup=get_cancel_keyboard(lang)
            )
        else:
            await message.answer(get_text('age_range_error', 'ru', min=MIN_AGE, max=MAX_AGE))
    except ValueError:
        await message.answer(get_text('please_enter_number', 'ru'))

# Обработчик ввода роста
@router.message(RegistrationStates.waiting_for_height)
async def process_height_input(message: Message, state: FSMContext):
    try:
        height = int(message.text)
        if MIN_HEIGHT <= height <= MAX_HEIGHT:
            await state.update_data(height=height)
            await state.set_state(RegistrationStates.waiting_for_weight)
            
            # Получаем язык пользователя
            db = next(get_db())
            user = get_user_by_telegram_id(message.from_user.id, db)
            lang = user.language if user else 'ru'
            
            await message.answer(
                f"{get_text('height_value', lang, height=height)}\n\n{get_text('enter_weight', lang)} ({MIN_WEIGHT}-{MAX_WEIGHT} кг):",
                reply_markup=get_cancel_keyboard(lang)
            )
        else:
            await message.answer(get_text('height_range_error', 'ru', min=MIN_HEIGHT, max=MAX_HEIGHT))
    except ValueError:
        await message.answer(get_text('please_enter_number', 'ru'))

# Обработчик ввода веса
@router.message(RegistrationStates.waiting_for_weight)
async def process_weight_input(message: Message, state: FSMContext):
    try:
        weight = int(message.text)
        if MIN_WEIGHT <= weight <= MAX_WEIGHT:
            await state.update_data(weight=weight)
            await state.set_state(RegistrationStates.waiting_for_marital_status)
            
            # Получаем язык пользователя
            db = next(get_db())
            user = get_user_by_telegram_id(message.from_user.id, db)
            lang = user.language if user else 'ru'
            
            await message.answer(
                f"{get_text('weight_value', lang, weight=weight)}\n\n{get_text('enter_marital_status', lang)}",
                reply_markup=get_marital_status_keyboard(lang)
            )
        else:
            await message.answer(get_text('weight_range_error', 'ru', min=MIN_WEIGHT, max=MAX_WEIGHT))
    except ValueError:
        await message.answer(get_text('please_enter_number', 'ru'))

# Обработчик выбора семейного положения
@router.callback_query(lambda c: c.data.startswith('marital_'))
async def process_marital_status_selection(callback: CallbackQuery, state: FSMContext):
    marital_status = callback.data.split('_')[1]
    await state.update_data(marital_status=marital_status)
    await state.set_state(RegistrationStates.waiting_for_bio)
    
    # Получаем язык пользователя
    db = next(get_db())
    user = get_user_by_telegram_id(callback.from_user.id, db)
    lang = user.language if user else 'ru'
    
    status_text = {
        'single': 'Холост/Не замужем' if lang == 'ru' else 'Bekor/Erkak emas',
        'married': 'Женат/Замужем' if lang == 'ru' else 'Uylangan/Turmush qurgan',
        'divorced': 'Разведен/Разведена' if lang == 'ru' else 'Ajrashgan/Ajrashgan'
    }.get(marital_status, marital_status)
    
    await callback.message.edit_text(
        f"{get_text('marital_status_value', lang, status=status_text)}\n\n{get_text('enter_bio', lang)} (или отправьте '-' чтобы пропустить):",
        reply_markup=get_cancel_keyboard(lang)
    )

# Обработчик ввода описания
@router.message(RegistrationStates.waiting_for_bio)
async def process_bio_input(message: Message, state: FSMContext):
    bio = message.text if message.text != '-' else None
    await state.update_data(bio=bio)
    
    # Получаем все данные
    data = await state.get_data()
    
    # Сохраняем профиль в базу данных
    db = next(get_db())
    user = get_user_by_telegram_id(message.from_user.id, db)
    
    if user:
        update_user_profile(
            user.id,
            gender=data['gender'],
            age=data['age'],
            height=data['height'],
            weight=data['weight'],
            marital_status=data['marital_status'],
            bio=data['bio']
        )
        
        await state.clear()
        await message.answer(
            get_text('profile_created', user.language),
            reply_markup=get_main_menu_keyboard(user.language)
        )
    else:
        await message.answer(get_text('user_not_found', 'ru'))

# Обработчик редактирования профиля
@router.callback_query(lambda c: c.data == 'profile_edit')
async def start_profile_edit(callback: CallbackQuery, state: FSMContext):
    await state.set_state(RegistrationStates.waiting_for_gender)
    
    # Получаем язык пользователя
    db = next(get_db())
    user = get_user_by_telegram_id(callback.from_user.id, db)
    lang = user.language if user else 'ru'
    
    await callback.message.edit_text(
        f"{get_text('edit_profile_title', lang)}\n\n{get_text('enter_gender', lang)}:",
        reply_markup=get_gender_keyboard(lang)
    )

# Обработчик отмены
@router.callback_query(lambda c: c.data == 'cancel')
async def cancel_action(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    db = next(get_db())
    user = get_user_by_telegram_id(callback.from_user.id, db)
    await callback.message.edit_text(
        get_text('main_menu', user.language if user else 'ru'),
        reply_markup=get_main_menu_keyboard(user.language if user else 'ru')
    )

# Обработчик главного меню
@router.callback_query(lambda c: c.data == 'back_to_main')
async def back_to_main_menu(callback: CallbackQuery):
    db = next(get_db())
    user = get_user_by_telegram_id(callback.from_user.id, db)
    await callback.message.edit_text(
        get_text('main_menu', user.language if user else 'ru'),
        reply_markup=get_main_menu_keyboard(user.language if user else 'ru')
    )

# Обработчик поиска
@router.callback_query(lambda c: c.data == 'menu_search')
async def menu_search(callback: CallbackQuery):
    db = next(get_db())
    user = get_user_by_telegram_id(callback.from_user.id, db)
    
    if not user or not is_profile_complete(user):
        await callback.message.edit_text(
            get_text('no_profile', user.language if user else 'ru'),
            reply_markup=get_main_menu_keyboard(user.language if user else 'ru')
        )
        return
    
    # Ищем пользователей
    users = search_users(user.id, db)
    if not users:
        await callback.message.edit_text(
            get_text('no_results', user.language),
            reply_markup=get_main_menu_keyboard(user.language)
        )
        return
    
    # Сохраняем результаты поиска
    user_search_results[callback.from_user.id] = users
    
    # Показываем первого пользователя
    await show_user_profile(callback.message, users[0], 0, user.language)

# Обработчик профиля
@router.callback_query(lambda c: c.data == 'menu_profile')
async def menu_profile(callback: CallbackQuery):
    db = next(get_db())
    user = get_user_by_telegram_id(callback.from_user.id, db)
    
    if not user:
        await callback.message.edit_text(
            get_text('no_profile', 'ru'),
            reply_markup=get_main_menu_keyboard('ru')
        )
        return
    
    profile_text = get_user_profile_text(user, user.language)
    await callback.message.edit_text(
        profile_text,
        reply_markup=get_profile_keyboard(user.language)
    )

# Обработчик запросов
@router.callback_query(lambda c: c.data == 'menu_requests')
async def menu_requests(callback: CallbackQuery):
    db = next(get_db())
    user = get_user_by_telegram_id(callback.from_user.id, db)
    
    if not user:
        await callback.message.edit_text(
            get_text('no_profile', 'ru'),
            reply_markup=get_main_menu_keyboard('ru')
        )
        return
    
    requests = get_user_requests(user.id, db, 'pending')
    
    if not requests:
        await callback.message.edit_text(
            get_text('no_new_requests', user.language),
            reply_markup=get_main_menu_keyboard(user.language)
        )
        return
    
    # Показываем первый запрос
    await show_request(callback.message, requests[0], user.language)

# Обработчик настроек
@router.callback_query(lambda c: c.data == 'menu_settings')
async def menu_settings(callback: CallbackQuery):
    db = next(get_db())
    user = get_user_by_telegram_id(callback.from_user.id, db)
    
    if not user:
        await callback.message.edit_text(
            get_text('no_profile', 'ru'),
            reply_markup=get_main_menu_keyboard('ru')
        )
        return
    
    await callback.message.edit_text(
        get_text('settings_title', user.language),
        reply_markup=get_settings_keyboard(user.language)
    )

# Обработчик отправки запроса
@router.callback_query(lambda c: c.data == 'send_request')
async def send_request_handler(callback: CallbackQuery):
    db = next(get_db())
    user = get_user_by_telegram_id(callback.from_user.id, db)
    
    if not user:
        await callback.answer(get_text('error', 'ru'))
        return
    
    # Получаем текущего пользователя из поиска
    if callback.from_user.id not in user_search_results:
        await callback.answer(get_text('search_results_not_found', 'ru'))
        return
    
    current_users = user_search_results[callback.from_user.id]
    # Получаем индекс из callback_data кнопки "Следующий"
    current_user_index = 0  # По умолчанию первый пользователь
    
    # Пытаемся получить индекс из callback_data
    try:
        if hasattr(callback.message, 'reply_markup') and callback.message.reply_markup:
            for row in callback.message.reply_markup.inline_keyboard:
                for button in row:
                    if button.callback_data and button.callback_data.startswith('next_user_'):
                        current_user_index = int(button.callback_data.split('_')[2])
                        break
    except:
        current_user_index = 0
    
    if current_user_index >= len(current_users):
        current_user_index = 0
    
    target_user = current_users[current_user_index]
    
    # Проверяем лимит запросов
    if not can_send_request(user.id, db):
        await callback.answer(get_text('daily_limit_reached', user.language))
        return
    
    # Создаем запрос
    request = create_request(user.id, target_user.id, db)
    if request:
        await callback.answer(get_text('request_sent', user.language))
        
        # Уведомляем получателя
        try:
            await bot.send_message(
                target_user.telegram_id,
                get_text('request_received', user.language),
                reply_markup=get_request_actions_keyboard(request.id, user.language)
            )
        except Exception as e:
            print(f"Ошибка отправки уведомления: {e}")
    else:
        await callback.answer(get_text('request_already_sent', user.language))

# Обработчик принятия/отклонения запроса
@router.callback_query(lambda c: c.data.startswith(('accept_request_', 'decline_request_')))
async def handle_request_action(callback: CallbackQuery):
    action, request_id = callback.data.split('_', 1)
    request_id = int(request_id)
    
    db = next(get_db())
    user = get_user_by_telegram_id(callback.from_user.id, db)
    
    if not user:
        await callback.answer(get_text('error', 'ru'))
        return
    
    request = get_request_by_id(request_id, db)
    if not request or request.to_user_id != user.id:
        await callback.answer(get_text('request_not_found', user.language))
        return
    
    if action == 'accept_request':
        # Принимаем запрос
        update_request_status(request_id, 'accepted', db)
        await callback.message.edit_text(get_text('request_accepted', user.language))
        
        # Уведомляем отправителя
        try:
            from_user = db.query(User).filter(User.id == request.from_user_id).first()
            if from_user and user.username:
                await bot.send_message(
                    from_user.telegram_id,
                    get_text('username_shared', user.language, username=user.username)
                )
        except Exception as e:
            print(f"Ошибка отправки уведомления: {e}")
    
    elif action == 'decline_request':
        # Отклоняем запрос
        update_request_status(request_id, 'declined', db)
        await callback.message.edit_text(get_text('request_declined', user.language))

# Обработчик следующего пользователя
@router.callback_query(lambda c: c.data.startswith('next_user'))
async def next_user_handler(callback: CallbackQuery):
    if callback.from_user.id not in user_search_results:
        await callback.answer(get_text('search_results_not_found', 'ru'))
        return
    
    users = user_search_results[callback.from_user.id]
    
    # Получаем текущий индекс
    current_index = 0
    try:
        if callback.data != 'next_user':
            current_index = int(callback.data.split('_')[2])
    except:
        current_index = 0
    
    # Показываем следующего пользователя
    if current_index + 1 < len(users):
        next_index = current_index + 1
        await show_user_profile(callback.message, users[next_index], next_index, 'ru')
    else:
        await callback.message.edit_text(
            get_text('no_results', 'ru'),
            reply_markup=get_main_menu_keyboard('ru')
        )

# Вспомогательные функции
async def show_user_profile(message: Message, user: User, index: int, lang: str = 'ru'):
    """Показать профиль пользователя"""
    profile_text = get_user_profile_text(user, lang)
    
    # Создаем клавиатуру с индексом
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text('send_request', lang), callback_data="send_request")],
        [InlineKeyboardButton(text=get_text('next_user', lang), callback_data=f"next_user_{index}")],
        [InlineKeyboardButton(text=get_text('back_to_menu', lang), callback_data="back_to_main")]
    ])
    
    await message.edit_text(profile_text, reply_markup=keyboard)

async def show_request(message: Message, request: Request, lang: str = 'ru'):
    """Показать запрос"""
    db = next(get_db())
    from_user = db.query(User).filter(User.id == request.from_user_id).first()
    
    request_text = f"📨 {get_text('request_received', lang)}\n\n"
    if from_user:
        request_text += get_text('from_user', lang, name=from_user.first_name or get_text('user_default', lang))
    
    await message.edit_text(
        request_text,
        reply_markup=get_request_actions_keyboard(request.id, lang)
    )

# HTTP сервер для healthcheck
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"Получен запрос: {self.path}")
        
        try:
            if self.path in ['/', '/health']:
                self.send_response(200)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                response = "OK - Dating Bot is running!"
                self.wfile.write(response.encode('utf-8'))
                print(f"Отправлен ответ: 200 OK для {self.path}")
            else:
                self.send_response(404)
                self.end_headers()
                print("Отправлен ответ: 404")
        except Exception as e:
            print(f"Ошибка в обработке запроса: {e}")
            try:
                self.send_response(500)
                self.end_headers()
            except:
                pass

    def log_message(self, format, *args):
        print(f"HTTP: {format % args}")

# Функция запуска HTTP сервера в фоне
def run_http_server():
    """Запуск HTTP сервера в фоновом потоке"""
    port = int(os.environ.get("PORT", 8000))
    print(f"🌐 Запуск HTTP сервера на порту {port}")
    
    try:
        server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
        print(f"✅ HTTP сервер запущен на 0.0.0.0:{port}")
        server.serve_forever()
    except Exception as e:
        print(f"❌ Ошибка запуска HTTP сервера: {e}")

# Главная функция
async def main():
    print("=== ЗАПУСК СИСТЕМЫ ===")
    
    try:
        # Проверяем подключение к базе данных
        if not check_database_connection():
            print("❌ Не удалось подключиться к базе данных")
            return
        
        # Создаем таблицы
        create_tables()
        print("✅ Таблицы созданы")
        
        # Регистрируем роутеры
        dp.include_router(router)
        
        # Запускаем HTTP сервер в фоновом потоке
        http_thread = threading.Thread(target=run_http_server, daemon=True)
        http_thread.start()
        print("✅ HTTP сервер запущен в фоне")
        
        # Ждем немного
        await asyncio.sleep(3)
        
        # Запускаем бота в основном потоке
        print("🤖 Запуск Telegram бота...")
        await dp.start_polling(bot)
        
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 