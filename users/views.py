from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from store.models import Library, Wishlist

# ... existing register/logout views ...
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'users/logout.html')

@login_required
def profile(request):
    # Pass basic stats to dashboard
    library_count = Library.objects.filter(user=request.user).count()
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    return render(request, 'users/profile.html', {
        'library_count': library_count,
        'wishlist_count': wishlist_count
    })

@login_required
def library(request):
    # Fetch actual games owned by user
    library_items = Library.objects.filter(user=request.user).select_related('game')
    return render(request, 'users/library.html', {'library_items': library_items})

@login_required
def wishlist(request):
    # Fetch wishlist items
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('game')
    return render(request, 'users/wishlist.html', {'wishlist_items': wishlist_items})