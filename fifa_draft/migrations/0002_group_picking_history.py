# Generated by Django 4.0.4 on 2022-07-04 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fifa_draft", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="group",
            name="picking_history",
            field=models.CharField(blank=True, max_length=10000000, null=True),
        ),
    ]
