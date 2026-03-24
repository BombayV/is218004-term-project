from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Game(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, related_name='games')
    release_date = models.DateField()
    developer = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    cover_image = models.ImageField(upload_to='game_covers/', blank=True, null=True)
    description = models.TextField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_text = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game') # A user can review a game only once
        ordering = ['-date_posted']

    def __str__(self):
        return f"{self.user.username}'s review of {self.game.title}"

class AdminActionLog(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='action_logs')
    action_type = models.CharField(max_length=100)
    action_details = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.admin.username} - {self.action_type} at {self.timestamp}"
