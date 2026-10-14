"""
Модуль для модерации отзывов.

Проверяет текст на наличие запрещённых слов.
Список FORBIDDEN_WORDS — это заглушка.
В реальном проекте его нужно заменить на полноценный
список нецензурной лексики или подключить библиотеку
вроде `better_profanity` или `profanity-check`.
"""

import re


# Заглушка: список «плохих» слов для теста
# В продакшене заменить на реальный список
FORBIDDEN_WORDS = [
    'плохоеслово',
    'ругательство',
    'запрещёнка',
    'test_bad_word',
]


def contains_forbidden_words(text):
    """
    Проверяет, содержит ли текст запрещённые слова.
    Возвращает True, если найдено хотя бы одно.
    """
    if not text:
        return False

    text_lower = text.lower()
    for word in FORBIDDEN_WORDS:
        if re.search(rf'\b{re.escape(word)}', text_lower):
            return True
    return False


def get_forbidden_words(text):
    """
    Возвращает список запрещённых слов, найденных в тексте.
    Полезно для отладки и сообщений пользователю.
    """
    if not text:
        return []

    text_lower = text.lower()
    found = []
    for word in FORBIDDEN_WORDS:
        if re.search(rf'\b{re.escape(word)}', text_lower):
            found.append(word)
    return found
