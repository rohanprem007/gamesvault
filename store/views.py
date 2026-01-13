from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Game, Library, Wishlist

def home(request):
    # Only fetch Top 10 Featured games for Home Page
    featured_games = Game.objects.filter(is_featured=True)[:10]
    
    context = {
        'featured_games': featured_games,
        'games': featured_games, # For the grid on home page, usually just show trending too
    }
    return render(request, 'store/home.html', context)

def browse_games(request):
    # Fetch ALL games for the browse page
    query = request.GET.get('q')
    genre_filter = request.GET.get('genre')
    
    games = Game.objects.all().order_by('-release_date')
    
    if query:
        games = games.filter(Q(title__icontains=query) | Q(description__icontains=query))
    
    if genre_filter:
        games = games.filter(genre=genre_filter)
        
    context = {
        'games': games,
        'query': query,
        'genre_filter': genre_filter
    }
    return render(request, 'store/browse.html', context)

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

def community(request):
    return render(request, 'community.html')

def support_hub(request):
    return render(request, 'support.html')