# Generated by Django 4.0.4 on 2022-05-09 19:24

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fifa_draft', '0004_alter_group_featured_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Formation',
            fields=[
                ('formation', models.CharField(choices=[('4–4–2', 'First'), ('4–3–3', 'Second'), ('4–1–2-1-2', 'Third'), ('4–4–1–1', 'Fourth'), ('4–3–2–1', 'Fifth'), ('4-2-3-1', 'Sixth'), ('3–4–3', 'Seventh'), ('5–3–2', 'Eighth')], default='4–4–2', max_length=10)),
                ('description', models.TextField(blank=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fifa_draft.team')),
            ],
        ),
    ]
