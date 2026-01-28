from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('browse/', views.browse_games, name='browse_games'),
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),
    
    # Wishlist
    path('game/<int:game_id>/wishlist/add/', views.add_to_wishlist, name='add_to_wishlist'),
    path('game/<int:game_id>/wishlist/remove/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    # Cart & Purchase
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:game_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:game_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('game/<int:game_id>/buy/', views.buy_game, name='buy_game'),
    
    # Library Management (New)
    path('remove-from-library/<int:game_id>/', views.remove_from_library, name='remove_from_library'),
    path('library/', views.library, name='library'),
    path('wishlist/', views.wishlist, name='wishlist'),

    # Misc
    path('community/', views.community, name='community'),
    path('support-hub/', views.support_hub, name='support_hub'),
]