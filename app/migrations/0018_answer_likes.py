# Generated by Django 4.2.18 on 2025-01-22 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_post_dislikes'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
