# Generated by Django 4.0.4 on 2022-05-09 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fifa_draft', '0005_team_description_team_formation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='formation',
            field=models.CharField(choices=[(0, 'Low'), (1, 'Normal'), (2, 'High')], default=0, max_length=10),
        ),
    ]