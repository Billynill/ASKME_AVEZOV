# Generated by Django 4.2.18 on 2025-01-20 22:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_rename_name_tag_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='title',
            new_name='name',
        ),
    ]
