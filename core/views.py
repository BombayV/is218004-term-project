from django.shortcuts import render, get_object_or_404
from .models import Game, Genre, Review

def home(request):
    """Home page introducing everything"""
    recent_games = Game.objects.order_by('-release_date')[:6]
    context = {'recent_games': recent_games}
    return render(request, 'core/home.html', context)

def gallery(request):
    """Gallery page with URL search params like genre & rating"""
    games = Game.objects.all()
    genres = Genre.objects.all()
    
    genre_slug = request.GET.get('genre')
    rating = request.GET.get('rating')
    query = request.GET.get('q')
    
    if query:
        games = games.filter(title__icontains=query)
    
    if genre_slug:
        games = games.filter(genre__slug=genre_slug)
        
    context = {
        'games': games,
        'genres': genres,
        'current_genre': genre_slug,
        'rating': rating,
        'query': query,
    }
    return render(request, 'core/gallery.html', context)

def game_detail(request, game_slug):
    """Show information about the game"""
    game = get_object_or_404(Game, slug=game_slug)
    reviews = Review.objects.filter(game=game).order_by('-date_posted')
    context = {
        'game': game,
        'reviews': reviews
    }
    return render(request, 'core/game_detail.html', context)

def review_detail(request, game_slug, review_id):
    """Custom page to show a single review"""
    context = {'game_slug': game_slug, 'review_id': review_id}
    return render(request, 'core/review_detail.html', context)

def user_profile(request, user_id):
    """Show reviews and other info about users"""
    context = {'user_id': user_id}
    return render(request, 'core/user_profile.html', context)

def dashboard(request):
    """Users can manage reviews and other stuff while admins have other options available"""
    return render(request, 'core/dashboard.html')

