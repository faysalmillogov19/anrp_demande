# Generated by Django 4.1 on 2024-01-06 01:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Demande", "0014_infos_arrete"),
    ]

    operations = [
        migrations.AddField(
            model_name="infos",
            name="mot_fin",
            field=models.TextField(null=True),
        ),
    ]