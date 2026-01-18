from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Game, Library, Wishlist, Cart, CartItem, Review
from .forms import ReviewForm

def home(request):
    featured_games = Game.objects.filter(is_featured=True)[:10]
    # For the grid, we can show recent games or random ones
    games = Game.objects.filter(is_featured=True)[:4] 
    context = {
        'featured_games': featured_games,
        'games': games, 
    }
    return render(request, 'store/home.html', context)

def browse_games(request):
    query = request.GET.get('q')
    genre_filter = request.GET.get('genre')
    games = Game.objects.all().order_by('-release_date')
    
    if query:
        games = games.filter(Q(title__icontains=query) | Q(description__icontains=query))
    
    if genre_filter:
        games = games.filter(genre=genre_filter)

    # Get all unique genres for the filter dropdown
    genres = Game.objects.values_list('genre', flat=True).distinct()

    context = {
        'games': games, 
        'query': query, 
        'genre_filter': genre_filter,
        'genres': genres
    }
    return render(request, 'store/browse.html', context)

def game_detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    in_library = False
    in_wishlist = False
    in_cart = False
    
    if request.user.is_authenticated:
        in_library = Library.objects.filter(user=request.user, game=game).exists()
        in_wishlist = Wishlist.objects.filter(user=request.user, game=game).exists()
        cart, _ = Cart.objects.get_or_create(user=request.user)
        in_cart = CartItem.objects.filter(cart=cart, game=game).exists()

    # --- Review Logic ---
    reviews = game.reviews.all().order_by('-created_at')
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.game = game
            review.user = request.user
            review.save()
            messages.success(request, 'Review posted successfully!')
            return redirect('game_detail', game_id=game_id)
    else:
        form = ReviewForm()
        
    context = {
        'game': game,
        'in_library': in_library,
        'in_wishlist': in_wishlist,
        'in_cart': in_cart,
        'reviews': reviews,
        'form': form
    }
    return render(request, 'store/game_detail.html', context)

@login_required
def add_to_wishlist(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    Wishlist.objects.get_or_create(user=request.user, game=game)
    messages.success(request, "Added to wishlist")
    return redirect('game_detail', game_id=game_id)

@login_required
def remove_from_wishlist(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    Wishlist.objects.filter(user=request.user, game=game).delete()
    messages.info(request, "Removed from wishlist")
    return redirect('game_detail', game_id=game_id)

@login_required
def add_to_cart(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    if Library.objects.filter(user=request.user, game=game).exists():
        messages.warning(request, "You already own this game!")
        return redirect('game_detail', game_id=game_id)
        
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, game=game)
    if created:
        messages.success(request, f"{game.title} added to cart")
    else:
        messages.info(request, "Already in cart")
    return redirect('view_cart')

@login_required
def remove_from_cart(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    cart = get_object_or_404(Cart, user=request.user)
    CartItem.objects.filter(cart=cart, game=game).delete()
    messages.info(request, "Removed from cart")
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'store/cart.html', {'cart': cart})

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.all()
    
    if not items:
        messages.warning(request, "Your cart is empty!")
        return redirect('view_cart')
        
    for item in items:
        # Check if already owned just in case
        if not Library.objects.filter(user=request.user, game=item.game).exists():
            Library.objects.create(user=request.user, game=item.game)
            # Remove from wishlist if purchased
            Wishlist.objects.filter(user=request.user, game=item.game).delete()
            
    # Clear cart
    cart.items.all().delete()
    messages.success(request, "Purchase successful! Games added to library.")
    return redirect('library')

@login_required
def buy_game(request, game_id):
    # Direct buy shortcut
    game = get_object_or_404(Game, pk=game_id)
    if Library.objects.filter(user=request.user, game=game).exists():
        messages.warning(request, "You already own this game!")
    else:
        Library.objects.create(user=request.user, game=game)
        messages.success(request, f"Purchased {game.title}!")
        Wishlist.objects.filter(user=request.user, game=game).delete()
    return redirect('library')

def community(request):
    return render(request, 'community.html')

def support_hub(request):
    return render(request, 'support.html')

@login_required
def library(request):
    library_items = Library.objects.filter(user=request.user).select_related('game')
    games = [item.game for item in library_items]
    context = {'games': games}
    return render(request, 'users/library.html', context)