# Generated by Django 4.0.4 on 2022-05-23 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fifa_draft', '0025_alter_group_name_alter_player_club_logo_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
