from .models import Cart


def cart_counter(request):
    """
    Контекстный процессор, добавляющий количество товаров в корзине
    во все шаблоны (доступно как переменная `cart_total_items`).
    """
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        if not request.session.session_key:
            return {'cart_total_items': 0}
        cart = Cart.objects.filter(
            session_key=request.session.session_key
        ).first()

    if cart:
        return {'cart_total_items': cart.total_items}
    return {'cart_total_items': 0}
