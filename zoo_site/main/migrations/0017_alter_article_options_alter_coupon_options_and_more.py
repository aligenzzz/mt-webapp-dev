# Generated by Django 4.2.4 on 2023-09-14 19:37

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_alter_animal_placement_alter_article_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-date', 'title'], 'verbose_name': 'Article', 'verbose_name_plural': 'Articles'},
        ),
        migrations.AlterModelOptions(
            name='coupon',
            options={'ordering': ['-discount', '-is_active'], 'verbose_name': 'Coupon', 'verbose_name_plural': 'Coupons'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['-date'], 'verbose_name': 'Question', 'verbose_name_plural': 'Questions'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-date'], 'verbose_name': 'Review', 'verbose_name_plural': 'Reviews'},
        ),
        migrations.AlterField(
            model_name='article',
            name='date',
            field=models.DateField(default=datetime.date(2023, 9, 14)),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='discount',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(10, message='The discount cannot be < 10'), django.core.validators.MaxValueValidator(100, message='The discount cannot be > 100')]),
        ),
        migrations.AlterField(
            model_name='question',
            name='date',
            field=models.DateField(default=datetime.date(2023, 9, 14)),
        ),
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateField(default=datetime.date(2023, 9, 14)),
        ),
    ]