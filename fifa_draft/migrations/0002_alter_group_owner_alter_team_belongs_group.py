# Generated by Django 4.0.4 on 2022-05-05 14:58

from django.db import migrations, models
import django.db.models.deletion
import fifa_draft.models


class Migration(migrations.Migration):

    dependencies = [
        ('fifa_draft', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='owner',
            field=models.ForeignKey(db_constraint=False, default=fifa_draft.models.Profile, on_delete=django.db.models.deletion.CASCADE, to='fifa_draft.profile'),
        ),
        migrations.AlterField(
            model_name='team',
            name='belongs_group',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='fifa_draft.group'),
        ),
    ]
