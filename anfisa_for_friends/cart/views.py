from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

from .cart import CartService
from .forms import OrderCreateForm
from .models import Order, OrderItem


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


def order_create(request):
    """
    Оформление заказа из корзины.
    Если пользователь авторизован, поля предзаполняются из профиля.
    """
    cart_service = CartService(request)
    cart = cart_service.cart

    if not cart.items.exists():
        messages.warning(request, 'Ваша корзина пуста.')
        return redirect('ice_cream:ice_cream_list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.total_price = cart.total_price
            order.save()

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_title=item.product.title,
                    price=item.product.price,
                    quantity=item.quantity,
                )

            cart_service.clear()
            messages.success(request, 'Заказ успешно оформлен!')
            return redirect('cart:order_success', order_id=order.id)
    else:
        # Предзаполняем форму из профиля пользователя
        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'phone': request.user.phone,
                'email': request.user.email,
                'address': request.user.address,
            }
            form = OrderCreateForm(initial=initial_data)
        else:
            form = OrderCreateForm()

    return render(request, 'cart/order_create.html', {
        'form': form,
        'cart': cart,
    })


def order_success(request, order_id):
    """
    Страница «Спасибо за заказ».
    """
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'cart/order_success.html', {'order': order})


@login_required
def order_history(request):
    """
    История заказов текущего пользователя.
    """
    orders = Order.objects.filter(user=request.user)
    return render(request, 'cart/order_history.html', {'orders': orders})
