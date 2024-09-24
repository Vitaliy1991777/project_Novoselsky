from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_current_usd, name='get_current_usd'),  # Здесь без дублирования
]
