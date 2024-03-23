from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Structure(models.Model):
    denomination=models.CharField(max_length=50,null=True)
    telephone=models.CharField(max_length=20,null=True)
    email=models.CharField(max_length=100, null=True)
    bp=models.CharField(max_length=100, null=True)
    grossiste=models.BooleanField(default=False)

class Demandeur(models.Model):
    tel=models.IntegerField(null=True)
    adresse=models.TextField(null=True)
    structure=models.CharField(max_length=150)
    user=models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    affect_structure=models.ForeignKey(Structure, null=True, on_delete=models.CASCADE)