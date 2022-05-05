# Generated by Django 4.0.4 on 2022-05-04 16:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fifa_draft', '0005_group_number_of_players_alter_group_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='number_of_players',
            field=models.IntegerField(default=18, validators=[django.core.validators.MaxValueValidator(20), django.core.validators.MinValueValidator(14)]),
        ),
    ]