from django.shortcuts import render
from games.models import Game
from datetime import date, timedelta

def game_list(request):
    all_games = Game.objects.all()

    new_games = Game.objects.filter(release_date__gte=date.today() - timedelta(days=30))
    recent_games = Game.objects.order_by('-release_date')[:6]

    return render(request, 'page/home.html', {
        'games': all_games,
        'new_games': new_games,
        'recent_games': recent_games,
    })
