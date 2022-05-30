# Generated by Django 4.0.4 on 2022-05-30 14:56

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import fifa_draft.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('name', models.CharField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('featured_image', models.ImageField(blank=True, null=True, upload_to='group_images/')),
                ('password', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('number_of_players', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(14), django.core.validators.MaxValueValidator(20)])),
                ('draft_order_choice', models.CharField(choices=[('Serpentine', 'Serpentine'), ('Fixed', 'Fixed')], default='Serpentine', max_length=10)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('draft_order', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sofifa_id', models.IntegerField(default=False, verbose_name='sofifa_id')),
                ('player_url', models.CharField(default=False, max_length=150, verbose_name='player_url')),
                ('short_name', models.CharField(default=False, max_length=50, verbose_name='short_name')),
                ('player_positions', models.CharField(default=False, max_length=15, null=True, verbose_name='player_positions')),
                ('overall', models.IntegerField(null=True, verbose_name='overall')),
                ('age', models.IntegerField(null=True, verbose_name='age')),
                ('height_cm', models.IntegerField(null=True, verbose_name='height_cm')),
                ('weight_kg', models.IntegerField(null=True, verbose_name='weight_kg')),
                ('club_name', models.CharField(default=False, max_length=50, null=True, verbose_name='club_name')),
                ('preferred_foot', models.CharField(default=False, max_length=6, null=True, verbose_name='preferred_foot')),
                ('weak_foot', models.IntegerField(null=True, verbose_name='weak_foot')),
                ('skill_moves', models.IntegerField(null=True, verbose_name='skill_moves')),
                ('work_rate', models.CharField(default=False, max_length=50, null=True, verbose_name='work_rate')),
                ('pace', models.IntegerField(null=True, verbose_name='pace')),
                ('shooting', models.IntegerField(null=True, verbose_name='shooting')),
                ('passing', models.IntegerField(null=True, verbose_name='passing')),
                ('dribbling', models.IntegerField(null=True, verbose_name='dribbling')),
                ('defending', models.IntegerField(null=True, verbose_name='defending')),
                ('physic', models.IntegerField(null=True, verbose_name='physic')),
                ('player_face_url', models.CharField(default=False, max_length=200, null=True, verbose_name='player_face_url')),
                ('club_logo_url', models.CharField(default=False, max_length=200, null=True, verbose_name='club_logo_url')),
                ('nation_flag_url', models.CharField(default=False, max_length=200, null=True, verbose_name='nation_flag_url')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('username', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('location', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=50, null=True)),
                ('short_intro', models.CharField(blank=True, max_length=250, null=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_images/')),
                ('social_github', models.CharField(blank=True, max_length=200, null=True)),
                ('social_twitter', models.CharField(blank=True, max_length=200, null=True)),
                ('social_linkedin', models.CharField(blank=True, max_length=200, null=True)),
                ('social_youtube', models.CharField(blank=True, max_length=200, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('name', models.CharField(max_length=20)),
                ('featured_image', models.ImageField(blank=True, null=True, upload_to='team_images/')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('group_password', models.CharField(max_length=50)),
                ('max_players', models.PositiveIntegerField(default=14)),
                ('formation', models.CharField(choices=[('4–4–2', '4–4–2'), ('4–3–3', '4–3–3'), ('4–1–2-1-2', '4–1–2-1-2'), ('4–4–1–1', '4–4–1–1'), ('4–3–2–1', '4–3–2–1'), ('4-2-3-1', '4-2-3-1'), ('3–4–3', '3–4–3'), ('5–3–2', '5–3–2')], default=('4–3–3', '4–3–3'), max_length=10)),
                ('description', models.TextField(blank=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('belongs_group', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='fifa_draft.group')),
                ('owner', models.ForeignKey(default=fifa_draft.models.Profile, on_delete=django.db.models.deletion.CASCADE, to='fifa_draft.profile')),
                ('team_players', models.ManyToManyField(blank=True, related_name='team_players', to='fifa_draft.player')),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='draft_teams',
            field=models.ManyToManyField(blank=True, related_name='draft_teams', to='fifa_draft.team'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='group',
            name='group_players',
            field=models.ManyToManyField(blank=True, related_name='group_players', to='fifa_draft.player'),
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(blank=True, default=fifa_draft.models.Profile, related_name='members', to='fifa_draft.profile'),
        ),
        migrations.AddField(
            model_name='group',
            name='owner',
            field=models.ForeignKey(db_constraint=False, default=fifa_draft.models.Profile, on_delete=django.db.models.deletion.CASCADE, to='fifa_draft.profile'),
        ),
        migrations.AddField(
            model_name='group',
            name='picking_person',
            field=models.ManyToManyField(blank=True, default=fifa_draft.models.Profile, related_name='picking_person', to='fifa_draft.profile'),
        ),
        migrations.AddField(
            model_name='group',
            name='teams',
            field=models.ManyToManyField(blank=True, related_name='teams', to='fifa_draft.team'),
        ),
    ]
