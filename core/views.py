from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Game, Genre, Platform, Review
from .forms import ReviewForm

def home(request):
    """Home page introducing everything"""
    recent_games = Game.objects.order_by('-release_date')[:6]
    context = {'recent_games': recent_games}
    return render(request, 'core/home.html', context)

def gallery(request):
    """Gallery page with URL search params like genre & rating"""
    games = Game.objects.all()
    genres = Genre.objects.all()
    platforms = Platform.objects.all()
    
    genre_slugs = request.GET.getlist('genre')
    platform_slugs = request.GET.getlist('platform')
    rating = request.GET.get('rating')
    query = request.GET.get('q')
    min_date = request.GET.get('min_date')
    max_date = request.GET.get('max_date')
    sort_by = request.GET.get('sort', '-release_date')
    
    has_filters = bool(query or genre_slugs or platform_slugs or rating or min_date or max_date or request.GET.get('sort'))
    
    if query:
        games = games.filter(title__icontains=query)
    
    if genre_slugs:
        games = games.filter(genres__slug__in=genre_slugs).distinct()
        
    if platform_slugs:
        games = games.filter(platforms__slug__in=platform_slugs).distinct()
        
    if rating:
        games = games.filter(average_rating__gte=rating)
        
    if min_date:
        games = games.filter(release_date__gte=min_date)
        
    if max_date:
        games = games.filter(release_date__lte=max_date)
        
    if sort_by == 'newest':
        games = games.order_by('-release_date')
    elif sort_by == 'oldest':
        games = games.order_by('release_date')
    elif sort_by == 'highest_rated':
        games = games.order_by('-average_rating')
    elif sort_by == 'lowest_rated':
        games = games.order_by('average_rating')
    elif sort_by == 'title_asc':
        games = games.order_by('title')
    elif sort_by == 'title_desc':
        games = games.order_by('-title')
    else:
        games = games.order_by('-release_date')
        
    paginator = Paginator(games, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    query_dict = request.GET.copy()
    if 'page' in query_dict:
        del query_dict['page']
    query_string = query_dict.urlencode()
    
    user_favorites = []
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        user_favorites = list(request.user.profile.favorite_games.values_list('id', flat=True))
        
    context = {
        'games': page_obj,
        'genres': genres,
        'platforms': platforms,
        'current_genres': genre_slugs,
        'current_platforms': platform_slugs,
        'rating': rating,
        'query': query,
        'min_date': min_date,
        'max_date': max_date,
        'sort_by': sort_by,
        'has_filters': has_filters,
        'query_string': query_string,
        'user_favorites': user_favorites,
    }
    return render(request, 'core/gallery.html', context)

def game_detail(request, game_slug):
    """Show information about the game"""
    game = get_object_or_404(Game, slug=game_slug)
    reviews = Review.objects.filter(game=game).order_by('-date_posted')
    
    user_review = None
    is_favorited = False
    
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
        if hasattr(request.user, 'profile'):
            is_favorited = game in request.user.profile.favorite_games.all()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('account_login')
            
        if user_review:
            # Update existing review
            form = ReviewForm(request.POST, instance=user_review)
        else:
            # Create new review
            form = ReviewForm(request.POST)
            
        if form.is_valid():
            review = form.save(commit=False)
            review.game = game
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been saved!')
            return redirect('game_detail', game_slug=game.slug)
    else:
        form = ReviewForm(instance=user_review) if user_review else ReviewForm()

    context = {
        'game': game,
        'reviews': reviews,
        'form': form,
        'user_review': user_review,
        'is_favorited': is_favorited,
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

@login_required
def dashboard(request):
    """User dashboard to manage reviews and account settings."""
    user = request.user
    
    # Ensure user has a profile
    if not hasattr(user, 'profile'):
        from .models import UserProfile
        UserProfile.objects.create(user=user)
        
    favorites = user.profile.favorite_games.all()
    reviews = Review.objects.filter(user=user).select_related('game').order_by('-date_posted')
    
    # Recommendation logic based on favorites
    if favorites.exists():
        # Get all genres from favorite games
        favorite_genres = Genre.objects.filter(games__in=favorites).distinct()
        
        # Recommendations: Games in those genres matching high ratings, excluding already favorited games
        recommendations = Game.objects.filter(genres__in=favorite_genres) \
                                      .exclude(id__in=favorites.values_list('id', flat=True)) \
                                      .distinct() \
                                      .order_by('-average_rating')[:3]
        
        # Fallback if no recommendations in those genres
        if not recommendations:
            recommendations = Game.objects.exclude(id__in=favorites.values_list('id', flat=True)) \
                                          .order_by('-average_rating')[:3]
    else:
        # Fallback for users without favorites
        recommendations = Game.objects.order_by('-average_rating')[:3]

    context = {
        'favorites': favorites,
        'reviews': reviews,
        'recommendations': recommendations,
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def toggle_favorite(request, game_id):
    """Toggle a game in the user's favorites"""
    game = get_object_or_404(Game, id=game_id)
    
    if hasattr(request.user, 'profile'):
        profile = request.user.profile
    else:
        from .models import UserProfile
        profile = UserProfile.objects.create(user=request.user)
    
    if game in profile.favorite_games.all():
        profile.favorite_games.remove(game)
        messages.success(request, f'Removed {game.title} from your favorites.')
    else:
        profile.favorite_games.add(game)
        messages.success(request, f'Added {game.title} to your favorites.')
        
    # Redirect back to where the user came from, or home
    next_url = request.GET.get('next', request.META.get('HTTP_REFERER', 'home'))
    return redirect(next_url)

