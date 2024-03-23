from django.db import models
from Produit.models import Categorie
from Demande.models import Demande
from Demandeur.models import Structure

class Nature_impression_asi(models.Model):
    libelle=models.CharField(max_length=25)

    class Meta:
        verbose_name = ("demandeur")
        verbose_name_plural = ("demandeurs")

class ASI(Demande):
    
    facture_proforma=models.FileField(upload_to='asi/proforma/', blank=True, null=True)
    code_facture=models.TextField(null=True)
    date_facture=models.DateField(null=True)
    certicat_bonne_pratique=models.FileField(upload_to='asi/cert_bonne_pratiq/', blank=True, null=True)
    certificat_analyse_prod=models.FileField(upload_to='asi/certificat_analyse_prod/', blank=True, null=True)
    certificat_origine_prod=models.FileField(upload_to='asi/cert_origine_prod/', blank=True, null=True)
    certificat_atestation_don=models.FileField(upload_to='asi/cert_attestation_don/', blank=True, null=True)
    nombre=models.IntegerField(null=True)
    total_item=models.IntegerField(null=True)
    cout=models.IntegerField(null=True)
    nature_impression=models.ForeignKey(Nature_impression_asi, null=True, on_delete=models.CASCADE)
    note_stupefiant=models.TextField(null=True)

class Group_facture(models.Model):
    structure=models.ForeignKey(Structure, null=True, on_delete=models.CASCADE)
    code=models.TextField(null=True)
    cout=models.IntegerField(null=True)
    num_quittance=models.CharField(max_length=100,null=True)
    payer=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Facture(models.Model):
    asi=models.ForeignKey(ASI, null=True, on_delete=models.CASCADE)
    group_facture=models.ForeignKey(Group_facture, null=True, on_delete=models.CASCADE)
    num_quittance=models.CharField(max_length=100,null=True)
    copie_quittance=models.TextField(null=True)
    code=models.TextField(null=True)
    nombre=models.IntegerField(null=True)
    cout=models.IntegerField(null=True)
    total_item=models.IntegerField(null=True)
    payer=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)