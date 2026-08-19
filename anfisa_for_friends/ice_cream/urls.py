from django.urls import path

from .views import IceCreamListView, IceCreamDetailView

app_name = 'ice_cream'

urlpatterns = [
    path('', IceCreamListView.as_view(), name='ice_cream_list'),
    path('<int:pk>/', IceCreamDetailView.as_view(), name='ice_cream_detail'),
]
