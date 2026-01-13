from django.contrib import admin
from .models import Game, Library, Wishlist

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'genre', 'is_featured')
    list_filter = ('genre', 'is_featured')
    search_fields = ('title', 'description')

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'purchase_date')
    search_fields = ('user__username', 'game__title')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'added_at')