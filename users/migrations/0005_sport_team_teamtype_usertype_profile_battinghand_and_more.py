# Generated by Django 4.1.2 on 2023-02-10 00:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("users", "0004_profile_bio"),
    ]

    operations = [
        migrations.CreateModel(
            name="Sport",
            fields=[
                ("SportID", models.AutoField(primary_key=True, serialize=False)),
                ("Name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Team",
            fields=[
                ("TeamID", models.AutoField(primary_key=True, serialize=False)),
                ("TeamName", models.CharField(max_length=100)),
                ("PrimaryEmail", models.EmailField(max_length=254, unique=True)),
                ("SecondaryEmail", models.EmailField(max_length=254, null=True)),
                ("PrimaryPhone", models.CharField(max_length=12, null=True)),
                ("SecondPhone", models.CharField(max_length=12, null=True)),
                ("City", models.CharField(max_length=2000, null=True)),
                ("State", models.CharField(max_length=2000, null=True)),
                ("Zip", models.CharField(max_length=2000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="TeamType",
            fields=[
                ("TeamTypeID", models.AutoField(primary_key=True, serialize=False)),
                ("Type", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="UserType",
            fields=[
                ("UserTypeID", models.AutoField(primary_key=True, serialize=False)),
                ("Type", models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name="profile",
            name="BattingHand",
            field=models.CharField(
                choices=[("R", "Right"), ("L", "Left")], default="R", max_length=2000
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="BirthDate",
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="City",
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="PrimaryEmail",
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="PrimaryPhone",
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="SecondPhone",
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="SecondaryEmail",
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="ShootingHand",
            field=models.CharField(
                choices=[("R", "Right"), ("L", "Left")], default="R", max_length=2000
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="State",
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="ThrowingHand",
            field=models.CharField(
                choices=[("R", "Right"), ("L", "Left")], default="R", max_length=2000
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="YearInSchool",
            field=models.CharField(
                choices=[
                    ("FR", "Freshman"),
                    ("SO", "Sophomore"),
                    ("JR", "Junior"),
                    ("SR", "Senior"),
                    ("GR", "Graduate"),
                ],
                default="FR",
                max_length=200,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="Zip",
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.CreateModel(
            name="UserRelationship",
            fields=[
                (
                    "UserRelationshipID",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                (
                    "User1",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="Parent",
                        to="users.profile",
                    ),
                ),
                (
                    "User2",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="Child",
                        to="users.profile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TeamRoster",
            fields=[
                ("TeamPlayerID", models.AutoField(primary_key=True, serialize=False)),
                ("ActiveMember", models.BooleanField(default=False)),
                (
                    "Player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.profile"
                    ),
                ),
                (
                    "Role",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="auth.group"
                    ),
                ),
                (
                    "Team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.team"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TeamCoach",
            fields=[
                ("TeamCoachID", models.AutoField(primary_key=True, serialize=False)),
                ("IsHeadCoach", models.BooleanField(default=False)),
                (
                    "Coach",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.profile"
                    ),
                ),
                (
                    "Role",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="auth.group"
                    ),
                ),
                (
                    "Team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.team"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="team",
            name="SportType",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="users.teamtype"
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="UserType",
            field=models.ManyToManyField(to="users.usertype"),
        ),
    ]
