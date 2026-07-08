from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    USER_TYPES = [
        ("CU", "customer"),
        ("CS", "customer service"),
    ]

    display_name = models.CharField(max_length=50)
    biography = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        default="profile_pictures/Profile-PlaceHolder.png",
        blank=True,
        null=True,
    )
    user_type = models.CharField(
        max_length=2,
        choices=USER_TYPES,
        default="CU",
    )

    REQUIRED_FIELDS = [
        "display_name",
        "email",
    ]

    def is_customer_service(self):
        return self.user_type == "CS"

    def __str__(self):
        return self.display_name + " (" + self.username + ")"
