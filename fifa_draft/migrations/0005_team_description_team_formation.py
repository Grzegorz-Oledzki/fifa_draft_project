# Generated by Django 4.0.4 on 2022-05-09 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fifa_draft", "0004_alter_group_featured_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="team",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="team",
            name="formation",
            field=models.CharField(
                choices=[
                    ("4–4–2", "First"),
                    ("4–3–3", "Second"),
                    ("4–1–2-1-2", "Third"),
                    ("4–4–1–1", "Fourth"),
                    ("4–3–2–1", "Fifth"),
                    ("4-2-3-1", "Sixth"),
                    ("3–4–3", "Seventh"),
                    ("5–3–2", "Eighth"),
                ],
                default="4–4–2",
                max_length=10,
            ),
        ),
    ]
