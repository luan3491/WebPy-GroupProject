from django import forms
from .models import Game, GameImage, Review
from django.utils.translation import gettext_lazy as _


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


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            "stars",
            "text",
        ]

        widgets = {
            "stars": forms.Select(choices=Review.STARS),
            "text": forms.Textarea(attrs={"rows": 5}),
        }


class GameSearchForm(forms.Form):
    search_text = forms.CharField(
        required=False,
        label=_("Search text"),
    )

    stars = forms.ChoiceField(
        required=False,
        label=_("Rating"),
        choices=[
            ("", _("All ratings")),
            ("1", _("1 Star and above")),
            ("2", _("2 Stars and above")),
            ("3", _("3 Stars and above")),
            ("4", _("4 Stars and above")),
            ("5", _("5 Stars")),
        ],
    )
