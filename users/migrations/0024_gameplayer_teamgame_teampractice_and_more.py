# Generated by Django 4.1.2 on 2023-02-20 14:58

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0023_accessrequestqueue"),
    ]

    operations = [
        migrations.CreateModel(
            name="GamePlayer",
            fields=[
                (
                    "GameTeamPlayerID",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("FirstName", models.CharField(default="", max_length=1000)),
                ("MiddleName", models.CharField(default="", max_length=1000)),
                ("LastName", models.CharField(default="", max_length=1000)),
                ("FullName", models.CharField(default="", max_length=1000)),
                ("JerseyNumber", models.CharField(default="", max_length=10)),
                (
                    "ThrowingHand",
                    models.CharField(
                        choices=[("R", "Right"), ("L", "Left"), ("B", "Both")],
                        default="R",
                        max_length=2000,
                    ),
                ),
                (
                    "BattingHand",
                    models.CharField(
                        choices=[("R", "Right"), ("L", "Left"), ("B", "Both")],
                        default="R",
                        max_length=2000,
                    ),
                ),
                ("BattingOrder", models.IntegerField(default=0)),
                (
                    "FieldPosition",
                    models.CharField(
                        choices=[
                            ("1B", "Firstbase"),
                            ("2B", "Secondbase"),
                            ("SS", "Shortstop"),
                            ("3B", "Thirdbase"),
                            ("LF", "Leftfield"),
                            ("CF", "Centerfield"),
                            ("RG", "Rightfield"),
                            ("DH", "Designatedhitter"),
                            ("P", "Pitcher"),
                            ("C", "Catcher"),
                        ],
                        default="DH",
                        max_length=2000,
                    ),
                ),
                ("PlayerID", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="TeamGame",
            fields=[
                ("TeamGameID", models.AutoField(primary_key=True, serialize=False)),
                (
                    "Start_Game_DateTime",
                    models.DateTimeField(default=datetime.datetime.today),
                ),
                (
                    "End_Game_DateTime",
                    models.DateTimeField(default=datetime.datetime.today),
                ),
                ("Location", models.CharField(default="", max_length=5000)),
                (
                    "AwayTeam",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="Away_Team",
                        to="users.team",
                    ),
                ),
                (
                    "HomeTeam",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="Home_Team",
                        to="users.team",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TeamPractice",
            fields=[
                ("TeamPracticeID", models.AutoField(primary_key=True, serialize=False)),
                ("FieldLocation", models.CharField(max_length=5000)),
                (
                    "StartGameDateTime",
                    models.DateTimeField(default=datetime.datetime.today),
                ),
                (
                    "EndGameDateTime",
                    models.DateTimeField(default=datetime.datetime.today),
                ),
                ("AdditionalInfo", models.TextField(max_length=8000)),
                (
                    "AssignedTeam",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.team"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TeamPitcherStatTotal",
            fields=[
                (
                    "PitcherGameStatID",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("InningsPitch", models.IntegerField(default=0)),
                ("Hits", models.IntegerField(default=0)),
                ("Runs", models.IntegerField(default=0)),
                ("EarnRuns", models.IntegerField(default=0)),
                ("BaseOnBalls", models.IntegerField(default=0)),
                ("StrikeOuts", models.IntegerField(default=0)),
                ("BattersFaced", models.IntegerField(default=0)),
                ("EarnRunAverage", models.IntegerField(default=0)),
                (
                    "AssignedGame",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.teamgame"
                    ),
                ),
                (
                    "AssignedTeam",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.team"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TeamBatterStatTotal",
            fields=[
                (
                    "TeamBatterStatTotalID",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("AtBats", models.IntegerField(default=0)),
                ("Runs", models.IntegerField(default=0)),
                ("Hits", models.IntegerField(default=0)),
                ("RBI", models.IntegerField(default=0)),
                ("BaseOnBalls", models.IntegerField(default=0)),
                ("StrikeOuts", models.IntegerField(default=0)),
                ("BattingAverage", models.IntegerField(default=0)),
                ("OBP", models.IntegerField(default=0)),
                (
                    "AssignedGame",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.teamgame"
                    ),
                ),
                (
                    "AssignedTeam",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.team"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PitcherGameStat",
            fields=[
                (
                    "PitcherGameStatID",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("InningsPitch", models.IntegerField(default=0)),
                ("Hits", models.IntegerField(default=0)),
                ("Runs", models.IntegerField(default=0)),
                ("EarnRuns", models.IntegerField(default=0)),
                ("BaseOnBalls", models.IntegerField(default=0)),
                ("StrikeOuts", models.IntegerField(default=0)),
                ("BattersFaced", models.IntegerField(default=0)),
                ("EarnRunAverage", models.IntegerField(default=0)),
                ("Loss", models.BooleanField(default=False)),
                ("Won", models.BooleanField(default=False)),
                (
                    "AssignedPlayer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.gameplayer",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="gameplayer",
            name="AssignedGame",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="users.teamgame"
            ),
        ),
        migrations.AddField(
            model_name="gameplayer",
            name="AssignedTeam",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="users.team"
            ),
        ),
        migrations.CreateModel(
            name="BatterGameStat",
            fields=[
                (
                    "BatterGameStatID",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("Position", models.CharField(max_length=40)),
                ("AtBats", models.IntegerField(default=0)),
                ("Runs", models.IntegerField(default=0)),
                ("Hits", models.IntegerField(default=0)),
                ("RBI", models.IntegerField(default=0)),
                ("BaseOnBalls", models.IntegerField(default=0)),
                ("StrikeOuts", models.IntegerField(default=0)),
                ("BattingAverage", models.IntegerField(default=0)),
                ("OBP", models.IntegerField(default=0)),
                (
                    "AssignedPlayer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.gameplayer",
                    ),
                ),
            ],
        ),
    ]
