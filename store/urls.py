from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('community/', views.community, name='community'),
    path('support-hub/', views.support_hub, name='support_hub'),
]