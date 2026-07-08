import random

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import MyUser


class MySignUpForm(UserCreationForm):

    class Meta:
        model = MyUser
        fields = (
            "display_name",
            "email",
            "biography",
            "profile_picture",
        )
        labels = {
            "display_name": _("Display name"),
            "email": _("Email address"),
            "biography": _("Biography"),
            "profile_picture": _("Profile picture"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True

    def save(self, commit=True):
        myuser = super().save(commit=False)
        myuser.username = self.create_account_name(myuser.display_name)

        if commit:
            myuser.save()

        return myuser

    @staticmethod
    def create_account_name(display_name):
        account_name_base = "".join(
            character for character in display_name if character.isalnum()
        )

        if not account_name_base:
            account_name_base = "user"

        first_number = random.randint(0, 9999)

        for offset in range(10000):
            number = (first_number + offset) % 10000
            account_name = account_name_base + f"{number:04d}"

            account_name_exists = MyUser.objects.filter(
                username__iexact=account_name
            ).exists()

            if not account_name_exists:
                return account_name

        raise ValueError(
            _("No free account name could be created for this display name.")
        )


class UserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = [
            "display_name",
            "email",
            "biography",
            "profile_picture",
        ]
        labels = {
            "display_name": _("Display name"),
            "email": _("Email address"),
            "biography": _("Biography"),
            "profile_picture": _("Profile picture"),
        }