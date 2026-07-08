from django.db import migrations, models


DEFAULT_PROFILE_PICTURE = "profile_pictures/Profile-PlaceHolder.png"


def set_default_profile_picture(apps, schema_editor):
    MyUser = apps.get_model("Useradmin", "MyUser")
    MyUser.objects.filter(profile_picture__isnull=True).update(
        profile_picture=DEFAULT_PROFILE_PICTURE
    )
    MyUser.objects.filter(profile_picture="").update(
        profile_picture=DEFAULT_PROFILE_PICTURE
    )


class Migration(migrations.Migration):

    dependencies = [
        ("Useradmin", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="myuser",
            name="profile_picture",
            field=models.ImageField(
                blank=True,
                default=DEFAULT_PROFILE_PICTURE,
                null=True,
                upload_to="profile_pictures/",
            ),
        ),
        migrations.RunPython(
            set_default_profile_picture,
            migrations.RunPython.noop,
        ),
    ]
