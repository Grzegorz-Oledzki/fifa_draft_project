# Generated by Django 4.0.4 on 2022-05-10 16:44

from django.db import migrations, models
import django.db.models.deletion
import fifa_draft.models


class Migration(migrations.Migration):

    dependencies = [
        ('fifa_draft', '0012_alter_group_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='owner',
            field=models.ForeignKey(default=fifa_draft.models.Profile, on_delete=django.db.models.deletion.CASCADE, to='fifa_draft.profile'),
        ),
    ]
