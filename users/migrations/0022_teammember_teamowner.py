# Generated by Django 4.1.2 on 2023-02-17 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0021_remove_teamcoach_role_team_currentseason_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="teammember",
            name="TeamOwner",
            field=models.BooleanField(default=False),
        ),
    ]