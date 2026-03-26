from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Platform(models.Model):
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
    genres = models.ManyToManyField(Genre, related_name='games')
    platforms = models.ManyToManyField(Platform, related_name='games', blank=True)
    release_date = models.DateField()
    developer = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    cover_image = models.ImageField(upload_to='game_covers/', blank=True, null=True)
    description = models.TextField()
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def update_rating(self):
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        self.average_rating = avg if avg is not None else 0.0
        self.save(update_fields=['average_rating'])

    def __str__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_text = models.TextField()
    is_spoiler = models.BooleanField(default=False)
    helpful_votes = models.ManyToManyField(User, related_name='helpful_reviews', blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'game') # A user can review a game only once
        ordering = ['-date_posted']

    def __str__(self):
        return f"{self.user.username}'s review of {self.game.title}"

@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def update_game_rating(sender, instance, **kwargs):
    instance.game.update_rating()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, max_length=500)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    favorite_games = models.ManyToManyField(Game, related_name='favorited_by', blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

class AdminActionLog(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='action_logs')
    action_type = models.CharField(max_length=100)
    action_details = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.admin.username} - {self.action_type} at {self.timestamp}"
