from django.shortcuts import render
from .models import Game

def game_list(request):
    games = Game.objects.all()
    return render(request, 'page/home.html', {
        'games': games,
        'new_games': games.order_by('-release_date')[:5],
        'recent_games': games.order_by('-id')[:5],
    })
