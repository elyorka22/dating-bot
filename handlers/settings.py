import json
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import User, SearchSettings
from keyboards.inline import get_main_menu_keyboard
from keyboards.settings import (
    get_gender_preference_keyboard, get_age_range_keyboard,
    get_height_range_keyboard, get_weight_range_keyboard,
    get_marital_preference_keyboard, get_settings_menu_keyboard
)
from locales.translations import get_text
from config import MIN_AGE, MAX_AGE, MIN_HEIGHT, MAX_HEIGHT, MIN_WEIGHT, MAX_WEIGHT, MARITAL_STATUSES

router = Router()

class SettingsStates(StatesGroup):
    waiting_for_gender_preference = State()
    waiting_for_min_age = State()
    waiting_for_max_age = State()
    waiting_for_min_height = State()
    waiting_for_max_height = State()
    waiting_for_min_weight = State()
    waiting_for_max_weight = State()
    waiting_for_marital_preference = State()

def get_user_language(telegram_id: int, db: Session) -> str:
    """Получить язык пользователя"""
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    return user.language if user else 'ru'

@router.callback_query(F.data == "search_settings")
async def show_settings_menu(callback: CallbackQuery):
    """Показать меню настроек поиска"""
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
        
        # Получаем текущие настройки
        search_settings = db.query(SearchSettings).filter(SearchSettings.user_id == current_user.id).first()
        if not search_settings:
            await callback.message.edit_text(
                get_text('error_not_registered', lang),
                reply_markup=get_main_menu_keyboard(lang)
            )
            return
        
        # Формируем текст с текущими настройками
        settings_text = f"{get_text('settings_title', lang)}\n\n"
        settings_text += f"{get_text('settings_gender', lang, preference=search_settings.gender_preference)}\n"
        settings_text += f"{get_text('settings_age', lang, min=search_settings.min_age, max=search_settings.max_age)}\n"
        settings_text += f"{get_text('settings_height', lang, min=search_settings.min_height, max=search_settings.max_height)}\n"
        settings_text += f"{get_text('settings_weight', lang, min=search_settings.min_weight, max=search_settings.max_weight)}\n"
        
        if search_settings.marital_status_preference:
            try:
                marital_prefs = json.loads(search_settings.marital_status_preference)
                settings_text += f"{get_text('settings_marital', lang, preference=', '.join(marital_prefs))}\n"
            except:
                settings_text += f"{get_text('settings_marital', lang, preference=get_text('btn_all', lang))}\n"
        
        settings_text += f"\n{get_text('settings_change_gender', lang)}"
        
        await callback.message.edit_text(
            settings_text,
            reply_markup=get_settings_menu_keyboard(lang)
        )
        
    except Exception as e:
        lang = get_user_language(callback.from_user.id, db)
        await callback.message.edit_text(
            get_text('error_occurred', lang),
            reply_markup=get_main_menu_keyboard(lang)
        )
        print(f"Settings error: {e}")
    finally:
        db.close()

@router.callback_query(F.data == "change_gender_preference")
async def change_gender_preference(callback: CallbackQuery, state: FSMContext):
    """Изменить предпочтения по полу"""
    db = next(get_db())
    lang = get_user_language(callback.from_user.id, db)
    db.close()
    
    await callback.message.edit_text(
        get_text('settings_change_gender', lang),
        reply_markup=get_gender_preference_keyboard(lang)
    )
    await state.set_state(SettingsStates.waiting_for_gender_preference)

@router.callback_query(F.data.startswith("gender_pref:"))
async def handle_gender_preference(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора предпочтений по полу"""
    gender_pref = callback.data.split(":")[1]
    db = next(get_db())
    
    try:
        # Получаем язык пользователя
        lang = get_user_language(callback.from_user.id, db)
        
        # Получаем пользователя
        current_user = db.query(User).filter(User.telegram_id == callback.from_user.id).first()
        if not current_user:
            await callback.message.edit_text(
                get_text('error_not_registered', lang),
                reply_markup=get_main_menu_keyboard(lang)
            )
            return
        
        # Обновляем настройки
        search_settings = db.query(SearchSettings).filter(SearchSettings.user_id == current_user.id).first()
        if search_settings:
            search_settings.gender_preference = gender_pref
            db.commit()
            
            await callback.answer(f"✅ {get_text('settings_gender', lang, preference=gender_pref)}", show_alert=True)
        else:
            await callback.answer(get_text('error_occurred', lang), show_alert=True)
            return
        
        # Возвращаемся в меню настроек
        await show_settings_menu(callback)
        
    except Exception as e:
        lang = get_user_language(callback.from_user.id, db)
        await callback.answer(get_text('error_occurred', lang), show_alert=True)
        print(f"Gender preference error: {e}")
    finally:
        db.close()

@router.callback_query(F.data == "change_age_range")
async def change_age_range(callback: CallbackQuery, state: FSMContext):
    """Изменить диапазон возраста"""
    await callback.message.edit_text(
        f"📅 Укажите минимальный возраст (от {MIN_AGE} до {MAX_AGE} лет):"
    )
    await state.set_state(SettingsStates.waiting_for_min_age)

@router.message(SettingsStates.waiting_for_min_age)
async def handle_min_age_input(message: Message, state: FSMContext):
    """Обработка ввода минимального возраста"""
    try:
        min_age = int(message.text)
        if MIN_AGE <= min_age <= MAX_AGE:
            await state.update_data(min_age=min_age)
            await message.answer(
                f"✅ Минимальный возраст: {min_age} лет\n\n"
                f"Теперь укажите максимальный возраст (от {min_age} до {MAX_AGE} лет):"
            )
            await state.set_state(SettingsStates.waiting_for_max_age)
        else:
            await message.answer(f"Возраст должен быть от {MIN_AGE} до {MAX_AGE} лет. Попробуйте еще раз:")
    except ValueError:
        await message.answer("Пожалуйста, введите число. Попробуйте еще раз:")

@router.message(SettingsStates.waiting_for_max_age)
async def handle_max_age_input(message: Message, state: FSMContext):
    """Обработка ввода максимального возраста"""
    try:
        max_age = int(message.text)
        data = await state.get_data()
        min_age = data.get("min_age", MIN_AGE)
        
        if min_age <= max_age <= MAX_AGE:
            # Сохраняем настройки
            db = next(get_db())
            try:
                current_user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
                search_settings = db.query(SearchSettings).filter(SearchSettings.user_id == current_user.id).first()
                
                search_settings.min_age = min_age
                search_settings.max_age = max_age
                db.commit()
                
                await message.answer(
                    f"✅ Диапазон возраста обновлен: {min_age}-{max_age} лет\n\n"
                    "Настройки сохранены!",
                    reply_markup=get_main_menu_keyboard()
                )
                await state.clear()
                
            except Exception as e:
                await message.answer("❌ Ошибка при сохранении настроек")
                print(f"Age settings error: {e}")
            finally:
                db.close()
        else:
            await message.answer(f"Максимальный возраст должен быть от {min_age} до {MAX_AGE} лет. Попробуйте еще раз:")
    except ValueError:
        await message.answer("Пожалуйста, введите число. Попробуйте еще раз:")

@router.callback_query(F.data == "change_height_range")
async def change_height_range(callback: CallbackQuery, state: FSMContext):
    """Изменить диапазон роста"""
    await callback.message.edit_text(
        f"📏 Укажите минимальный рост (от {MIN_HEIGHT} до {MAX_HEIGHT} см):"
    )
    await state.set_state(SettingsStates.waiting_for_min_height)

@router.message(SettingsStates.waiting_for_min_height)
async def handle_min_height_input(message: Message, state: FSMContext):
    """Обработка ввода минимального роста"""
    try:
        min_height = int(message.text)
        if MIN_HEIGHT <= min_height <= MAX_HEIGHT:
            await state.update_data(min_height=min_height)
            await message.answer(
                f"✅ Минимальный рост: {min_height} см\n\n"
                f"Теперь укажите максимальный рост (от {min_height} до {MAX_HEIGHT} см):"
            )
            await state.set_state(SettingsStates.waiting_for_max_height)
        else:
            await message.answer(f"Рост должен быть от {MIN_HEIGHT} до {MAX_HEIGHT} см. Попробуйте еще раз:")
    except ValueError:
        await message.answer("Пожалуйста, введите число. Попробуйте еще раз:")

@router.message(SettingsStates.waiting_for_max_height)
async def handle_max_height_input(message: Message, state: FSMContext):
    """Обработка ввода максимального роста"""
    try:
        max_height = int(message.text)
        data = await state.get_data()
        min_height = data.get("min_height", MIN_HEIGHT)
        
        if min_height <= max_height <= MAX_HEIGHT:
            # Сохраняем настройки
            db = next(get_db())
            try:
                current_user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
                search_settings = db.query(SearchSettings).filter(SearchSettings.user_id == current_user.id).first()
                
                search_settings.min_height = min_height
                search_settings.max_height = max_height
                db.commit()
                
                await message.answer(
                    f"✅ Диапазон роста обновлен: {min_height}-{max_height} см\n\n"
                    "Настройки сохранены!",
                    reply_markup=get_main_menu_keyboard()
                )
                await state.clear()
                
            except Exception as e:
                await message.answer("❌ Ошибка при сохранении настроек")
                print(f"Height settings error: {e}")
            finally:
                db.close()
        else:
            await message.answer(f"Максимальный рост должен быть от {min_height} до {MAX_HEIGHT} см. Попробуйте еще раз:")
    except ValueError:
        await message.answer("Пожалуйста, введите число. Попробуйте еще раз:")

@router.callback_query(F.data == "change_weight_range")
async def change_weight_range(callback: CallbackQuery, state: FSMContext):
    """Изменить диапазон веса"""
    await callback.message.edit_text(
        f"⚖️ Укажите минимальный вес (от {MIN_WEIGHT} до {MAX_WEIGHT} кг):"
    )
    await state.set_state(SettingsStates.waiting_for_min_weight)

@router.message(SettingsStates.waiting_for_min_weight)
async def handle_min_weight_input(message: Message, state: FSMContext):
    """Обработка ввода минимального веса"""
    try:
        min_weight = int(message.text)
        if MIN_WEIGHT <= min_weight <= MAX_WEIGHT:
            await state.update_data(min_weight=min_weight)
            await message.answer(
                f"✅ Минимальный вес: {min_weight} кг\n\n"
                f"Теперь укажите максимальный вес (от {min_weight} до {MAX_WEIGHT} кг):"
            )
            await state.set_state(SettingsStates.waiting_for_max_weight)
        else:
            await message.answer(f"Вес должен быть от {MIN_WEIGHT} до {MAX_WEIGHT} кг. Попробуйте еще раз:")
    except ValueError:
        await message.answer("Пожалуйста, введите число. Попробуйте еще раз:")

@router.message(SettingsStates.waiting_for_max_weight)
async def handle_max_weight_input(message: Message, state: FSMContext):
    """Обработка ввода максимального веса"""
    try:
        max_weight = int(message.text)
        data = await state.get_data()
        min_weight = data.get("min_weight", MIN_WEIGHT)
        
        if min_weight <= max_weight <= MAX_WEIGHT:
            # Сохраняем настройки
            db = next(get_db())
            try:
                current_user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
                search_settings = db.query(SearchSettings).filter(SearchSettings.user_id == current_user.id).first()
                
                search_settings.min_weight = min_weight
                search_settings.max_weight = max_weight
                db.commit()
                
                await message.answer(
                    f"✅ Диапазон веса обновлен: {min_weight}-{max_weight} кг\n\n"
                    "Настройки сохранены!",
                    reply_markup=get_main_menu_keyboard()
                )
                await state.clear()
                
            except Exception as e:
                await message.answer("❌ Ошибка при сохранении настроек")
                print(f"Weight settings error: {e}")
            finally:
                db.close()
        else:
            await message.answer(f"Максимальный вес должен быть от {min_weight} до {MAX_WEIGHT} кг. Попробуйте еще раз:")
    except ValueError:
        await message.answer("Пожалуйста, введите число. Попробуйте еще раз:")

@router.callback_query(F.data == "change_marital_preference")
async def change_marital_preference(callback: CallbackQuery, state: FSMContext):
    """Изменить предпочтения по семейному положению"""
    await callback.message.edit_text(
        "💍 Выберите предпочтения по семейному положению:",
        reply_markup=get_marital_preference_keyboard()
    )
    await state.set_state(SettingsStates.waiting_for_marital_preference)

@router.callback_query(F.data.startswith("marital_pref:"))
async def handle_marital_preference(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора предпочтений по семейному положению"""
    marital_pref = callback.data.split(":")[1]
    db = next(get_db())
    
    try:
        # Получаем пользователя и настройки
        current_user = db.query(User).filter(User.telegram_id == callback.from_user.id).first()
        search_settings = db.query(SearchSettings).filter(SearchSettings.user_id == current_user.id).first()
        
        # Обновляем настройки
        if marital_pref == "all":
            search_settings.marital_status_preference = json.dumps(MARITAL_STATUSES, ensure_ascii=False)
        else:
            search_settings.marital_status_preference = json.dumps([marital_pref], ensure_ascii=False)
        
        db.commit()
        
        await callback.answer("✅ Предпочтения по семейному положению обновлены!", show_alert=True)
        
        # Возвращаемся в меню настроек
        await show_settings_menu(callback)
        
    except Exception as e:
        await callback.answer("❌ Ошибка при обновлении настроек", show_alert=True)
        print(f"Marital preference error: {e}")
    finally:
        db.close() 