from django.db import models
from django.conf import settings

# Create your models here.

class ComputerGame(models.Model):

    GENRES = [
        ('action', 'Action'),
        ('adventure', 'Adventure'),
        ('rpg', 'RPG'),
        ('strategy', 'Strategy'),
        ('sports', 'Sports'),
        ('puzzle', 'Puzzle'),
        ('simulation', 'Simulation'),
        ("fps", "First-Person Shooter"),
        ("mmorpg", "Massively Multiplayer Online Role Playing Game"),
        ("fighter", "Fighting Game"),
        ("platfomer", "Platformer/Jump And Run"),
    ]

    FSK = [
        (0, "ab 0"),
        (6, "ab 6"),
        (12, "ab 12"),
        (16, "ab 16"),
        (18, "ab 18"),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.CharField(max_length=50, choices=GENRES)
    fsk = models.IntegerField(choices=FSK, default=0)
    developer = models.CharField(max_length=100)
    release_date = models.DateField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

