# Generated by Django 5.2 on 2025-06-12 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0012_alter_user_image_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="image_profile",
            field=models.ImageField(blank=True, null=True, upload_to="profile_images"),
        ),
    ]
