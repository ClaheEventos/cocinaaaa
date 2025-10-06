from django.urls import path
from .views import JefeTokenObtainView

urlpatterns = [
    path('login/', JefeTokenObtainView.as_view(), name='login_jefe'),
]