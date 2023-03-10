# Generated by Django 4.1.2 on 2023-02-12 02:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0009_teamwebsite_teamwebsiteexternallink_teamdocument"),
    ]

    operations = [
        migrations.CreateModel(
            name="SiteStyle",
            fields=[
                ("SiteStyleID", models.AutoField(primary_key=True, serialize=False)),
                ("Style", models.CharField(max_length=1000)),
                ("Active", models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name="teamwebsite",
            name="BackgroundColor",
        ),
        migrations.AddField(
            model_name="teamwebsite",
            name="SiteTheme",
            field=models.ForeignKey(
                default="",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="SiteTheme",
                to="users.sitestyle",
            ),
        ),
    ]
