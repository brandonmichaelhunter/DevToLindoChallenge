# Generated by Django 4.1.2 on 2023-02-16 19:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("users", "0017_teamroster_fullname_teammedia_playermedia"),
    ]

    operations = [
 
        migrations.RemoveField(
            model_name="teamroster",
            name="Player",
        ),
        migrations.RemoveField(
            model_name="teamroster",
            name="Role",
        ),
        migrations.AddField(
            model_name="teamroster",
            name="BattingHand",
            field=models.CharField(
                choices=[("R", "Right"), ("L", "Left"), ("B", "Both")],
                default="R",
                max_length=2000,
            ),
        ),
        migrations.AddField(
            model_name="teamroster",
            name="FirstName",
            field=models.CharField(default="", max_length=1000),
        ),
        migrations.AddField(
            model_name="teamroster",
            name="JerseyNumber",
            field=models.CharField(default="", max_length=10),
        ),
        migrations.AddField(
            model_name="teamroster",
            name="LastName",
            field=models.CharField(default="", max_length=1000),
        ),
        migrations.AddField(
            model_name="teamroster",
            name="MiddleName",
            field=models.CharField(default="", max_length=1000),
        ),
        migrations.AddField(
            model_name="teamroster",
            name="ProfileImage",
            field=models.ImageField(
                default="default.jpg", upload_to="player_profile_images"
            ),
        ),
        migrations.AddField(
            model_name="teamroster",
            name="ThrowingHand",
            field=models.CharField(
                choices=[("R", "Right"), ("L", "Left"), ("B", "Both")],
                default="R",
                max_length=2000,
            ),
        ),
        migrations.CreateModel(
            name="TeamFanInviteRequest",
            fields=[
                ("DateCreated", models.DateField(auto_created=True)),
                (
                    "TeamFanInviteRequest",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("EmailContact", models.CharField(max_length=1000)),
                (
                    "RequestStatus",
                    models.CharField(
                        choices=[
                            ("OPEN", "Open"),
                            ("PENDING", "Pending"),
                            ("APPROVED", "Approved"),
                            ("REJECTED", "Rejected"),
                        ],
                        default="OPEN",
                        max_length=2000,
                    ),
                ),
                ("DateApprovedRejected", models.DateField(auto_now=True)),
                ("InviteCode", models.CharField(default="", max_length=2000)),
                (
                    "AssignedTeam",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.team",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TeamFan",
            fields=[
                ("TeamFanID", models.AutoField(primary_key=True, serialize=False)),
                (
                    "AssignedTeam",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.team"
                    ),
                ),
                (
                    "FanUser",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PlayerContact",
            fields=[
                (
                    "PlayerFamilyContactID",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                (
                    "ContactType",
                    models.CharField(
                        choices=[
                            ("Family", "Family"),
                            ("Emergency", "Emergency"),
                            ("Both", "Both"),
                        ],
                        default="Family",
                        max_length=2000,
                    ),
                ),
                (
                    "FamilyMember",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.teamfan"
                    ),
                ),
                (
                    "Player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.teamroster",
                    ),
                ),
            ],
        ),
    ]
