# Generated by Django 4.1 on 2024-01-06 13:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ASI", "0011_nature_impression_asi_alter_asi_nature_impression"),
    ]

    operations = [
        migrations.AddField(
            model_name="asi",
            name="note_stupefiant",
            field=models.TextField(null=True),
        ),
    ]
