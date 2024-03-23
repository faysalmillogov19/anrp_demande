# Generated by Django 4.1 on 2023-12-08 12:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ASI", "0007_asi_total_item"),
    ]

    operations = [
        migrations.AlterField(
            model_name="asi",
            name="certicat_bonne_pratique",
            field=models.FileField(null=True, upload_to="static/ASI/BP/"),
        ),
        migrations.AlterField(
            model_name="asi",
            name="certificat_analyse_prod",
            field=models.FileField(null=True, upload_to="static/ASI/AP/"),
        ),
        migrations.AlterField(
            model_name="asi",
            name="certificat_atestation_don",
            field=models.FileField(null=True, upload_to="static/ASI/AD/"),
        ),
        migrations.AlterField(
            model_name="asi",
            name="certificat_origine_prod",
            field=models.FileField(null=True, upload_to="static/ASI/OP/"),
        ),
        migrations.AlterField(
            model_name="asi",
            name="copie_quittance",
            field=models.FileField(null=True, upload_to="static/ASI/Quittance"),
        ),
        migrations.AlterField(
            model_name="asi",
            name="facture_proforma",
            field=models.FileField(
                max_length=50, null=True, upload_to="static/ASI/Proforma/"
            ),
        ),
    ]
