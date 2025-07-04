# Generated by Django 5.2.2 on 2025-06-25 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_game_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='author',
            field=models.CharField(default='Unknown', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='game',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
        migrations.AlterField(
            model_name='game',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
