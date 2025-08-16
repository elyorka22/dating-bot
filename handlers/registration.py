import json
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import User, SearchSettings
from keyboards.inline import get_gender_keyboard, get_age_keyboard, get_height_keyboard, get_weight_keyboard, get_marital_status_keyboard, get_interests_keyboard, get_main_menu_keyboard
from keyboards.language import get_language_keyboard
from locales.translations import get_text
from utils.validators import validate_age, validate_height, validate_weight, validate_gender, validate_marital_status, validate_interests, validate_bio, sanitize_text
from utils.rate_limiter import spam_protection
from utils.logger import log_user_action, log_error
from config import MIN_AGE, MAX_AGE, MIN_HEIGHT, MAX_HEIGHT, MIN_WEIGHT, MAX_WEIGHT, MARITAL_STATUSES, INTERESTS

router = Router()

class RegistrationStates(StatesGroup):
    waiting_for_language = State()
    waiting_for_gender = State()
    waiting_for_age = State()
    waiting_for_height = State()
    waiting_for_weight = State()
    waiting_for_marital_status = State()
    waiting_for_interests = State()
    waiting_for_bio = State()

def get_user_language(telegram_id: int, db: Session) -> str:
    """Получить язык пользователя"""
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    return user.language if user else 'ru'

@router.message(Command("start"))
async def start_registration(message: Message, state: FSMContext):
    """Начало регистрации"""
    # Проверяем защиту от спама
    spam_check = spam_protection.check_action_spam(message.from_user.id, 'message')
    if spam_check['is_spam']:
        await message.answer("⚠️ Слишком много запросов. Попробуйте позже.")
        return
    
    db = next(get_db())
    
    try:
        # Проверяем, есть ли уже пользователь
        existing_user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
        if existing_user:
            lang = existing_user.language
            await message.answer(
                get_text('welcome', lang),
                reply_markup=get_main_menu_keyboard(lang)
            )
            log_user_action(message.bot.logger, message.from_user.id, "start_command", "existing_user")
            return

        # Если новый пользователь, сначала выбираем язык
        await message.answer(
            get_text('choose_language'),
            reply_markup=get_language_keyboard()
        )
        await state.set_state(RegistrationStates.waiting_for_language)
        log_user_action(message.bot.logger, message.from_user.id, "start_command", "new_user")
        
    except Exception as e:
        log_error(message.bot.logger, e, "start_registration")
        await message.answer("❌ Произошла ошибка. Попробуйте еще раз.")
    finally:
        db.close()

@router.callback_query(F.data.startswith("language:"))
async def handle_language_selection(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора языка"""
    # Проверяем защиту от спама
    spam_check = spam_protection.check_action_spam(callback.from_user.id, 'message')
    if spam_check['is_spam']:
        await callback.answer("⚠️ Слишком много запросов. Попробуйте позже.", show_alert=True)
        return
    
    lang = callback.data.split(":")[1]
    db = next(get_db())
    
    try:
        # Проверяем, есть ли уже пользователь
        existing_user = db.query(User).filter(User.telegram_id == callback.from_user.id).first()
        if existing_user:
            # Обновляем язык существующего пользователя
            existing_user.language = lang
            db.commit()
            
            await callback.message.edit_text(
                get_text('language_changed', lang),
                reply_markup=get_main_menu_keyboard(lang)
            )
            log_user_action(callback.bot.logger, callback.from_user.id, "language_changed", f"lang={lang}")
            await state.clear()
            return

        # Сохраняем выбранный язык
        await state.update_data(language=lang)
        
        # Переходим к выбору пола
        await callback.message.edit_text(
            get_text('registration_gender', lang),
            reply_markup=get_gender_keyboard(lang)
        )
        await state.set_state(RegistrationStates.waiting_for_gender)
        log_user_action(callback.bot.logger, callback.from_user.id, "language_selected", f"lang={lang}")
        
    except Exception as e:
        log_error(callback.bot.logger, e, "handle_language_selection")
        await callback.answer("❌ Произошла ошибка. Попробуйте еще раз.", show_alert=True)
    finally:
        db.close()

@router.callback_query(F.data.startswith("gender:"))
async def handle_gender_selection(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора пола"""
    # Проверяем защиту от спама
    spam_check = spam_protection.check_action_spam(callback.from_user.id, 'message')
    if spam_check['is_spam']:
        await callback.answer("⚠️ Слишком много запросов. Попробуйте позже.", show_alert=True)
        return
    
    gender = callback.data.split(":")[1]
    
    # Валидируем пол
    is_valid, error_msg = validate_gender(gender)
    if not is_valid:
        spam_protection.record_error(callback.from_user.id, 'invalid_inputs')
        await callback.answer(f"❌ {error_msg}", show_alert=True)
        return
    
    data = await state.get_data()
    lang = data.get('language', 'ru')
    
    await state.update_data(gender=gender)
    
    await callback.message.edit_text(
        get_text('registration_age', lang),
        reply_markup=get_age_keyboard(lang)
    )
    await state.set_state(RegistrationStates.waiting_for_age)
    log_user_action(callback.bot.logger, callback.from_user.id, "gender_selected", f"gender={gender}")

@router.callback_query(F.data.startswith("age:"))
async def handle_age_selection(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора возраста"""
    # Проверяем защиту от спама
    spam_check = spam_protection.check_action_spam(callback.from_user.id, 'message')
    if spam_check['is_spam']:
        await callback.answer("⚠️ Слишком много запросов. Попробуйте позже.", show_alert=True)
        return
    
    age_str = callback.data.split(":")[1]
    
    # Валидируем возраст
    is_valid, age_value, error_msg = validate_age(age_str)
    if not is_valid:
        spam_protection.record_error(callback.from_user.id, 'invalid_inputs')
        await callback.answer(f"❌ {error_msg}", show_alert=True)
        return
    
    data = await state.get_data()
    lang = data.get('language', 'ru')
    
    await state.update_data(age=age_value)
    
    await callback.message.edit_text(
        get_text('registration_height', lang),
        reply_markup=get_height_keyboard(lang)
    )
    await state.set_state(RegistrationStates.waiting_for_height)
    log_user_action(callback.bot.logger, callback.from_user.id, "age_selected", f"age={age_value}")

@router.callback_query(F.data.startswith("height:"))
async def handle_height_selection(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора роста"""
    # Проверяем защиту от спама
    spam_check = spam_protection.check_action_spam(callback.from_user.id, 'message')
    if spam_check['is_spam']:
        await callback.answer("⚠️ Слишком много запросов. Попробуйте позже.", show_alert=True)
        return
    
    height_str = callback.data.split(":")[1]
    
    # Валидируем рост
    is_valid, height_value, error_msg = validate_height(height_str)
    if not is_valid:
        spam_protection.record_error(callback.from_user.id, 'invalid_inputs')
        await callback.answer(f"❌ {error_msg}", show_alert=True)
        return
    
    data = await state.get_data()
    lang = data.get('language', 'ru')
    
    await state.update_data(height=height_value)
    
    await callback.message.edit_text(
        get_text('registration_weight', lang),
        reply_markup=get_weight_keyboard(lang)
    )
    await state.set_state(RegistrationStates.waiting_for_weight)
    log_user_action(callback.bot.logger, callback.from_user.id, "height_selected", f"height={height_value}")

@router.callback_query(F.data.startswith("weight:"))
async def handle_weight_selection(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора веса"""
    # Проверяем защиту от спама
    spam_check = spam_protection.check_action_spam(callback.from_user.id, 'message')
    if spam_check['is_spam']:
        await callback.answer("⚠️ Слишком много запросов. Попробуйте позже.", show_alert=True)
        return
    
    weight_str = callback.data.split(":")[1]
    
    # Валидируем вес
    is_valid, weight_value, error_msg = validate_weight(weight_str)
    if not is_valid:
        spam_protection.record_error(callback.from_user.id, 'invalid_inputs')
        await callback.answer(f"❌ {error_msg}", show_alert=True)
        return
    
    data = await state.get_data()
    lang = data.get('language', 'ru')
    
    await state.update_data(weight=weight_value)
    
    await callback.message.edit_text(
        get_text('registration_marital', lang),
        reply_markup=get_marital_status_keyboard(lang)
    )
    await state.set_state(RegistrationStates.waiting_for_marital_status)
    log_user_action(callback.bot.logger, callback.from_user.id, "weight_selected", f"weight={weight_value}")

@router.callback_query(F.data.startswith("marital:"))
async def handle_marital_selection(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора семейного положения"""
    # Проверяем защиту от спама
    spam_check = spam_protection.check_action_spam(callback.from_user.id, 'message')
    if spam_check['is_spam']:
        await callback.answer("⚠️ Слишком много запросов. Попробуйте позже.", show_alert=True)
        return
    
    marital_status = callback.data.split(":")[1]
    
    # Валидируем семейное положение
    is_valid, error_msg = validate_marital_status(marital_status)
    if not is_valid:
        spam_protection.record_error(callback.from_user.id, 'invalid_inputs')
        await callback.answer(f"❌ {error_msg}", show_alert=True)
        return
    
    data = await state.get_data()
    lang = data.get('language', 'ru')
    
    await state.update_data(marital_status=marital_status)
    
    await callback.message.edit_text(
        get_text('registration_interests', lang),
        reply_markup=get_interests_keyboard(lang)
    )
    await state.set_state(RegistrationStates.waiting_for_interests)
    log_user_action(callback.bot.logger, callback.from_user.id, "marital_selected", f"marital={marital_status}")

@router.callback_query(F.data.startswith("interest:"))
async def handle_interest_selection(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора интересов"""
    # Проверяем защиту от спама
    spam_check = spam_protection.check_action_spam(callback.from_user.id, 'message')
    if spam_check['is_spam']:
        await callback.answer("⚠️ Слишком много запросов. Попробуйте позже.", show_alert=True)
        return
    
    interest = callback.data.split(":")[1]
    data = await state.get_data()
    lang = data.get('language', 'ru')
    
    # Получаем текущие выбранные интересы
    selected_interests = data.get('interests', [])
    
    if interest in selected_interests:
        selected_interests.remove(interest)
    else:
        selected_interests.append(interest)
    
    await state.update_data(interests=selected_interests)
    
    interests_text = ", ".join(selected_interests) if selected_interests else get_text('btn_none', lang)
    
    await callback.message.edit_text(
        f"{get_text('registration_interests_selected', lang, interests=interests_text)}\n\n"
        f"{get_text('registration_interests_continue', lang)}",
        reply_markup=get_interests_keyboard(lang, selected_interests)
    )

@router.callback_query(F.data == "interests_done")
async def handle_interests_done(callback: CallbackQuery, state: FSMContext):
    """Завершение выбора интересов"""
    # Проверяем защиту от спама
    spam_check = spam_protection.check_action_spam(callback.from_user.id, 'message')
    if spam_check['is_spam']:
        await callback.answer("⚠️ Слишком много запросов. Попробуйте позже.", show_alert=True)
        return
    
    data = await state.get_data()
    lang = data.get('language', 'ru')
    selected_interests = data.get('interests', [])
    
    # Валидируем интересы
    is_valid, error_msg = validate_interests(selected_interests)
    if not is_valid:
        spam_protection.record_error(callback.from_user.id, 'invalid_inputs')
        await callback.answer(f"❌ {error_msg}", show_alert=True)
        return
    
    await callback.message.edit_text(
        get_text('registration_bio', lang)
    )
    await state.set_state(RegistrationStates.waiting_for_bio)
    log_user_action(callback.bot.logger, callback.from_user.id, "interests_selected", f"interests={selected_interests}")

@router.message(RegistrationStates.waiting_for_bio)
async def handle_bio_input(message: Message, state: FSMContext):
    """Обработка ввода описания о себе"""
    # Проверяем защиту от спама
    spam_check = spam_protection.check_message_spam(message.from_user.id, message.text)
    if spam_check['is_spam']:
        if spam_check['action'] == 'block':
            await message.answer("⚠️ Сообщение заблокировано из-за подозрительного содержимого.")
            return
        elif spam_check['action'] == 'warn':
            await message.answer("⚠️ Внимание: сообщение содержит подозрительное содержимое.")
    
    # Санитизируем и валидируем описание
    sanitized_bio = sanitize_text(message.text)
    is_valid, error_msg = validate_bio(sanitized_bio)
    
    if not is_valid:
        spam_protection.record_error(message.from_user.id, 'invalid_inputs')
        await message.answer(f"❌ {error_msg}")
        return
    
    # Сохраняем описание
    await state.update_data(bio=sanitized_bio)
    
    # Завершаем регистрацию
    await complete_registration(message, state)

async def complete_registration(message: Message, state: FSMContext):
    """Завершение регистрации"""
    data = await state.get_data()
    lang = data.get('language', 'ru')
    
    db = next(get_db())
    
    try:
        # Создаем пользователя
        user = User(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            gender=data['gender'],
            age=data['age'],
            height=data['height'],
            weight=data['weight'],
            marital_status=data['marital_status'],
            interests=json.dumps(data.get('interests', []), ensure_ascii=False),
            bio=data.get('bio'),
            language=lang
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Создаем настройки поиска по умолчанию
        search_settings = SearchSettings(
            user_id=user.id,
            gender_preference="Все",
            min_age=MIN_AGE,
            max_age=MAX_AGE,
            min_height=MIN_HEIGHT,
            max_height=MAX_HEIGHT,
            min_weight=MIN_WEIGHT,
            max_weight=MAX_WEIGHT,
            marital_status_preference=json.dumps(MARITAL_STATUSES, ensure_ascii=False)
        )
        
        db.add(search_settings)
        db.commit()
        
        # Сбрасываем лимиты для нового пользователя
        spam_protection.rate_limiter.reset_user_limits(message.from_user.id)
        
        await message.answer(
            get_text('registration_complete', lang),
            reply_markup=get_main_menu_keyboard(lang)
        )
        
        log_user_action(message.bot.logger, message.from_user.id, "registration_complete", f"user_id={user.id}")
        await state.clear()
        
    except Exception as e:
        log_error(message.bot.logger, e, "complete_registration")
        await message.answer("❌ Произошла ошибка при регистрации. Попробуйте еще раз.")
    finally:
        db.close() 