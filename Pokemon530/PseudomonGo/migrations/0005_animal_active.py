# Generated by Django 4.0.3 on 2022-05-13 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PseudomonGo', '0004_remove_move_atk_multiplier_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
