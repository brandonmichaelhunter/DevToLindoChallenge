# Generated by Django 4.1.2 on 2023-02-11 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_remove_profile_usertype_delete_usertype_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="team",
            old_name="SecondPhone",
            new_name="SecondaryPhone",
        ),
        migrations.AddField(
            model_name="team",
            name="TeamLogo",
            field=models.ImageField(default="default.jpg", upload_to="team_logos"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="BattingHand",
            field=models.CharField(
                choices=[("R", "Right"), ("L", "Left"), ("B", "Both")],
                default="R",
                max_length=2000,
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="ShootingHand",
            field=models.CharField(
                choices=[("R", "Right"), ("L", "Left"), ("B", "Both")],
                default="R",
                max_length=2000,
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="ThrowingHand",
            field=models.CharField(
                choices=[("R", "Right"), ("L", "Left"), ("B", "Both")],
                default="R",
                max_length=2000,
            ),
        ),
    ]
