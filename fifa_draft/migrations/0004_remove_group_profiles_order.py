# Generated by Django 4.0.4 on 2022-06-29 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fifa_draft', '0003_group_profiles_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='profiles_order',
        ),
    ]
