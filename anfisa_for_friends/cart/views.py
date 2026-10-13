from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

from .cart import CartService


def cart_detail(request):
    """
    Страница корзины с итоговой суммой.
    """
    cart_service = CartService(request)
    return render(request, 'cart/detail.html', {'cart': cart_service.cart})


@require_POST
def cart_add(request, product_id):
    """
    Добавляет товар в корзину.
    Принимает product_id из URL и quantity из POST.
    """
    cart_service = CartService(request)
    quantity = int(request.POST.get('quantity', 1))
    cart_service.add(product_id, quantity)
    messages.success(request, 'Товар добавлен в корзину!')
    return redirect('cart:cart_detail')


@require_POST
def cart_update(request, item_id):
    """
    Обновляет количество товара в позиции (через обычную форму).
    """
    cart_service = CartService(request)
    quantity = int(request.POST.get('quantity', 1))
    cart_service.update_quantity(item_id, quantity)
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, item_id):
    """
    Удаляет позицию из корзины.
    """
    cart_service = CartService(request)
    cart_service.remove(item_id)
    messages.info(request, 'Товар удалён из корзины.')
    return redirect('cart:cart_detail')


@require_POST
def cart_update_ajax(request):
    """
    AJAX-обновление количества товара в корзине.
    Принимает JSON: {"item_id": 1, "quantity": 2}
    Возвращает JSON: {"success": true, "item_total": ..., "cart_total": ..., "cart_items": ...}
    """
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = int(data.get('quantity', 1))
    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse(
            {'success': False, 'error': 'Invalid data'},
            status=400
        )

    cart_service = CartService(request)
    cart_service.update_quantity(item_id, quantity)

    cart = cart_service.cart
    item = cart.items.filter(id=item_id).first()

    return JsonResponse({
        'success': True,
        'item_total': str(item.total_price) if item else '0',
        'cart_total': str(cart.total_price),
        'cart_items': cart.total_items,
    })
