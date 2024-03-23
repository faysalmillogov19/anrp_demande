# Generated by Django 4.1 on 2023-12-17 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("ASI", "0010_asi_nature_impression"),
    ]

    operations = [
        migrations.CreateModel(
            name="Nature_impression_asi",
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
                ("libelle", models.CharField(max_length=25)),
            ],
            options={
                "verbose_name": "demandeur",
                "verbose_name_plural": "demandeurs",
            },
        ),
        migrations.AlterField(
            model_name="asi",
            name="nature_impression",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="ASI.nature_impression_asi",
            ),
        ),
    ]