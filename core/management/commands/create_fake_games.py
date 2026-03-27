import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from core.models import Game, Genre, Platform

class Command(BaseCommand):
    help = 'Create fake games'

    def handle(self, *args, **kwargs):
        genres = ['Action', 'RPG', 'Shooter', 'Platformer', 'Simulation', 'Strategy']
        platforms = ['PC', 'PlayStation 5', 'Xbox Series X', 'Nintendo Switch']

        # Ensure genres and platforms exist
        genre_objs = []
        for g in genres:
            genre, _ = Genre.objects.get_or_create(name=g)
            genre_objs.append(genre)

        platform_objs = []
        for p in platforms:
            platform, _ = Platform.objects.get_or_create(name=p)
            platform_objs.append(platform)

        games_data = [
            ('Cosmic Destiny', 'Space Explorer', 'Galactic Studios'),
            ('Warrior\'s Path', 'Swords & Magic', 'Epic Games Corp'),
            ('City Builder Pro', 'Urban Development', 'SimCorp'),
            ('Speed Demons', 'Velocity Games', 'Fast Track Ltd'),
            ('Mystery Manor', 'Enigma Soft', 'Puzzle Masters'),
        ]

        games_created = 0
        for i, (title, dev, pub) in enumerate(games_data):
            title = f"{title} {random.randint(1, 99)}"
            release_date = date.today() - timedelta(days=random.randint(1, 3650))
            
            game, created = Game.objects.get_or_create(
                title=title,
                defaults={
                    'release_date': release_date,
                    'developer': dev,
                    'publisher': pub,
                    'description': f'This is a fake description for {title}. It is an amazing game that you will love playing.'
                }
            )
            
            if created:
                games_created += 1
                game.genres.add(*random.sample(genre_objs, random.randint(1, 3)))
                game.platforms.add(*random.sample(platform_objs, random.randint(1, 3)))

        self.stdout.write(self.style.SUCCESS(f'Successfully created {games_created} fake games'))
