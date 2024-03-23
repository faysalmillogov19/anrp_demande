# Generated by Django 4.1 on 2024-02-15 06:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Demandeur", "0005_demandeur_affect_structure"),
        ("ASI", "0020_group_facture_created_at_group_facture_updated_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="group_facture",
            name="num_quittance",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="group_facture",
            name="structure",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="Demandeur.structure",
            ),
        ),
    ]