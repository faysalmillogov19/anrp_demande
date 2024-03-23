from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.core.files.storage import default_storage
import os
from ASI.models import ASI
from ADI.models import ADI
from ASE.models import ASE
from DPI.models import DPI
from Produit.models import Produit_demande
#from .models import ADI,DPI,ASI,ARI,ASE,Demande,Voie_entree,Specialisation,Demandeur

def get_asi_recepice(request, id):
	datum=ASI.objects.get(id=id)
	intitule="Demande d’Autorisation Spécial d’Importation (ASI)"
	produits=[]
	if datum:
		produits=Produit_demande.objects.filter(demande=datum.id, amm=False)
	return render(request,'recepice.html',{'datum':datum,'produits':produits,'intitule':intitule})

def get_ase_recepice(request, id):
	datum=ASE.objects.get(id=id)
	intitule="Demande d’Autorisation Spécial d’Exportation (ASE)"
	produits=[]
	if datum:
		produits=Produit_demande.objects.filter(demande=datum.id)
	return render(request,'recepice.html',{'datum':datum,'produits':produits,'intitule':intitule})

def get_dpi_recepice(request, id):
	datum=DPI.objects.get(id=id)
	intitule="Déclaration Préalable d’importation"
	produits=[]
	if datum:
		produits=Produit_demande.objects.filter(demande=datum.id)
	return render(request,'recepice.html',{'datum':datum,'produits':produits,'intitule':intitule})

def get_adi_recepice(request, id):
	datum=ADI.objects.get(id=id)
	intitule="Déclaration Préalable d’importation"
	produits=[]
	return render(request,'recepice.html',{'datum':datum,'produits':produits,'intitule':intitule,'adi':True})

def uploadFile(file_input, folder, extension):
	name=str(datetime.now().strftime("_%Y_%m_%d_%H_%M_%S"))+str(extension)
	file_name=folder+name
	if not os.path.exists(file_name):
		default_storage.save('media/'+file_name, file_input)
	print(name)
	return name #file_name

def deleteFile(link):
	os.remove('static/'+link)

