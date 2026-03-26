from django.contrib import admin
from .models import Genre, Platform, Game, Review, AdminActionLog, UserProfile

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', )
    search_fields = ('user__username',)

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'release_date', 'developer', 'publisher', 'average_rating')
    list_filter = ('genres', 'platforms', 'release_date')
    search_fields = ('title', 'developer', 'publisher')
    filter_horizontal = ('genres', 'platforms')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('game', 'user', 'rating', 'date_posted')
    list_filter = ('rating', 'date_posted')
    search_fields = ('user__username', 'game__title')

@admin.register(AdminActionLog)
class AdminActionLogAdmin(admin.ModelAdmin):
    list_display = ('admin', 'action_type', 'timestamp')
    readonly_fields = ('admin', 'action_type', 'action_details', 'timestamp')
    list_filter = ('action_type', 'timestamp')
    search_fields = ('admin__username', 'action_type')

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
