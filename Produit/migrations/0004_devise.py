# Generated by Django 4.1 on 2024-01-03 20:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Produit", "0003_produit_demande_stupefiant"),
    ]

    operations = [
        migrations.CreateModel(
            name="Devise",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("libelle", models.CharField(max_length=50)),
                ("symbole", models.CharField(max_length=50)),
            ],
        ),
    ]
