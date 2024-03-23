from django.db import models
from Produit.models import Categorie
from Demande.models import Demande, Nature_impression


class ASE(Demande):
    
    facture_proforma=models.FileField(upload_to='ase/proforma/', blank=True, null=True)
    code_facture=models.TextField(null=True)
    date_facture=models.DateField(null=True)
    copie_asi=models.FileField(upload_to='ase/copie_asi/', blank=True, null=True)
    total_item=models.IntegerField(null=True)
    nature_impression=models.ForeignKey(Nature_impression, null=True, on_delete=models.CASCADE)
    
    

    