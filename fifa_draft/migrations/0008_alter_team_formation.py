# Generated by Django 4.0.4 on 2022-05-09 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fifa_draft', '0007_alter_team_formation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='formation',
            field=models.CharField(choices=[(1, '4–4–2'), (2, '4–3–3'), (3, '4–1–2-1-2'), (4, '4–4–1–1'), (5, '4–3–2–1'), (6, '4-2-3-1'), (7, '3–4–3'), (8, '5–3–2')], default=(2, '4–3–3'), max_length=10),
        ),
    ]
