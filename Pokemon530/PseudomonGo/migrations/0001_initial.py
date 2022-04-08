# Generated by Django 4.0.3 on 2022-04-08 02:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('level', models.IntegerField()),
                ('num_animals', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Robot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=25)),
                ('health', models.FloatField()),
                ('attack', models.FloatField()),
                ('defense', models.FloatField()),
                ('speed', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('animal_name', models.CharField(max_length=50)),
                ('animal_type', models.CharField(max_length=50)),
                ('animal_species', models.CharField(max_length=50)),
                ('photograph_path', models.CharField(max_length=100)),
                ('health', models.FloatField()),
                ('attack', models.FloatField()),
                ('defense', models.FloatField()),
                ('speed', models.FloatField()),
                ('owner_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PseudomonGo.player')),
            ],
        ),
    ]
