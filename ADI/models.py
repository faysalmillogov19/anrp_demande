from django.db import models
from Produit.models import Categorie, Devise
from Demande.models import Demande, Nature_impression


class ADI(Demande):
    
    facture_proforma=models.FileField(upload_to='adi/proforma/', blank=True, null=True)
    code_facture=models.TextField(null=True)
    date_facture=models.DateField(null=True)
    total_item=models.IntegerField(null=True)
    cout=models.IntegerField(null=True)
    devise=models.ForeignKey(Devise, null=True, on_delete=models.CASCADE)
    nature_impression=models.ForeignKey(Nature_impression, null=True, on_delete=models.CASCADE)
    

    