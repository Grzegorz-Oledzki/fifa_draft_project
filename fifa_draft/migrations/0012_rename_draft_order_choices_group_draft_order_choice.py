# Generated by Django 4.0.4 on 2022-05-05 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fifa_draft', '0011_group_draft_order_choices'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='draft_order_choices',
            new_name='draft_order_choice',
        ),
    ]
