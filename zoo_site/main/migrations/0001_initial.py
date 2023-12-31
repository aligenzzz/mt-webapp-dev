# Generated by Django 4.2.1 on 2023-05-18 19:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnimalClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Fodder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Placement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('name', models.CharField(max_length=30)),
                ('basin', models.BooleanField()),
                ('area', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Staffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.post')),
            ],
        ),
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('admission_date', models.DateField(blank=True, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('image', models.ImageField(upload_to='')),
                ('info', models.TextField()),
                ('daily_feed', models.FloatField()),
                ('animal_class', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.animalclass')),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.country')),
                ('fodder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.fodder')),
                ('placement', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='animals', to='main.placement')),
                ('species', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.species')),
                ('staffer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='animals', to='main.staffer')),
            ],
            options={
                'ordering': ['admission_date'],
            },
        ),
    ]
