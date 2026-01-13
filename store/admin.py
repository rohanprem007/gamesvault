from django.contrib import admin
from .models import Game, Library, Wishlist, Cart, CartItem

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'genre', 'is_featured')
    list_filter = ('genre', 'is_featured')
    search_fields = ('title', 'description')

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'purchase_date')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'added_at')

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'total_price')
    inlines = [CartItemInline]