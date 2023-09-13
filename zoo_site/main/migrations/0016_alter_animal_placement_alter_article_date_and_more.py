# Generated by Django 4.2.4 on 2023-09-13 20:25

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_coupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='placement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='animals', to='main.placement'),
        ),
        migrations.AlterField(
            model_name='article',
            name='date',
            field=models.DateField(default=datetime.date(2023, 9, 13)),
        ),
        migrations.AlterField(
            model_name='question',
            name='date',
            field=models.DateField(default=datetime.date(2023, 9, 13)),
        ),
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateField(default=datetime.date(2023, 9, 13)),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0, message='The rating cannot be < 0'), django.core.validators.MaxValueValidator(10, message='The rating cannot be > 0')]),
        ),
    ]