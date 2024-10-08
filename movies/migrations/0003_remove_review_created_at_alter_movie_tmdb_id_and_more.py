# Generated by Django 5.1 on 2024-09-02 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_movie_tmdb_id_review_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='created_at',
        ),
        migrations.AlterField(
            model_name='movie',
            name='tmdb_id',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveIntegerField(),
        ),
    ]
