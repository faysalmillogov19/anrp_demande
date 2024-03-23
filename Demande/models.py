from django.db import models
from django.utils.timezone import now
from Demandeur.models import Demandeur
# Create your models here.

class Voie_entree(models.Model):
    libelle=models.CharField(max_length=25)

class Type_expediteur(models.Model):
    libelle=models.CharField(max_length=50)

class Type_demande(models.Model):
    libelle=models.CharField(max_length=150)

class Statut(models.Model):
    libelle=models.CharField(max_length=25)

class Nature_impression(models.Model):
    libelle=models.CharField(max_length=25)

class Objet_demande(models.Model):
    libelle=models.CharField(max_length=25)
    description=models.TextField(null=True)


    class Meta:
        verbose_name = ("demandeur")
        verbose_name_plural = ("demandeurs")

class Demande(models.Model):
    type_expediteur=models.ForeignKey(Type_expediteur, null=True, on_delete=models.CASCADE)
    nom_expediteur=models.CharField(max_length=50,null=True)
    adresse_expediteur=models.CharField(max_length=50,null=True)
    nom_transitaire=models.CharField(max_length=50,null=True)
    adresse_transitaire=models.CharField(max_length=50,null=True)
    voie_entree=models.ForeignKey(Voie_entree, null=True, on_delete=models.CASCADE)
    demandeur=models.ForeignKey(Demandeur, null=True, on_delete=models.CASCADE)
    statut=models.ForeignKey(Statut, default=1, on_delete=models.CASCADE)
    objet=models.ForeignKey(Objet_demande, null=True, on_delete=models.CASCADE)
    destinataire=models.CharField(max_length=50,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_soumission = models.DateTimeField(null=True)
    note=models.TextField(null=True)

class Traitement(models.Model):
    demande=models.ForeignKey(Demande, null=True, on_delete=models.CASCADE)
    commentaire=models.TextField(null=True)
    statut=models.ForeignKey(Statut, default=1, on_delete=models.CASCADE)
    utilisateur=models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Signataire(models.Model):
    nom_signataire=models.TextField(null=True)
    fonction=models.TextField(null=True)
    signature=models.TextField(null=True)
    titre_honorifique=models.TextField(null=True)
    url_base=models.TextField(null=True)





class Infos(models.Model):
    denomination=models.CharField(max_length=100,null=True)
    sigle=models.CharField(max_length=50,null=True)
    devise=models.CharField(max_length=50,null=True)
    monaie=models.CharField(max_length=20,null=True)
    cout_asi=models.IntegerField(default=0)
    url_base=models.CharField(max_length=50,null=True)
    url_recepice=models.CharField(max_length=50,null=True)
    telephone=models.CharField(max_length=50,null=True)
    email=models.CharField(max_length=50,null=True)
    bp=models.CharField(max_length=50,null=True)
    adresse=models.CharField(max_length=50,null=True)
    arrete=models.TextField(null=True)
    mot_fin=models.TextField(null=True)
    lien_facebook=models.TextField(null=True)
    lien_youtube=models.TextField(null=True)
    lien_instagram=models.TextField(null=True)
    lien_linkedil=models.TextField(null=True)