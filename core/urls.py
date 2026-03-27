from django.urls import path
from allauth.account.views import LoginView, SignupView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('gallery/', views.gallery, name='gallery'),
    path('gallery/<slug:game_slug>/', views.game_detail, name='game_detail'),
    path('gallery/<slug:game_slug>/<int:review_id>/', views.review_detail, name='review_detail'),
    path('game/<int:game_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('users/<int:user_id>/', views.user_profile, name='user_profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Custom auth routes aliasing allauth
    path('login/', LoginView.as_view(template_name='core/login.html'), name='account_login'),
    path('signup/', SignupView.as_view(template_name='core/signup.html'), name='account_signup'),
]