# ventas/urls.py
from django.urls import path
from .views import VentasLoginView

urlpatterns = [
    path('login/', VentasLoginView.as_view(), name='login_ventas'),
]