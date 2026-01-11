from django.contrib import admin
from .models import Game

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'genre', 'is_featured')
    list_filter = ('genre', 'is_featured')
    search_fields = ('title', 'description')