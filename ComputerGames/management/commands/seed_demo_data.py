from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from ComputerGames.models import Game


class Command(BaseCommand):
    help = "Create sample users and games for local development."

    def handle(self, *args, **options):
        User = get_user_model()

        users = [
            {
                "username": "alice",
                "email": "alice@example.com",
                "display_name": "Alice",
                "password": "Test1234!",
                "user_type": "CU",
            },
            {
                "username": "bob",
                "email": "bob@example.com",
                "display_name": "Bob",
                "password": "Test1234!",
                "user_type": "CU",
            },
            {
                "username": "carol",
                "email": "carol@example.com",
                "display_name": "Carol",
                "password": "Test1234!",
                "user_type": "CU",
            },
        ]

        created_users = []
        for user_data in users:
            user, created = User.objects.get_or_create(
                username=user_data["username"],
                defaults={
                    "email": user_data["email"],
                    "display_name": user_data["display_name"],
                    "user_type": user_data["user_type"],
                },
            )
            user.set_password(user_data["password"])
            user.save()
            created_users.append(user)

        game_names = [
            "Astral Drift",
            "Neon Frontier",
            "Shadow Vault",
            "Crystal Rune",
            "Midnight Circuit",
            "Pixel Harbor",
            "Stormborn Legends",
            "Echoes of Ember",
            "Frostbite Arena",
            "Solaris Quest",
            "Arcade Dynasty",
            "Iron Harbor",
            "Velvet Mechanics",
            "Cobalt Frontier",
            "Moonlit Heist",
            "Raven Protocol",
            "Titanic Echo",
            "Wanderlight",
            "Ghost Relay",
            "Lunar Breakers",
            "Nova Tactics",
            "Chrono Forge",
            "Deepwater Odyssey",
            "Radiant Clash",
            "Velocirunner",
            "Silent Meridian",
            "Dragon Keep",
            "Skyline Overdrive",
            "Aurora Protocol",
            "Evergreen Wars",
        ]

        game_types = ["PH", "DI"]
        genres = ["FP", "RP", "PU", "SP", "TA", "AD", "SI", "TT"]
        fsk_values = [0, 6, 12, 16, 18]
        operation_systems = ["W", "L", "M", "X", "P"]

        for index, name in enumerate(game_names, start=1):
            if Game.objects.filter(name=name).exists():
                continue

            game = Game.objects.create(
                name=name,
                description=f"Sample description for {name}.",
                game_type=game_types[index % len(game_types)],
                genre=genres[index % len(genres)],
                fsk=fsk_values[(index - 1) % len(fsk_values)],
                price=Decimal(str(9 + (index % 10) + (index % 3) * 0.5)),
                operation_system=operation_systems[
                    (index - 1) % len(operation_systems)
                ],
            )
            if created_users:
                game.owners.add(created_users[(index - 1) % len(created_users)])

        self.stdout.write(self.style.SUCCESS("Demo data seeding completed."))
