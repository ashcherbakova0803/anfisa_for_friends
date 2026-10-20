import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404


from notifications.emails import send_order_confirmation
from .cart import CartService
from .forms import OrderCreateForm
from .models import Order, OrderItem, PromoCode
from .promo import get_promo_from_session, apply_promo_to_cart


def cart_detail(request):
    """
    Страница корзины с итоговой суммой и применённым промокодом.
    """
    cart_service = CartService(request)
    cart = cart_service.cart
    promo = get_promo_from_session(request)
    totals = apply_promo_to_cart(cart, promo)

    return render(request, 'cart/detail.html', {
        'cart': cart,
        'promo': promo,
        'totals': totals,
    })


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
    promo = get_promo_from_session(request)
    totals = apply_promo_to_cart(cart, promo)

    if not cart.items.exists():
        messages.warning(request, 'Ваша корзина пуста.')
        return redirect('ice_cream:ice_cream_list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.total_price = totals['total']
            order.save()

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_title=item.product.title,
                    price=item.product.price,
                    quantity=item.quantity,
                )

            if promo:
                promo.apply()
                request.session.pop('promo_code', None)

            cart_service.clear()
            send_order_confirmation(order)
            messages.success(request, 'Заказ успешно оформлен!')
            return redirect('cart:order_success', order_id=order.id)
    else:
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
        'promo': promo,
        'totals': totals,
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


@login_required
def order_repeat_check(request, order_id):
    """
    AJAX-проверка товаров из заказа на наличие.
    Возвращает список позиций, которых нет в наличии, и список доступных.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)

    unavailable = []
    available = []

    for item in order.items.all():
        if item.product and item.product.is_available:
            available.append({
                'product_id': item.product.id,
                'title': item.product_title,
                'quantity': item.quantity,
            })
        else:
            unavailable.append({
                'title': item.product_title,
                'quantity': item.quantity,
            })

    return JsonResponse({
        'available': available,
        'unavailable': unavailable,
    })


@login_required
@require_POST
def order_repeat(request, order_id):
    """
    Повторяет заказ: добавляет доступные позиции в корзину.
    Принимает флаг skip_unavailable (true/false).
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    skip_unavailable = request.POST.get('skip_unavailable') == 'true'

    cart_service = CartService(request)
    added_count = 0
    skipped_count = 0

    for item in order.items.all():
        if item.product and item.product.is_available:
            cart_service.add(item.product.id, item.quantity)
            added_count += 1
        else:
            skipped_count += 1
            if not skip_unavailable:
                messages.warning(
                    request,
                    f'Товар «{item.product_title}» закончился и не был добавлен.'
                )

    if added_count > 0:
        messages.success(
            request,
            f'В корзину добавлено {added_count} товар(ов) из заказа №{order.id}.'
        )
    if skipped_count > 0 and skip_unavailable:
        messages.info(
            request,
            f'{skipped_count} товар(ов) пропущено (нет в наличии).'
        )

    return redirect('cart:cart_detail')


@require_POST
def apply_promo(request):
    """
    AJAX-применение промокода.
    Принимает JSON: {"code": "SUMMER15"}
    """
    try:
        data = json.loads(request.body)
        code = data.get('code', '').strip().upper()
    except (ValueError, json.JSONDecodeError):
        return JsonResponse({'success': False, 'error': 'Некорректный запрос'}, status=400)

    if not code:
        return JsonResponse({'success': False, 'error': 'Введите промокод'})

    try:
        promo = PromoCode.objects.get(code=code)
    except PromoCode.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Промокод не найден'})

    if not promo.is_valid:
        return JsonResponse({'success': False, 'error': 'Промокод недействителен или истёк'})

    request.session['promo_code'] = promo.code

    cart_service = CartService(request)
    totals = apply_promo_to_cart(cart_service.cart, promo)

    return JsonResponse({
        'success': True,
        'promo_code': promo.code,
        'discount_percent': promo.discount_percent,
        'subtotal': str(totals['subtotal']),
        'discount': str(totals['discount']),
        'total': str(totals['total']),
    })


@require_POST
def remove_promo(request):
    """
    Удаляет промокод из сессии.
    """
    request.session.pop('promo_code', None)
    cart_service = CartService(request)
    totals = apply_promo_to_cart(cart_service.cart, None)

    return JsonResponse({
        'success': True,
        'subtotal': str(totals['subtotal']),
        'total': str(totals['total']),
    })
