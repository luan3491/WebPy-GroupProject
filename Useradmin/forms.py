import random

from django.contrib.auth.forms import UserCreationForm

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
            "Für diesen Anzeigenamen konnte kein freier Accountname erstellt werden."
        )
