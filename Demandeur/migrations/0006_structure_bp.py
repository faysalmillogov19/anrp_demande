# Generated by Django 4.1 on 2024-03-16 10:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Demandeur", "0005_demandeur_affect_structure"),
    ]

    operations = [
        migrations.AddField(
            model_name="structure",
            name="bp",
            field=models.CharField(max_length=100, null=True),
        ),
    ]