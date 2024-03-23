# Generated by Django 4.1 on 2024-01-24 22:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Demandeur", "0004_structure_grossiste"),
    ]

    operations = [
        migrations.AddField(
            model_name="demandeur",
            name="affect_structure",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="Demandeur.structure",
            ),
        ),
    ]
