# Generated by Django 4.0.4 on 2022-05-04 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fifa_draft', '0003_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='members', to='fifa_draft.profile'),
        ),
    ]
