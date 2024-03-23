# Generated by Django 4.1 on 2023-12-18 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Demande", "0007_signataire"),
        ("ADI", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="adi",
            name="nature_impression",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="Demande.nature_impression",
            ),
        ),
    ]
