# Generated by Django 4.0.4 on 2022-05-05 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fifa_draft', '0014_team_max_players'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='max_players',
        ),
    ]
