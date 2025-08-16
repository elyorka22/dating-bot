import json
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import User
from keyboards.inline import get_main_menu_keyboard
from keyboards.profile import get_profile_edit_keyboard, get_interests_edit_keyboard
from locales.translations import get_text
from config import MIN_AGE, MAX_AGE, MIN_HEIGHT, MAX_HEIGHT, MIN_WEIGHT, MAX_WEIGHT, MARITAL_STATUSES, INTERESTS

router = Router()

class ProfileEditStates(StatesGroup):
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

@router.callback_query(F.data == "edit_profile")
async def show_profile_edit_menu(callback: CallbackQuery):
    """Показать меню редактирования профиля"""
    db = next(get_db())
    
    try:
        # Получаем язык пользователя
        lang = get_user_language(callback.from_user.id, db)
        
        # Получаем пользователя
        user = db.query(User).filter(User.telegram_id == callback.from_user.id).first()
        if not user:
            await callback.message.edit_text(
                get_text('error_not_registered', lang),
                reply_markup=get_main_menu_keyboard(lang)
            )
            return
        
        # Формируем текст профиля
        profile_text = f"{get_text('profile_title', lang)}\n\n"
        profile_text += f"{get_text('profile_gender', lang, gender=user.gender)}\n"
        profile_text += f"{get_text('profile_age', lang, age=user.age)}\n"
        profile_text += f"{get_text('profile_height', lang, height=user.height)}\n"
        profile_text += f"{get_text('profile_weight', lang, weight=user.weight)}\n"
        profile_text += f"{get_text('profile_marital', lang, status=user.marital_status)}\n"
        
        if user.interests:
            try:
                interests = json.loads(user.interests)
                if interests:
                    profile_text += f"{get_text('profile_interests', lang, interests=', '.join(interests))}\n"
            except:
                pass
        
        if user.bio:
            profile_text += f"\n{get_text('profile_bio', lang, bio=user.bio)}\n"
        
        profile_text += f"\n{get_text('settings_change_age', lang)}"
        
        await callback.message.edit_text(
            profile_text,
            reply_markup=get_profile_edit_keyboard(lang)
        )
        
    except Exception as e:
        lang = get_user_language(callback.from_user.id, db)
        await callback.message.edit_text(
            get_text('error_occurred', lang),
            reply_markup=get_main_menu_keyboard(lang)
        )
        print(f"Profile edit error: {e}")
    finally:
        db.close()

@router.callback_query(F.data == "edit_age")
async def edit_age(callback: CallbackQuery, state: FSMContext):
    """Редактирование возраста"""
    db = next(get_db())
    lang = get_user_language(callback.from_user.id, db)
    db.close()
    
    await callback.message.edit_text(
        get_text('registration_age', lang)
    )
    await state.set_state(ProfileEditStates.waiting_for_age)

@router.message(ProfileEditStates.waiting_for_age)
async def handle_age_edit(message: Message, state: FSMContext):
    """Обработка редактирования возраста"""
    try:
        age = int(message.text)
        if MIN_AGE <= age <= MAX_AGE:
            # Обновляем возраст в базе данных
            db = next(get_db())
            try:
                lang = get_user_language(message.from_user.id, db)
                user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
                user.age = age
                db.commit()
                
                await message.answer(
                    f"✅ {get_text('profile_age', lang, age=age)}\n\n"
                    f"{get_text('btn_save', lang)}!",
                    reply_markup=get_main_menu_keyboard(lang)
                )
                await state.clear()
                
            except Exception as e:
                await message.answer(get_text('error_occurred', lang))
                print(f"Age edit error: {e}")
            finally:
                db.close()
        else:
            db = next(get_db())
            lang = get_user_language(message.from_user.id, db)
            db.close()
            await message.answer(get_text('error_invalid_age', lang))
    except ValueError:
        db = next(get_db())
        lang = get_user_language(message.from_user.id, db)
        db.close()
        await message.answer(get_text('error_invalid_age', lang))

@router.callback_query(F.data == "edit_height")
async def edit_height(callback: CallbackQuery, state: FSMContext):
    """Редактирование роста"""
    await callback.message.edit_text(
        f"📏 Укажите ваш рост в см (от {MIN_HEIGHT} до {MAX_HEIGHT}):"
    )
    await state.set_state(ProfileEditStates.waiting_for_height)

@router.message(ProfileEditStates.waiting_for_height)
async def handle_height_edit(message: Message, state: FSMContext):
    """Обработка редактирования роста"""
    try:
        height = int(message.text)
        if MIN_HEIGHT <= height <= MAX_HEIGHT:
            # Обновляем рост в базе данных
            db = next(get_db())
            try:
                user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
                user.height = height
                db.commit()
                
                await message.answer(
                    f"✅ Рост обновлен: {height} см\n\n"
                    "Профиль сохранен!",
                    reply_markup=get_main_menu_keyboard()
                )
                await state.clear()
                
            except Exception as e:
                await message.answer("❌ Ошибка при сохранении профиля")
                print(f"Height edit error: {e}")
            finally:
                db.close()
        else:
            await message.answer(f"Рост должен быть от {MIN_HEIGHT} до {MAX_HEIGHT} см. Попробуйте еще раз:")
    except ValueError:
        await message.answer("Пожалуйста, введите число. Попробуйте еще раз:")

@router.callback_query(F.data == "edit_weight")
async def edit_weight(callback: CallbackQuery, state: FSMContext):
    """Редактирование веса"""
    await callback.message.edit_text(
        f"⚖️ Укажите ваш вес в кг (от {MIN_WEIGHT} до {MAX_WEIGHT}):"
    )
    await state.set_state(ProfileEditStates.waiting_for_weight)

@router.message(ProfileEditStates.waiting_for_weight)
async def handle_weight_edit(message: Message, state: FSMContext):
    """Обработка редактирования веса"""
    try:
        weight = int(message.text)
        if MIN_WEIGHT <= weight <= MAX_WEIGHT:
            # Обновляем вес в базе данных
            db = next(get_db())
            try:
                user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
                user.weight = weight
                db.commit()
                
                await message.answer(
                    f"✅ Вес обновлен: {weight} кг\n\n"
                    "Профиль сохранен!",
                    reply_markup=get_main_menu_keyboard()
                )
                await state.clear()
                
            except Exception as e:
                await message.answer("❌ Ошибка при сохранении профиля")
                print(f"Weight edit error: {e}")
            finally:
                db.close()
        else:
            await message.answer(f"Вес должен быть от {MIN_WEIGHT} до {MAX_WEIGHT} кг. Попробуйте еще раз:")
    except ValueError:
        await message.answer("Пожалуйста, введите число. Попробуйте еще раз:")

@router.callback_query(F.data == "edit_marital")
async def edit_marital(callback: CallbackQuery, state: FSMContext):
    """Редактирование семейного положения"""
    from keyboards.inline import get_marital_status_keyboard
    
    await callback.message.edit_text(
        "💍 Выберите ваше семейное положение:",
        reply_markup=get_marital_status_keyboard()
    )
    await state.set_state(ProfileEditStates.waiting_for_marital_status)

@router.callback_query(F.data.startswith("marital:"))
async def handle_marital_edit(callback: CallbackQuery, state: FSMContext):
    """Обработка редактирования семейного положения"""
    marital_status = callback.data.split(":")[1]
    db = next(get_db())
    
    try:
        # Получаем пользователя
        user = db.query(User).filter(User.telegram_id == callback.from_user.id).first()
        
        # Обновляем семейное положение
        user.marital_status = marital_status
        db.commit()
        
        await callback.answer("✅ Семейное положение обновлено!", show_alert=True)
        
        # Возвращаемся в меню редактирования профиля
        await show_profile_edit_menu(callback)
        
    except Exception as e:
        await callback.answer("❌ Ошибка при обновлении профиля", show_alert=True)
        print(f"Marital edit error: {e}")
    finally:
        db.close()

@router.callback_query(F.data == "edit_interests")
async def edit_interests(callback: CallbackQuery, state: FSMContext):
    """Редактирование интересов"""
    db = next(get_db())
    
    try:
        user = db.query(User).filter(User.telegram_id == callback.from_user.id).first()
        current_interests = []
        
        if user.interests:
            try:
                current_interests = json.loads(user.interests)
            except:
                pass
        
        await callback.message.edit_text(
            f"🎯 Выберите ваши интересы (текущие: {', '.join(current_interests) if current_interests else 'не выбрано'}):",
            reply_markup=get_interests_edit_keyboard(current_interests)
        )
        await state.set_state(ProfileEditStates.waiting_for_interests)
        
    except Exception as e:
        await callback.answer("❌ Ошибка при загрузке интересов", show_alert=True)
        print(f"Interests edit error: {e}")
    finally:
        db.close()

@router.callback_query(F.data.startswith("interest_edit:"))
async def handle_interest_edit(callback: CallbackQuery, state: FSMContext):
    """Обработка редактирования интересов"""
    interest = callback.data.split(":")[1]
    data = await state.get_data()
    selected_interests = data.get("interests", [])
    
    if interest in selected_interests:
        selected_interests.remove(interest)
    else:
        selected_interests.append(interest)
    
    await state.update_data(interests=selected_interests)
    
    interests_text = ", ".join(selected_interests) if selected_interests else "не выбрано"
    await callback.message.edit_text(
        f"🎯 Выбранные интересы: {interests_text}\n\n"
        f"Выберите интересы (можно выбрать несколько):",
        reply_markup=get_interests_edit_keyboard(selected_interests)
    )

@router.callback_query(F.data == "interests_save")
async def save_interests(callback: CallbackQuery, state: FSMContext):
    """Сохранение интересов"""
    data = await state.get_data()
    selected_interests = data.get("interests", [])
    
    db = next(get_db())
    
    try:
        user = db.query(User).filter(User.telegram_id == callback.from_user.id).first()
        user.interests = json.dumps(selected_interests, ensure_ascii=False)
        db.commit()
        
        interests_text = ", ".join(selected_interests) if selected_interests else "не выбрано"
        await callback.answer(f"✅ Интересы обновлены: {interests_text}", show_alert=True)
        
        # Возвращаемся в меню редактирования профиля
        await show_profile_edit_menu(callback)
        await state.clear()
        
    except Exception as e:
        await callback.answer("❌ Ошибка при сохранении интересов", show_alert=True)
        print(f"Save interests error: {e}")
    finally:
        db.close()

@router.callback_query(F.data == "edit_bio")
async def edit_bio(callback: CallbackQuery, state: FSMContext):
    """Редактирование описания о себе"""
    await callback.message.edit_text(
        "💬 Напишите немного о себе (или отправьте '-' чтобы удалить описание):"
    )
    await state.set_state(ProfileEditStates.waiting_for_bio)

@router.message(ProfileEditStates.waiting_for_bio)
async def handle_bio_edit(message: Message, state: FSMContext):
    """Обработка редактирования описания о себе"""
    bio = message.text if message.text != "-" else None
    
    # Обновляем описание в базе данных
    db = next(get_db())
    try:
        user = db.query(User).filter(User.telegram_id == message.from_user.id).first()
        user.bio = bio
        db.commit()
        
        if bio:
            await message.answer(
                f"✅ Описание обновлено!\n\n"
                f"О себе:\n{bio}\n\n"
                "Профиль сохранен!",
                reply_markup=get_main_menu_keyboard()
            )
        else:
            await message.answer(
                "✅ Описание удалено!\n\n"
                "Профиль сохранен!",
                reply_markup=get_main_menu_keyboard()
            )
        await state.clear()
        
    except Exception as e:
        await message.answer("❌ Ошибка при сохранении профиля")
        print(f"Bio edit error: {e}")
    finally:
        db.close() 