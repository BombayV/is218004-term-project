from django.urls import path
from allauth.account.views import login, signup
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('gallery/', views.gallery, name='gallery'),
    path('gallery/<slug:game_slug>/', views.game_detail, name='game_detail'),
    path('gallery/<slug:game_slug>/<int:review_id>/', views.review_detail, name='review_detail'),
    path('users/<int:user_id>/', views.user_profile, name='user_profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Custom auth routes aliasing allauth
    path('login/', login, name='account_login'),
    path('signup/', signup, name='account_signup'),
]