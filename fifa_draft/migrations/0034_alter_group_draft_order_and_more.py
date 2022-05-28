# Generated by Django 4.0.4 on 2022-05-28 17:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fifa_draft', '0033_alter_group_draft_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='draft_order',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='number_of_players',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(14), django.core.validators.MaxValueValidator(20)]),
        ),
    ]
