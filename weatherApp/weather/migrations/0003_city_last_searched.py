# Generated by Django 5.0.7 on 2024-07-17 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "weather",
            "0002_remove_userprofile_is_active_alter_userprofile_email_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="city",
            name="last_searched",
            field=models.DateTimeField(
                auto_now=True, verbose_name="Время последнего поиска"
            ),
        ),
    ]
