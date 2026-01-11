from django.shortcuts import render
from .models import Game

def home(request):
    featured_games = Game.objects.filter(is_featured=True)[:5]
    all_games = Game.objects.all()
    context = {
        'featured_games': featured_games,
        'games': all_games,
    }
    return render(request, 'store/home.html', context)