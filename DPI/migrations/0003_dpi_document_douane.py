# Generated by Django 4.1 on 2024-01-05 12:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("DPI", "0002_dpi_nature_impression"),
    ]

    operations = [
        migrations.AddField(
            model_name="dpi",
            name="document_douane",
            field=models.TextField(null=True),
        ),
    ]