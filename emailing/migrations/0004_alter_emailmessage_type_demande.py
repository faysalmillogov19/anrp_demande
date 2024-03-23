# Generated by Django 4.1 on 2023-12-07 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Demande", "0004_type_demande"),
        ("emailing", "0003_emailmessage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="emailmessage",
            name="type_demande",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="Demande.type_demande",
            ),
        ),
    ]