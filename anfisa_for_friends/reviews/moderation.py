"""
Модуль для модерации отзывов.

Проверяет текст на наличие запрещённых слов.
Список FORBIDDEN_WORDS — это заглушка.
В реальном проекте его нужно заменить на полноценный
список нецензурной лексики или подключить библиотеку
вроде `better_profanity` или `profanity-check`.
"""


# Заглушка: список «плохих» слов для теста (без окончания)
# В продакшене заменить на реальный список
FORBIDDEN_WORDS = [
    'плохоеслов',
    'ругательств',
    'запрещёнк',  # пишем с "ё"
    'test_bad_word',
]


def _normalize(text):
    """
    Приводит текст к единому виду для проверки:
    нижний регистр и замена "ё" на "е".
    """
    return text.lower().replace('ё', 'е')


def contains_forbidden_words(text):
    """
    Проверяет, содержит ли текст запрещённые слова.
    Возвращает True, если найдено хотя бы одно.
    """
    if not text:
        return False

    text_normalized = _normalize(text)

    # Нормализуем слово из словаря, чтобы избежать проблем с "ё"
    for word in FORBIDDEN_WORDS:
        if _normalize(word) in text_normalized:
            return True
    return False


def get_forbidden_words(text):
    """
    Возвращает список запрещённых слов, найденных в тексте.
    Полезно для отладки и сообщений пользователю.
    """
    if not text:
        return []

    found = []
    text_normalized = _normalize(text)

    for word in FORBIDDEN_WORDS:
        if _normalize(word) in text_normalized:
            found.append(word)
    return found
