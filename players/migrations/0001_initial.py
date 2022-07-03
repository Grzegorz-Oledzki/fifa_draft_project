# Generated by Django 4.0.4 on 2022-07-02 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Player",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sofifa_id",
                    models.IntegerField(default=False, verbose_name="sofifa_id"),
                ),
                (
                    "player_url",
                    models.CharField(
                        default=False, max_length=150, verbose_name="player_url"
                    ),
                ),
                (
                    "short_name",
                    models.CharField(
                        default=False, max_length=50, verbose_name="short_name"
                    ),
                ),
                (
                    "player_positions",
                    models.CharField(
                        default=False,
                        max_length=15,
                        null=True,
                        verbose_name="player_positions",
                    ),
                ),
                ("overall", models.IntegerField(null=True, verbose_name="overall")),
                ("age", models.IntegerField(null=True, verbose_name="age")),
                ("height_cm", models.IntegerField(null=True, verbose_name="height_cm")),
                ("weight_kg", models.IntegerField(null=True, verbose_name="weight_kg")),
                (
                    "club_name",
                    models.CharField(
                        default=False,
                        max_length=50,
                        null=True,
                        verbose_name="club_name",
                    ),
                ),
                (
                    "preferred_foot",
                    models.CharField(
                        default=False,
                        max_length=6,
                        null=True,
                        verbose_name="preferred_foot",
                    ),
                ),
                ("weak_foot", models.IntegerField(null=True, verbose_name="weak_foot")),
                (
                    "skill_moves",
                    models.IntegerField(null=True, verbose_name="skill_moves"),
                ),
                (
                    "work_rate",
                    models.CharField(
                        default=False,
                        max_length=50,
                        null=True,
                        verbose_name="work_rate",
                    ),
                ),
                ("pace", models.IntegerField(null=True, verbose_name="pace")),
                ("shooting", models.IntegerField(null=True, verbose_name="shooting")),
                ("passing", models.IntegerField(null=True, verbose_name="passing")),
                ("dribbling", models.IntegerField(null=True, verbose_name="dribbling")),
                ("defending", models.IntegerField(null=True, verbose_name="defending")),
                ("physic", models.IntegerField(null=True, verbose_name="physic")),
                (
                    "player_face_url",
                    models.CharField(
                        default=False,
                        max_length=200,
                        null=True,
                        verbose_name="player_face_url",
                    ),
                ),
                (
                    "club_logo_url",
                    models.CharField(
                        default=False,
                        max_length=200,
                        null=True,
                        verbose_name="club_logo_url",
                    ),
                ),
                (
                    "nation_flag_url",
                    models.CharField(
                        default=False,
                        max_length=200,
                        null=True,
                        verbose_name="nation_flag_url",
                    ),
                ),
            ],
        ),
    ]
