# Generated by Django 4.0.4 on 2022-05-06 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fifa_draft', '0003_remove_group_teams'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='teams',
            field=models.ManyToManyField(blank=True, related_name='teams', to='fifa_draft.profile'),
        ),
    ]
