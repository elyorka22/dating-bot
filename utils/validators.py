"""
Система валидации данных для безопасности
"""

import re
from typing import Optional, Tuple, List
from config import MIN_AGE, MAX_AGE, MIN_HEIGHT, MAX_HEIGHT, MIN_WEIGHT, MAX_WEIGHT, GENDERS, MARITAL_STATUSES, INTERESTS

class ValidationError(Exception):
    """Исключение для ошибок валидации"""
    pass

def validate_age(age_str: str) -> Tuple[bool, Optional[int], Optional[str]]:
    """
    Валидация возраста
    
    Args:
        age_str: Строка с возрастом
        
    Returns:
        (is_valid, age_value, error_message)
    """
    try:
        age = int(age_str)
        if MIN_AGE <= age <= MAX_AGE:
            return True, age, None
        else:
            return False, None, f"Возраст должен быть от {MIN_AGE} до {MAX_AGE} лет"
    except ValueError:
        return False, None, "Возраст должен быть числом"

def validate_height(height_str: str) -> Tuple[bool, Optional[int], Optional[str]]:
    """
    Валидация роста
    
    Args:
        height_str: Строка с ростом
        
    Returns:
        (is_valid, height_value, error_message)
    """
    try:
        height = int(height_str)
        if MIN_HEIGHT <= height <= MAX_HEIGHT:
            return True, height, None
        else:
            return False, None, f"Рост должен быть от {MIN_HEIGHT} до {MAX_HEIGHT} см"
    except ValueError:
        return False, None, "Рост должен быть числом"

def validate_weight(weight_str: str) -> Tuple[bool, Optional[int], Optional[str]]:
    """
    Валидация веса
    
    Args:
        weight_str: Строка с весом
        
    Returns:
        (is_valid, weight_value, error_message)
    """
    try:
        weight = int(weight_str)
        if MIN_WEIGHT <= weight <= MAX_WEIGHT:
            return True, weight, None
        else:
            return False, None, f"Вес должен быть от {MIN_WEIGHT} до {MAX_WEIGHT} кг"
    except ValueError:
        return False, None, "Вес должен быть числом"

def validate_gender(gender: str) -> Tuple[bool, Optional[str]]:
    """
    Валидация пола
    
    Args:
        gender: Пол
        
    Returns:
        (is_valid, error_message)
    """
    if gender in GENDERS:
        return True, None
    else:
        return False, f"Пол должен быть одним из: {', '.join(GENDERS)}"

def validate_marital_status(status: str) -> Tuple[bool, Optional[str]]:
    """
    Валидация семейного положения
    
    Args:
        status: Семейное положение
        
    Returns:
        (is_valid, error_message)
    """
    if status in MARITAL_STATUSES:
        return True, None
    else:
        return False, f"Семейное положение должно быть одним из: {', '.join(MARITAL_STATUSES)}"

def validate_interests(interests_list: List[str]) -> Tuple[bool, Optional[str]]:
    """
    Валидация интересов
    
    Args:
        interests_list: Список интересов
        
    Returns:
        (is_valid, error_message)
    """
    if not interests_list:
        return True, None
    
    for interest in interests_list:
        if interest not in INTERESTS:
            return False, f"Неизвестный интерес: {interest}"
    
    return True, None

def validate_bio(bio: str) -> Tuple[bool, Optional[str]]:
    """
    Валидация описания о себе
    
    Args:
        bio: Описание
        
    Returns:
        (is_valid, error_message)
    """
    if not bio:
        return True, None
    
    # Проверяем длину
    if len(bio) > 500:
        return False, "Описание не должно превышать 500 символов"
    
    # Проверяем на запрещенные символы
    forbidden_patterns = [
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
        r'@\w+',
        r'#\w+',
        r'<[^>]+>'
    ]
    
    for pattern in forbidden_patterns:
        if re.search(pattern, bio):
            return False, "Описание содержит запрещенные символы или ссылки"
    
    return True, None

def sanitize_text(text: str) -> str:
    """
    Санитизация текста
    
    Args:
        text: Исходный текст
        
    Returns:
        Очищенный текст
    """
    if not text:
        return ""
    
    # Удаляем HTML теги
    text = re.sub(r'<[^>]+>', '', text)
    
    # Удаляем множественные пробелы
    text = re.sub(r'\s+', ' ', text)
    
    # Обрезаем пробелы
    text = text.strip()
    
    return text

def validate_age_range(min_age: int, max_age: int) -> Tuple[bool, Optional[str]]:
    """
    Валидация диапазона возраста
    
    Args:
        min_age: Минимальный возраст
        max_age: Максимальный возраст
        
    Returns:
        (is_valid, error_message)
    """
    if min_age > max_age:
        return False, "Минимальный возраст не может быть больше максимального"
    
    if min_age < MIN_AGE or max_age > MAX_AGE:
        return False, f"Возраст должен быть от {MIN_AGE} до {MAX_AGE} лет"
    
    return True, None

def validate_height_range(min_height: int, max_height: int) -> Tuple[bool, Optional[str]]:
    """
    Валидация диапазона роста
    
    Args:
        min_height: Минимальный рост
        max_height: Максимальный рост
        
    Returns:
        (is_valid, error_message)
    """
    if min_height > max_height:
        return False, "Минимальный рост не может быть больше максимального"
    
    if min_height < MIN_HEIGHT or max_height > MAX_HEIGHT:
        return False, f"Рост должен быть от {MIN_HEIGHT} до {MAX_HEIGHT} см"
    
    return True, None

def validate_weight_range(min_weight: int, max_weight: int) -> Tuple[bool, Optional[str]]:
    """
    Валидация диапазона веса
    
    Args:
        min_weight: Минимальный вес
        max_weight: Максимальный вес
        
    Returns:
        (is_valid, error_message)
    """
    if min_weight > max_weight:
        return False, "Минимальный вес не может быть больше максимального"
    
    if min_weight < MIN_WEIGHT or max_weight > MAX_WEIGHT:
        return False, f"Вес должен быть от {MIN_WEIGHT} до {MAX_WEIGHT} кг"
    
    return True, None 