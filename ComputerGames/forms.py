from django import forms
from .models import Game, GameImage


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = [
            "name",
            "description",
            "game_type",
            "genre",
            "fsk",
            "price",
            "operation_system",
        ]

        widgets = {
            "game_type": forms.Select(choices=Game.GAMETYPES),
            "genre": forms.Select(choices=Game.GENRES),
            "fsk": forms.Select(choices=Game.FSK),
            "operation_system": forms.Select(choices=Game.OPERATIONSYSTEMS),
            "description": forms.Textarea(attrs={"rows": 5}),
        }


class GameImageForm(forms.ModelForm):
    class Meta:
        model = GameImage
        fields = ["image"]