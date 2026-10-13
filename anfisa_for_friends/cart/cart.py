from .models import Cart, CartItem
from ice_cream.models import IceCream


class CartService:
    """
    Сервис для работы с корзиной.
    Инкапсулирует логику получения, добавления и удаления товаров.
    """

    def __init__(self, request):
        self.request = request
        self.cart = self._get_or_create_cart()

    def _get_or_create_cart(self):
        """
        Возвращает корзину текущего пользователя или гостя.
        Для гостя использует ключ сессии.
        """
        if self.request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=self.request.user)
        else:
            if not self.request.session.session_key:
                self.request.session.create()
            cart, _ = Cart.objects.get_or_create(
                session_key=self.request.session.session_key
            )
        return cart

    def add(self, product_id, quantity=1):
        """
        Добавляет товар в корзину или увеличивает его количество.
        """
        product = IceCream.objects.get(id=product_id)
        item, created = CartItem.objects.get_or_create(
            cart=self.cart,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            item.quantity += quantity
            item.save()
        return item

    def remove(self, item_id):
        """Удаляет позицию из корзины."""
        CartItem.objects.filter(cart=self.cart, id=item_id).delete()

    def update_quantity(self, item_id, quantity):
        """Обновляет количество товара в позиции."""
        if quantity <= 0:
            self.remove(item_id)
            return
        CartItem.objects.filter(
            cart=self.cart, id=item_id).update(quantity=quantity)

    def clear(self):
        """Полностью очищает корзину."""
        self.cart.items.all().delete()
