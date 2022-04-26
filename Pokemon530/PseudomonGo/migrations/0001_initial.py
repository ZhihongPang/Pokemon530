# Generated by Django 4.0.3 on 2022-04-26 04:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_google_maps.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entity_name', models.CharField(max_length=50)),
                ('entity_desc', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='EntityClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=50)),
                ('class_description', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=25)),
                ('item_rarity', models.CharField(choices=[('C', 'Common'), ('U', 'Uncommon'), ('R', 'Rare'), ('E', 'Epic'), ('L', 'Legendary')], default='C', max_length=2)),
                ('healing', models.IntegerField(default=0)),
                ('stat_buffed', models.CharField(choices=[('AT', 'Attack'), ('D', 'Defense'), ('S', 'Speed'), ('N', 'None'), ('AL', 'ALL')], default='N', max_length=4)),
                ('buff_multiplier', models.IntegerField(default=1)),
                ('status_cured', models.CharField(default='none', max_length=25)),
                ('item_type', models.CharField(max_length=25)),
                ('item_description', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', django_google_maps.fields.AddressField(max_length=200)),
                ('geolocation', django_google_maps.fields.GeoLocationField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='StatusCondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PseudomonGo.item')),
                ('player_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experience', models.IntegerField(default=0)),
                ('level', models.IntegerField(default=1)),
                ('num_animals', models.IntegerField(default=0)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('move_name', models.CharField(max_length=50)),
                ('base_damage', models.IntegerField(default=0)),
                ('atk_multiplier', models.FloatField(default=1)),
                ('def_multiplier', models.FloatField(default=1)),
                ('spd_multiplier', models.FloatField(default=1)),
                ('move_description', models.CharField(max_length=150)),
                ('move_type', models.CharField(choices=[('A', 'Attack'), ('S', 'Status')], default='A', max_length=2)),
                ('target', models.CharField(choices=[('S', 'Self'), ('O', 'Opponent')], default='O', max_length=2)),
                ('entity', models.ManyToManyField(to='PseudomonGo.entity')),
                ('entity_class', models.ManyToManyField(to='PseudomonGo.entityclass')),
                ('status_inflicted', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PseudomonGo.statuscondition')),
            ],
        ),
        migrations.AddField(
            model_name='entity',
            name='entity_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PseudomonGo.entityclass'),
        ),
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('animal_name', models.CharField(max_length=50)),
                ('animal_description', models.TextField(max_length=500)),
                ('photo_path', models.FileField(null=True, upload_to='images/', verbose_name='')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
                ('health', models.IntegerField(default=100)),
                ('attack', models.IntegerField(default=1)),
                ('defense', models.IntegerField(default=1)),
                ('speed', models.IntegerField(default=1)),
                ('level', models.IntegerField(default=1)),
                ('experience', models.IntegerField(default=0)),
                ('animal_class', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='PseudomonGo.entityclass')),
                ('animal_species', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='PseudomonGo.entity')),
                ('player', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
