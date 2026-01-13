from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Game, Library, Wishlist

def home(request):
    featured_games = Game.objects.filter(is_featured=True)[:5]
    all_games = Game.objects.all()
    context = {
        'featured_games': featured_games,
        'games': all_games,
    }
    return render(request, 'store/home.html', context)

def game_detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    in_library = False
    in_wishlist = False
    
    if request.user.is_authenticated:
        in_library = Library.objects.filter(user=request.user, game=game).exists()
        in_wishlist = Wishlist.objects.filter(user=request.user, game=game).exists()
        
    context = {
        'game': game,
        'in_library': in_library,
        'in_wishlist': in_wishlist
    }
    return render(request, 'store/game_detail.html', context)

@login_required
def add_to_wishlist(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    Wishlist.objects.get_or_create(user=request.user, game=game)
    messages.success(request, f"{game.title} added to your wishlist!")
    return redirect('game_detail', game_id=game_id)

@login_required
def remove_from_wishlist(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    Wishlist.objects.filter(user=request.user, game=game).delete()
    messages.info(request, f"{game.title} removed from wishlist.")
    return redirect('game_detail', game_id=game_id)

@login_required
def buy_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    if Library.objects.filter(user=request.user, game=game).exists():
        messages.warning(request, "You already own this game!")
    else:
        Library.objects.create(user=request.user, game=game)
        messages.success(request, f"Successfully purchased {game.title}! Added to Library.")
        Wishlist.objects.filter(user=request.user, game=game).delete()
        
    return redirect('library')

# New Views for Community and Support
def community(request):
    return render(request, 'community.html')

def support_hub(request):
    return render(request, 'support.html')