# Generated by Django 4.1 on 2024-01-06 01:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("emailing", "0006_emailmessage_modif_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="emailmessage",
            name="duree",
            field=models.TextField(null=True),
        ),
    ]