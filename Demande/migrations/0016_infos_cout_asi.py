# Generated by Django 4.1 on 2024-02-01 09:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Demande", "0015_infos_mot_fin"),
    ]

    operations = [
        migrations.AddField(
            model_name="infos",
            name="cout_asi",
            field=models.IntegerField(default=0),
        ),
    ]