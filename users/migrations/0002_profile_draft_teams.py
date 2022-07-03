# Generated by Django 4.0.4 on 2022-07-02 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fifa_draft", "0001_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="draft_teams",
            field=models.ManyToManyField(
                blank=True, related_name="draft_teams", to="fifa_draft.team"
            ),
        ),
    ]
