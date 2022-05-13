# Generated by Django 4.0.3 on 2022-05-11 05:26

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
            name='Animal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('animal_name', models.CharField(max_length=50)),
                ('animal_description', models.TextField(max_length=500)),
                ('animal_location', models.CharField(max_length=50, verbose_name='Sighted Location')),
                ('photo_path', models.FileField(default=None, null=True, upload_to='images/', verbose_name='')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
                ('health', models.IntegerField(default=100)),
                ('attack', models.IntegerField(default=1)),
                ('defense', models.IntegerField(default=1)),
                ('speed', models.IntegerField(default=1)),
                ('level', models.IntegerField(default=1)),
                ('experience', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('attack', models.IntegerField(default=75)),
                ('defense', models.IntegerField(default=50)),
                ('health', models.IntegerField(default=100)),
                ('speed', models.IntegerField(default=50)),
                ('entity_desc', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='EntityClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=50)),
                ('class_description', models.CharField(max_length=500)),
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
                ('item_cost', models.IntegerField(default=0)),
                ('item_type', models.CharField(max_length=25)),
                ('item_description', models.CharField(max_length=500)),
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
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PseudomonGo.animal')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PseudomonGo.item')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experience', models.IntegerField(default=0)),
                ('level', models.IntegerField(default=1)),
                ('num_animals', models.IntegerField(default=0)),
                ('money', models.IntegerField(default=0)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('move_name', models.CharField(max_length=50)),
                ('infliction_chance', models.IntegerField(default=100)),
                ('accuracy', models.IntegerField(default=100)),
                ('base_damage', models.IntegerField(default=0)),
                ('atk_multiplier', models.FloatField(default=1)),
                ('def_multiplier', models.FloatField(default=1)),
                ('spd_multiplier', models.FloatField(default=1)),
                ('move_description', models.CharField(max_length=500)),
                ('move_type', models.CharField(choices=[('A', 'Attack'), ('S', 'Status')], default='A', max_length=2)),
                ('target', models.CharField(choices=[('S', 'Self'), ('O', 'Opponent')], default='O', max_length=2)),
                ('entity', models.ManyToManyField(to='PseudomonGo.entity')),
                ('entity_class', models.ManyToManyField(blank=True, default=None, to='PseudomonGo.entityclass')),
                ('status_inflicted', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='PseudomonGo.statuscondition')),
            ],
        ),
        migrations.AddField(
            model_name='entity',
            name='entity_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PseudomonGo.entityclass'),
        ),
        migrations.AddField(
            model_name='animal',
            name='animal_class',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='PseudomonGo.entityclass'),
        ),
        migrations.AddField(
            model_name='animal',
            name='animal_species',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='PseudomonGo.entity'),
        ),
        migrations.AddField(
            model_name='animal',
            name='move1',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='move1', to='PseudomonGo.move'),
        ),
        migrations.AddField(
            model_name='animal',
            name='move2',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='move2', to='PseudomonGo.move'),
        ),
        migrations.AddField(
            model_name='animal',
            name='move3',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='move3', to='PseudomonGo.move'),
        ),
        migrations.AddField(
            model_name='animal',
            name='move4',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='move4', to='PseudomonGo.move'),
        ),
        migrations.AddField(
            model_name='animal',
            name='player',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
