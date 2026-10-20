from .models import PromoCode


def get_promo_from_session(request):
    """
    Возвращает объект PromoCode из сессии или None.
    Если промокод стал недействительным - удаляет его из сессии.
    """
    code = request.session.get('promo_code')
    if not code:
        return None

    try:
        promo = PromoCode.objects.get(code=code)
    except PromoCode.DoesNotExist:
        request.session.pop('promo_code', None)
        return None

    if not promo.is_valid:
        request.session.pop('promo_code', None)
        return None

    return promo


def apply_promo_to_cart(cart, promo):
    """
    Применяет скидку к корзине.
    Возвращает словарь с итогами:
    - subtotal: сумма без скидки
    - discount: размер скидки
    - total: итоговая сумма
    """
    subtotal = cart.total_price
    if not promo:
        return {
            'subtotal': subtotal,
            'discount': 0,
            'total': subtotal,
            'promo': None,
        }

    discount = (subtotal * promo.discount_percent) / 100
    total = subtotal - discount

    return {
        'subtotal': subtotal,
        'discount': discount,
        'total': total,
        'promo': promo,
    }
