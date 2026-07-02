from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import MyUser


class MyUserAdmin(UserAdmin):
    fieldsets = tuple(UserAdmin.fieldsets or ()) + (
        (
            "Additional information",
            {
                "fields": (
                    "display_name",
                    "biography",
                    "profile_picture",
                    "user_type",
                ),
            },
        ),
    )

    add_fieldsets = tuple(UserAdmin.add_fieldsets or ()) + (
        (
            "Additional information",
            {
                "fields": (
                    "display_name",
                    "email",
                    "biography",
                    "profile_picture",
                    "user_type",
                ),
            },
        ),
    )

    list_display = (
        "username",
        "display_name",
        "email",
        "user_type",
        "is_staff",
        "is_active",
    )


admin.site.register(MyUser, MyUserAdmin)
