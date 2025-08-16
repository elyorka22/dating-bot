"""
Адаптер для работы с Supabase API
"""

from supabase import create_client, Client
from typing import Optional, List, Dict, Any
from config import SUPABASE_URL, SUPABASE_KEY

class SupabaseAdapter:
    def __init__(self):
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    def create_user(self, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Создать пользователя"""
        try:
            response = self.supabase.table('users').insert(user_data).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def get_user_by_telegram_id(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        """Получить пользователя по telegram_id"""
        try:
            response = self.supabase.table('users').select('*').eq('telegram_id', telegram_id).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def update_user(self, telegram_id: int, user_data: Dict[str, Any]) -> bool:
        """Обновить пользователя"""
        try:
            response = self.supabase.table('users').update(user_data).eq('telegram_id', telegram_id).execute()
            return len(response.data) > 0
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    def create_search_settings(self, settings_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Создать настройки поиска"""
        try:
            response = self.supabase.table('search_settings').insert(settings_data).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error creating search settings: {e}")
            return None
    
    def get_search_settings(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Получить настройки поиска"""
        try:
            response = self.supabase.table('search_settings').select('*').eq('user_id', user_id).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error getting search settings: {e}")
            return None
    
    def update_search_settings(self, user_id: int, settings_data: Dict[str, Any]) -> bool:
        """Обновить настройки поиска"""
        try:
            response = self.supabase.table('search_settings').update(settings_data).eq('user_id', user_id).execute()
            return len(response.data) > 0
        except Exception as e:
            print(f"Error updating search settings: {e}")
            return False
    
    def find_suitable_users(self, current_user_id: int, search_settings: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Найти подходящих пользователей"""
        try:
            # Базовый запрос
            query = self.supabase.table('users').select('*').neq('id', current_user_id).eq('is_active', True)
            
            # Фильтр по полу
            if search_settings.get('gender_preference') == 'Мужчины':
                query = query.eq('gender', 'Мужчина')
            elif search_settings.get('gender_preference') == 'Женщины':
                query = query.eq('gender', 'Женщина')
            
            # Фильтр по возрасту
            query = query.gte('age', search_settings.get('min_age')).lte('age', search_settings.get('max_age'))
            
            # Фильтр по росту
            query = query.gte('height', search_settings.get('min_height')).lte('height', search_settings.get('max_height'))
            
            # Фильтр по весу
            query = query.gte('weight', search_settings.get('min_weight')).lte('weight', search_settings.get('max_weight'))
            
            response = query.execute()
            return response.data
        except Exception as e:
            print(f"Error finding suitable users: {e}")
            return []
    
    def create_access_request(self, request_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Создать запрос на доступ"""
        try:
            response = self.supabase.table('access_requests').insert(request_data).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error creating access request: {e}")
            return None
    
    def get_pending_requests(self, user_id: int) -> List[Dict[str, Any]]:
        """Получить входящие запросы"""
        try:
            response = self.supabase.table('access_requests').select('*').eq('to_user_id', user_id).eq('status', 'pending').execute()
            return response.data
        except Exception as e:
            print(f"Error getting pending requests: {e}")
            return []
    
    def update_request_status(self, request_id: int, status: str) -> bool:
        """Обновить статус запроса"""
        try:
            response = self.supabase.table('access_requests').update({'status': status}).eq('id', request_id).execute()
            return len(response.data) > 0
        except Exception as e:
            print(f"Error updating request status: {e}")
            return False
    
    def create_allowed_contact(self, contact_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Создать разрешенный контакт"""
        try:
            response = self.supabase.table('allowed_contacts').insert(contact_data).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error creating allowed contact: {e}")
            return None
    
    def get_user_statistics(self, user_id: int) -> Dict[str, int]:
        """Получить статистику пользователя"""
        try:
            # Отправленные запросы
            sent_response = self.supabase.table('access_requests').select('id', count='exact').eq('from_user_id', user_id).execute()
            sent_count = sent_response.count if hasattr(sent_response, 'count') else len(sent_response.data)
            
            # Полученные запросы
            received_response = self.supabase.table('access_requests').select('id', count='exact').eq('to_user_id', user_id).execute()
            received_count = received_response.count if hasattr(received_response, 'count') else len(received_response.data)
            
            # Принятые запросы
            accepted_response = self.supabase.table('access_requests').select('id', count='exact').eq('to_user_id', user_id).eq('status', 'accepted').execute()
            accepted_count = accepted_response.count if hasattr(accepted_response, 'count') else len(accepted_response.data)
            
            return {
                'sent_requests': sent_count,
                'received_requests': received_count,
                'accepted_requests': accepted_count
            }
        except Exception as e:
            print(f"Error getting user statistics: {e}")
            return {'sent_requests': 0, 'received_requests': 0, 'accepted_requests': 0} 