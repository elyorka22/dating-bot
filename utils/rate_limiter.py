"""
Система защиты от спама с rate limiting
"""

import time
from typing import Dict, List, Optional
from collections import defaultdict
from datetime import datetime, timedelta

class RateLimiter:
    """Система ограничения частоты запросов"""
    
    def __init__(self):
        # Хранилище запросов пользователей
        self.user_requests: Dict[int, List[float]] = defaultdict(list)
        
        # Лимиты для разных действий
        self.limits = {
            'message': {'count': 10, 'window': 60},  # 10 сообщений в минуту
            'search': {'count': 5, 'window': 60},    # 5 поисков в минуту
            'request': {'count': 3, 'window': 300},  # 3 запроса в 5 минут
            'profile_edit': {'count': 10, 'window': 300},  # 10 изменений профиля в 5 минут
            'settings_edit': {'count': 10, 'window': 300},  # 10 изменений настроек в 5 минут
        }
    
    def is_allowed(self, user_id: int, action: str) -> bool:
        """
        Проверяет, разрешен ли запрос
        
        Args:
            user_id: ID пользователя
            action: Тип действия
            
        Returns:
            True если запрос разрешен
        """
        if action not in self.limits:
            return True  # Если лимит не установлен, разрешаем
        
        limit = self.limits[action]
        current_time = time.time()
        
        # Очищаем старые запросы
        self._cleanup_old_requests(user_id, current_time - limit['window'])
        
        # Проверяем количество запросов
        user_key = f"{user_id}_{action}"
        requests = self.user_requests[user_key]
        
        if len(requests) >= limit['count']:
            return False
        
        # Добавляем новый запрос
        requests.append(current_time)
        return True
    
    def get_remaining_requests(self, user_id: int, action: str) -> int:
        """
        Возвращает количество оставшихся запросов
        
        Args:
            user_id: ID пользователя
            action: Тип действия
            
        Returns:
            Количество оставшихся запросов
        """
        if action not in self.limits:
            return 999  # Неограниченно
        
        limit = self.limits[action]
        current_time = time.time()
        
        # Очищаем старые запросы
        self._cleanup_old_requests(user_id, current_time - limit['window'])
        
        user_key = f"{user_id}_{action}"
        requests = self.user_requests[user_key]
        
        return max(0, limit['count'] - len(requests))
    
    def get_reset_time(self, user_id: int, action: str) -> Optional[datetime]:
        """
        Возвращает время сброса лимита
        
        Args:
            user_id: ID пользователя
            action: Тип действия
            
        Returns:
            Время сброса лимита
        """
        if action not in self.limits:
            return None
        
        limit = self.limits[action]
        user_key = f"{user_id}_{action}"
        requests = self.user_requests[user_key]
        
        if not requests:
            return None
        
        # Время самого старого запроса + окно
        oldest_request = min(requests)
        return datetime.fromtimestamp(oldest_request + limit['window'])
    
    def _cleanup_old_requests(self, user_id: int, cutoff_time: float):
        """Очищает старые запросы"""
        for action in self.limits.keys():
            user_key = f"{user_id}_{action}"
            requests = self.user_requests[user_key]
            self.user_requests[user_key] = [req for req in requests if req > cutoff_time]
    
    def reset_user_limits(self, user_id: int):
        """Сбрасывает все лимиты для пользователя"""
        for action in self.limits.keys():
            user_key = f"{user_id}_{action}"
            self.user_requests[user_key] = []

class SpamProtection:
    """Система защиты от спама"""
    
    def __init__(self):
        self.rate_limiter = RateLimiter()
        self.suspicious_users: Dict[int, Dict] = defaultdict(dict)
        
        # Пороги для подозрительной активности
        self.suspicion_thresholds = {
            'repeated_errors': 5,  # 5 ошибок подряд
            'rapid_requests': 20,  # 20 запросов за короткое время
            'invalid_inputs': 10,  # 10 неверных вводов
        }
    
    def check_message_spam(self, user_id: int, message_text: str) -> Dict[str, any]:
        """
        Проверяет сообщение на спам
        
        Args:
            user_id: ID пользователя
            message_text: Текст сообщения
            
        Returns:
            Результат проверки
        """
        result = {
            'is_spam': False,
            'reason': None,
            'action': 'allow'
        }
        
        # Проверяем rate limiting
        if not self.rate_limiter.is_allowed(user_id, 'message'):
            result['is_spam'] = True
            result['reason'] = 'rate_limit_exceeded'
            result['action'] = 'block'
            return result
        
        # Проверяем на повторяющиеся символы
        if self._has_repeated_chars(message_text):
            result['is_spam'] = True
            result['reason'] = 'repeated_characters'
            result['action'] = 'warn'
        
        # Проверяем на капс
        if self._is_all_caps(message_text):
            result['is_spam'] = True
            result['reason'] = 'all_caps'
            result['action'] = 'warn'
        
        # Проверяем на ссылки
        if self._contains_links(message_text):
            result['is_spam'] = True
            result['reason'] = 'contains_links'
            result['action'] = 'block'
        
        return result
    
    def check_action_spam(self, user_id: int, action: str) -> Dict[str, any]:
        """
        Проверяет действие на спам
        
        Args:
            user_id: ID пользователя
            action: Тип действия
            
        Returns:
            Результат проверки
        """
        result = {
            'is_spam': False,
            'reason': None,
            'action': 'allow',
            'remaining_requests': 0,
            'reset_time': None
        }
        
        # Проверяем rate limiting
        if not self.rate_limiter.is_allowed(user_id, action):
            result['is_spam'] = True
            result['reason'] = 'rate_limit_exceeded'
            result['action'] = 'block'
            result['remaining_requests'] = 0
            result['reset_time'] = self.rate_limiter.get_reset_time(user_id, action)
            return result
        
        result['remaining_requests'] = self.rate_limiter.get_remaining_requests(user_id, action)
        result['reset_time'] = self.rate_limiter.get_reset_time(user_id, action)
        
        return result
    
    def record_error(self, user_id: int, error_type: str):
        """Записывает ошибку пользователя"""
        if user_id not in self.suspicious_users:
            self.suspicious_users[user_id] = {
                'repeated_errors': 0,
                'rapid_requests': 0,
                'invalid_inputs': 0,
                'last_error_time': None
            }
        
        user_data = self.suspicious_users[user_id]
        current_time = time.time()
        
        # Увеличиваем счетчик ошибок
        if error_type in user_data:
            user_data[error_type] += 1
        
        user_data['last_error_time'] = current_time
        
        # Проверяем на подозрительную активность
        if user_data['repeated_errors'] >= self.suspicion_thresholds['repeated_errors']:
            # Временно блокируем пользователя
            self._temporary_block(user_id, 'repeated_errors')
    
    def _has_repeated_chars(self, text: str) -> bool:
        """Проверяет на повторяющиеся символы"""
        if len(text) < 3:
            return False
        
        for i in range(len(text) - 2):
            if text[i] == text[i+1] == text[i+2]:
                return True
        return False
    
    def _is_all_caps(self, text: str) -> bool:
        """Проверяет на капс"""
        if len(text) < 5:
            return False
        
        letters = [c for c in text if c.isalpha()]
        if not letters:
            return False
        
        return all(c.isupper() for c in letters)
    
    def _contains_links(self, text: str) -> bool:
        """Проверяет на наличие ссылок"""
        import re
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return bool(re.search(url_pattern, text))
    
    def _temporary_block(self, user_id: int, reason: str):
        """Временно блокирует пользователя"""
        # Здесь можно добавить логику временной блокировки
        # Например, добавить в базу данных или кэш
        print(f"Temporary block for user {user_id} due to {reason}")
    
    def is_user_blocked(self, user_id: int) -> bool:
        """Проверяет, заблокирован ли пользователь"""
        # Здесь можно добавить проверку блокировки
        return False

# Глобальный экземпляр
spam_protection = SpamProtection() 