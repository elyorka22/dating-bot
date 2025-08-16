from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup
from sqlalchemy.orm import Session
from sqlalchemy import and_

from database.database import get_db
from database.models import User, AccessRequest
from keyboards.inline import get_main_menu_keyboard

class NotificationService:
    def __init__(self, bot: Bot):
        self.bot = bot
    
    async def send_access_granted_notification(self, request_id: int):
        """Отправить уведомление о предоставлении доступа"""
        db = next(get_db())
        
        try:
            # Получаем запрос
            access_request = db.query(AccessRequest).filter(AccessRequest.id == request_id).first()
            if not access_request:
                return
            
            # Получаем пользователей
            from_user = db.query(User).filter(User.id == access_request.from_user_id).first()
            to_user = db.query(User).filter(User.id == access_request.to_user_id).first()
            
            if not from_user or not to_user:
                return
            
            # Формируем username для отправки
            if to_user.username:
                username_text = f"@{to_user.username}"
            else:
                username_text = "Пользователь не указал username"
            
            # Отправляем уведомление пользователю, который запрашивал доступ
            notification_text = f"🎉 Отличные новости!\n\n"
            notification_text += f"Пользователь {to_user.gender}, {to_user.age} лет согласился дать вам доступ в личку.\n\n"
            notification_text += f"Username: {username_text}\n\n"
            notification_text += f"Теперь вы можете начать общение!"
            
            await self.bot.send_message(
                chat_id=from_user.telegram_id,
                text=notification_text,
                reply_markup=get_main_menu_keyboard()
            )
            
        except Exception as e:
            print(f"Error sending access granted notification: {e}")
        finally:
            db.close()
    
    async def send_new_request_notification(self, request_id: int):
        """Отправить уведомление о новом запросе на доступ"""
        db = next(get_db())
        
        try:
            # Получаем запрос
            access_request = db.query(AccessRequest).filter(AccessRequest.id == request_id).first()
            if not access_request:
                return
            
            # Получаем пользователей
            from_user = db.query(User).filter(User.id == access_request.from_user_id).first()
            to_user = db.query(User).filter(User.id == access_request.to_user_id).first()
            
            if not from_user or not to_user:
                return
            
            # Отправляем уведомление пользователю, которому отправлен запрос
            notification_text = f"📨 Новый запрос на доступ!\n\n"
            notification_text += f"👤 {from_user.gender}, {from_user.age} лет\n"
            notification_text += f"📏 Рост: {from_user.height} см\n"
            notification_text += f"⚖️ Вес: {from_user.weight} кг\n"
            notification_text += f"💍 Статус: {from_user.marital_status}\n\n"
            
            if from_user.interests:
                try:
                    import json
                    interests = json.loads(from_user.interests)
                    if interests:
                        notification_text += f"🎯 Интересы: {', '.join(interests)}\n\n"
                except:
                    pass
            
            if from_user.bio:
                notification_text += f"💬 О себе:\n{from_user.bio}\n\n"
            
            notification_text += f"Хотите дать доступ к вашему username?"
            
            from keyboards.inline import get_access_request_keyboard
            keyboard = get_access_request_keyboard(request_id)
            
            await self.bot.send_message(
                chat_id=to_user.telegram_id,
                text=notification_text,
                reply_markup=keyboard
            )
            
        except Exception as e:
            print(f"Error sending new request notification: {e}")
        finally:
            db.close()
    
    async def send_daily_summary(self, user_id: int):
        """Отправить ежедневную сводку"""
        db = next(get_db())
        
        try:
            user = db.query(User).filter(User.telegram_id == user_id).first()
            if not user:
                return
            
            # Получаем статистику за день
            from datetime import datetime, timedelta
            today = datetime.utcnow().date()
            
            # Новые запросы
            new_requests = db.query(AccessRequest).filter(
                and_(
                    AccessRequest.to_user_id == user.id,
                    AccessRequest.status == "pending",
                    AccessRequest.created_at >= today
                )
            ).count()
            
            # Принятые запросы
            accepted_requests = db.query(AccessRequest).filter(
                and_(
                    AccessRequest.to_user_id == user.id,
                    AccessRequest.status == "accepted",
                    AccessRequest.created_at >= today
                )
            ).count()
            
            # Отправленные запросы
            sent_requests = db.query(AccessRequest).filter(
                and_(
                    AccessRequest.from_user_id == user.id,
                    AccessRequest.created_at >= today
                )
            ).count()
            
            if new_requests > 0 or accepted_requests > 0 or sent_requests > 0:
                summary_text = f"📊 Ежедневная сводка\n\n"
                summary_text += f"📨 Новых запросов: {new_requests}\n"
                summary_text += f"✅ Принятых запросов: {accepted_requests}\n"
                summary_text += f"📤 Отправленных запросов: {sent_requests}\n\n"
                
                if new_requests > 0:
                    summary_text += f"💡 У вас есть {new_requests} непросмотренных запросов!\n"
                    summary_text += f"Проверьте раздел '📨 Запросы'"
                
                await self.bot.send_message(
                    chat_id=user_id,
                    text=summary_text,
                    reply_markup=get_main_menu_keyboard()
                )
            
        except Exception as e:
            print(f"Error sending daily summary: {e}")
        finally:
            db.close() 