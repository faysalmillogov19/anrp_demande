# Generated by Django 4.1 on 2023-12-14 12:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("ASE", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="ase",
            old_name="certicat_bonne_pratique",
            new_name="code_facture",
        ),
        migrations.RenameField(
            model_name="ase",
            old_name="certificat_analyse_prod",
            new_name="copie_asi",
        ),
        migrations.RemoveField(
            model_name="ase",
            name="certificat_atestation_don",
        ),
        migrations.RemoveField(
            model_name="ase",
            name="certificat_origine_prod",
        ),
    ]
