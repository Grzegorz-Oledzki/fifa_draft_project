# Generated by Django 4.0.4 on 2022-05-30 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fifa_draft', '0002_alter_profile_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='team',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]