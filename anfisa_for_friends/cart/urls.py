from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('update/<int:item_id>/', views.cart_update, name='cart_update'),
    path('remove/<int:item_id>/', views.cart_remove, name='cart_remove'),
    path('update-ajax/', views.cart_update_ajax, name='cart_update_ajax'),
    path('order/create/', views.order_create, name='order_create'),
    path('order/success/<int:order_id>/',
         views.order_success, name='order_success'),
    path('orders/', views.order_history, name='order_history'),
]
