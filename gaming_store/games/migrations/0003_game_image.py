# Generated by Django 5.2.2 on 2025-06-25 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_remove_game_is_digital_game_release_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='games/'),
        ),
    ]
