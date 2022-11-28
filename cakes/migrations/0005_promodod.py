# Generated by Django 3.2.7 on 2022-11-28 07:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cakes', '0004_auto_20221124_1445'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promodod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promocode', models.CharField(max_length=20, verbose_name='Промокод')),
                ('discount', models.IntegerField(validators=[django.core.validators.MaxValueValidator(100)], verbose_name='Скидка в процентах %')),
            ],
        ),
    ]