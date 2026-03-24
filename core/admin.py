from django.contrib import admin
from .models import Genre, Game, Review, AdminActionLog

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'genre', 'release_date', 'developer', 'publisher')
    list_filter = ('genre', 'release_date')
    search_fields = ('title', 'developer', 'publisher')

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
