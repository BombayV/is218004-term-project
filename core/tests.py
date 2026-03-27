from django.test import TestCase
from django.contrib.auth.models import User
from .models import Game, Review, Genre, Platform
from datetime import date

class GameModelTestCase(TestCase):
    def setUp(self):
        # Create a genre and platform for the game
        self.genre = Genre.objects.create(name="Action")
        self.platform = Platform.objects.create(name="PC")

    def test_create_game(self):
        # Create a game
        game = Game.objects.create(
            title="Test Game 1",
            release_date=date(2023, 1, 1),
            developer="Test Dev",
            publisher="Test Pub",
            description="A test game description"
        )
        game.genres.add(self.genre)
        game.platforms.add(self.platform)

        # Assertions to check if the game was created correctly
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(game.title, "Test Game 1")
        self.assertEqual(game.slug, "test-game-1") # Check slug formatting
        self.assertIn(self.genre, game.genres.all())
        self.assertIn(self.platform, game.platforms.all())

class ReviewModelTestCase(TestCase):
    def setUp(self):
        # Create a user, a game for the review
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.game = Game.objects.create(
            title="Review Test Game",
            release_date=date(2023, 2, 2),
            developer="Review Dev",
            publisher="Review Pub",
            description="Game to review"
        )

    def test_create_review(self):
        # Create a review
        review = Review.objects.create(
            user=self.user,
            game=self.game,
            rating=4,
            review_text="This is a test review."
        )

        # Assertions
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.game, self.game)
        self.assertEqual(review.rating, 4)

        # Test the update_game_rating signals
        self.game.refresh_from_db()
        self.assertEqual(self.game.average_rating, 4.0)

    def test_multiple_reviews_average_rating(self):
        # Create second user
        user2 = User.objects.create_user(username="testuser2", password="testpassword")

        # Create two reviews
        Review.objects.create(user=self.user, game=self.game, rating=5, review_text="Great!")
        Review.objects.create(user=user2, game=self.game, rating=3, review_text="Okay.")

        # Check average rating
        self.game.refresh_from_db()
        self.assertEqual(float(self.game.average_rating), 4.0)

