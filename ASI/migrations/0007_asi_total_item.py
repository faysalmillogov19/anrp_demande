# Generated by Django 4.1 on 2023-12-01 11:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ASI", "0006_rename_quantite_asi_nombre"),
    ]

    operations = [
        migrations.AddField(
            model_name="asi",
            name="total_item",
            field=models.IntegerField(null=True),
        ),
    ]
