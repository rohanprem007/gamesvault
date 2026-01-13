from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('browse/', views.browse_games, name='browse_games'), # Key route for View All
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),
    path('game/<int:game_id>/wishlist/add/', views.add_to_wishlist, name='add_to_wishlist'),
    path('game/<int:game_id>/wishlist/remove/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('game/<int:game_id>/buy/', views.buy_game, name='buy_game'),
    path('community/', views.community, name='community'),
    path('support-hub/', views.support_hub, name='support_hub'),
]