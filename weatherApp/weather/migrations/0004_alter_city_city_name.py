# Generated by Django 5.0.7 on 2024-07-17 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("weather", "0003_city_last_searched"),
    ]

    operations = [
        migrations.AlterField(
            model_name="city",
            name="city_name",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Название города"
            ),
        ),
    ]
