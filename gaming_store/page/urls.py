# page/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.game_list, name='game_list'),
]
