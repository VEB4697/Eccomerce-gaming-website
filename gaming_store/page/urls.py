# page/urls.py
from django.urls import path
from . import views

app_name = 'page'

urlpatterns = [
    # This path maps the root URL ('') to your game_list view.
    path('', views.game_list, name='home'),
    # Add this new path for the About page
    path('about/', views.about_view, name='about'),
]
