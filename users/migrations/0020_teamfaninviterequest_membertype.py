# Generated by Django 4.1.2 on 2023-02-17 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0019_remove_teamroster_activemember_teammember"),
    ]

    operations = [
        migrations.AddField(
            model_name="teamfaninviterequest",
            name="MemberType",
            field=models.CharField(
                choices=[("PARENT", "Parent"), ("COACH", "Coach")],
                default="PARENT",
                max_length=2000,
            ),
        ),
    ]
