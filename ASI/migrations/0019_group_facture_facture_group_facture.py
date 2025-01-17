# Generated by Django 4.1 on 2024-02-15 04:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("ASI", "0018_rename_demande_facture_asi"),
    ]

    operations = [
        migrations.CreateModel(
            name="Group_facture",
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
                ("code", models.TextField(null=True)),
                ("cout", models.IntegerField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name="facture",
            name="group_facture",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="ASI.group_facture",
            ),
        ),
    ]
