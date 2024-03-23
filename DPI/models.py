from django.db import models
from Produit.models import Categorie
from Demande.models import Demande,Nature_impression


class DPI(Demande):
    
    facture_proforma=models.FileField(upload_to='dpi/proforma/', blank=True, null=True)
    code_facture=models.TextField(null=True)
    date_facture=models.DateField(null=True)
    liste_colisage=models.TextField(null=True)
    certificat_atestation_don=models.FileField(upload_to='dpi/attestation_don/', blank=True, null=True)
    document_douane=models.FileField(upload_to='dpi/document_douane/', blank=True, null=True)
    total_item=models.IntegerField(null=True)
    nature_impression=models.ForeignKey(Nature_impression, null=True, on_delete=models.CASCADE)
    

    