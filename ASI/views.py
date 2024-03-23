from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import ASI, Facture
from ADI.models import ADI
from ASE.models import ASE
from DPI.models import DPI
from Demande.models import Demande, Type_expediteur, Voie_entree,Statut, Objet_demande, Infos
from Demandeur.models import Demandeur
from Produit.models import Produit, Categorie, Produit_demande, Devise
from Filing.views import uploadFile, deleteFile, generateQRCode, add_text_Recepice
import json
from datetime import datetime
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from SystemConf.Front_Control_Access import access_to_asi
from emailing.views import Send_mailFile
from emailing.models import EmailMessage
from django.db.models import Q, Avg, Sum


@login_required(login_url='demandeur_signin')
def add_produit(request, id_asi):
	#ASI.objects.all().delete()
	if request.method=="POST":
		demandeur=Demandeur.objects.filter(user=request.user).first()
		element= Produit_demande()
		if id_asi==0:
			asi=ASI();
			asi.demandeur=demandeur
			asi.save()
			element.demande=Demande.objects.get(id=asi.id)
		else:
			element.demande=Demande.objects.get(id=id_asi)

		element.categorie=Categorie.objects.get( id=request.POST.get('categorie') )
		element.devise_id=request.POST.get('devise')
		element.dc=request.POST.get('dc')
		element.dci=request.POST.get('dci')
		element.forme=request.POST.get('forme')
		element.dosage=request.POST.get('dosage')
		element.presentation=request.POST.get('presentation')
		element.quantite=request.POST.get('quantite')
		element.cout=request.POST.get('cout')
		element.stupefiant=bool(request.POST.get('stupefiant'))
		element.amm=verify_amm(element.categorie, element.dc, element.dosage)
		element.save()
		return redirect('/asi/list_produit/'+str(element.demande.id))
	else:
		categories=Categorie.objects.all()
		devises=Devise.objects.all()
		return render(request,'ASI/add_produit.html',{'categories':categories,'id_asi':id_asi,'devises':devises})

@access_to_asi
def list_produit(request, id_asi):
	produits= Produit_demande.objects.filter(demande=id_asi)
	return render(request,'ASI/list_produit.html',{'produits':produits,'id_asi':id_asi})

@login_required(login_url='demandeur_signin')
def delete_produit(request, id):
	element=Produit_demande.objects.get(id=id)
	element.delete()
	return redirect('/asi/list_produit/'+str(element.demande.id))

@login_required(login_url='demandeur_signin')
def set_produit(request, id):
	if request.method=='POST':
		element=Produit_demande.objects.get(id=id)
		element.categorie=Categorie.objects.get( id=request.POST.get('categorie') )
		element.devise_id=request.POST.get('devise')
		element.dc=request.POST.get('dc')
		element.dci=request.POST.get('dci')
		element.forme=request.POST.get('forme')
		element.dosage=request.POST.get('dosage')
		element.presentation=request.POST.get('presentation')
		element.quantite=request.POST.get('quantite')
		element.cout=request.POST.get('cout')
		element.stupefiant=bool(request.POST.get('stupefiant'))
		element.amm=verify_amm(element.categorie, element.dc, element.dosage)
		element.save()
		return redirect('/asi/list_produit/'+str(element.demande.id))
	else:
		produit=Produit_demande.objects.get(id=id)
		categories=Categorie.objects.all()
		devises=Devise.objects.all()
		return render(request,'ASI/set_produit.html',{'categories':categories,'produit':produit,'devises':devises})

@access_to_asi
def expediteur(request, id_asi):
	if request.method=="POST":
		element= ASI.objects.get(id=id_asi)
		element.type_expediteur=Type_expediteur.objects.get( id=request.POST.get('type_expediteur') )
		element.objet_id=int( request.POST.get('objet') )
		element.destinataire=request.POST.get('destinataire') 
		element.voie_entree=Voie_entree.objects.get( id=request.POST.get('voie') )
		element.nom_expediteur=request.POST.get('nom_expediteur')
		element.adresse_expediteur=request.POST.get('adresse_expediteur')
		element.nom_transitaire=request.POST.get('nom_transitaire')
		element.adresse_transitaire=request.POST.get('adresse_transitaire')
		element.save()
		return redirect('/asi/pieces_jointes/'+str(element.id))
	else:
		type_expediteurs=Type_expediteur.objects.all()
		voies=Voie_entree.objects.all()
		objets=Objet_demande.objects.all()
		element=ASI.objects.get(id=id_asi)
		return render(request,'ASI/add_expediteur.html',{'element':element,'id_asi':id_asi,'type_expediteurs':type_expediteurs,'voies':voies,'objets':objets})

@access_to_asi
def pieces_jointes(request, id_asi):
	if request.method=="POST":
		element= ASI.objects.get(id=id_asi)
		if request.FILES.get("facture_proforma"):
			element.facture_proforma=request.FILES.get("facture_proforma")
			#element.facture_proforma=uploadFile(request.FILES.get("facture_proforma"),"static/", "uploads/ASI/Proforma/", '.pdf')
		if request.FILES.get("certicat_bonne_pratique"):
			element.certicat_bonne_pratique=request.FILES.get("certicat_bonne_pratique")
			#element.certicat_bonne_pratique=uploadFile(request.FILES.get("certicat_bonne_pratique"), "static/", "uploads/ASI/BP/", '.pdf')
		if request.FILES.get("certificat_analyse_prod"):
			element.certificat_analyse_prod=request.FILES.get("certificat_analyse_prod")
			#element.certificat_analyse_prod=uploadFile(request.FILES.get("certificat_analyse_prod"), "static/", "uploads/ASI/AP/", '.pdf')
		if request.FILES.get("certificat_origine_prod"):
			element.certificat_origine_prod=request.FILES.get("certificat_origine_prod")
			#element.certificat_origine_prod=uploadFile(request.FILES.get("certificat_origine_prod"), "static/", "uploads/ASI/OP/", '.pdf')
		if request.FILES.get("certificat_atestation_don"):
			element.certificat_atestation_don=request.FILES.get("certificat_atestation_don")
			#element.certificat_atestation_don=uploadFile(request.FILES.get("certificat_atestation_don"), "static/", "uploads/ASI/AD", '.pdf')
		element.code_facture=request.POST.get('code_facture')
		element.date_facture=request.POST.get('date_facture')
		element.save()
		return redirect('/asi/recap_asi/'+str(element.id))
	else:
		element=ASI.objects.get(id=id_asi)
		sans_amm=Produit_demande.objects.filter(amm=False).first()
		return render(request,'ASI/add_piece.html',{'element':element,'id_asi':id_asi,'sans_amm':sans_amm})

#@access_to_asi
def recap_asi(request, id_asi):
	nombre=Produit_demande.objects.filter( Q(demande_id=id_asi) & ( Q(amm=False) | Q(stupefiant=True) ) ).count()
	info=Infos.objects.get(id=1)
	cout=info.cout_asi*nombre
	asi=ASI.objects.get(id=id_asi)
	complete=len(str(asi.certificat_atestation_don))
	if  (len(str(asi.facture_proforma)) == 0 ) or (len(str(asi.certicat_bonne_pratique)) == 0 ) or (asi.nom_expediteur is None) or (asi.nom_transitaire is None) or (asi.type_expediteur is None) :
		return render(request,'ASI/uncomplete_asi.html',{'id_asi':id_asi})
	else:
		return render(request,'ASI/recap_asi.html',{'nombre':nombre,'cout':cout,'id_asi':id_asi})

#@access_to_asi
def valid_asi(request, id_asi):
	if request.method=='POST':

		asi=ASI.objects.get(id=id_asi)
		asi.total_item=Produit_demande.objects.filter(demande_id=id_asi ).count()
		asi.date_soumission=datetime.today()
		
		demandeur=Demandeur.objects.filter(user=request.user).first()
		
		if int(request.POST.get('nombre')) > 0:
			asi.nombre=int(request.POST.get('nombre'))
			asi.cout=int(request.POST.get('cout'))
			if demandeur.affect_structure and demandeur.affect_structure.grossiste:
				asi.statut=Statut.objects.get(id=3)
			else:
				asi.statut=Statut.objects.get(id=2)
			asi.save()
		else:
			asi.statut=Statut.objects.get(id=3)
			asi.nombre=0
			asi.cout=0
			asi.save()

		code=str(asi.date_soumission.strftime("%d%m%Y"))+str(asi.id)
		info=Infos.objects.get(id=1)
		facture=calcul_montant(id_asi, asi.nombre, asi.total_item, asi.cout)

		data=[	 
				"Demande d’Autorisation Spécial d’Importation (ASI)",
				"Code: "+facture.code,
				"Nom : "+demandeur.user.first_name,
				"Structure: "+demandeur.structure,
				"Téléphone: "+str(demandeur.tel),
				"Email: "+demandeur.user.email,
				"Total Produit: "+str(asi.total_item),
				"Produits sans AMM : "+str(asi.nombre),
				"Cout: "+str(facture.cout)+' '+info.monaie,
				"Date: "+str(asi.date_soumission.strftime("%d/%m/%Y"))
		]
		
		qr_code=generateQRCode(info.url_recepice+'asi/'+str(asi.id), 'static/uploads/Recepice/')
		filename=add_text_Recepice(data,qr_code)
		msg=EmailMessage.objects.get(id=1)
		send=Send_mailFile(msg.objet, msg.message, demandeur.user.email, filename)
		deleteFile(qr_code)
		deleteFile(filename)

		return render(request,'end_demande.html',{})

def calcul_montant(id_asi, nombre, total_item, cout):
	asi=ASI.objects.get(id=id_asi)
	paye=Facture.objects.filter(asi=asi, payer=True).aggregate(Sum("cout", default=0))
	last=Facture.objects.filter(asi=asi, payer=False).last()
	cout=cout-paye['cout__sum']
	
	if cout >0 and last:
		last.cout=cout
		last.nombre=nombre
		last.total_item=total_item
		last.save()

	elif cout > 0 and (last is None):
		last=Facture()
		last.asi=asi
		last.nombre=nombre
		last.total_item=total_item
		last.cout=cout
		asi=ASI.objects.get(id=id_asi)
		asi.save()
		last.save()
		last.code=str(datetime.today().strftime("%d%m%Y"))+str(last.id)
		last.save()

	elif cout <= 0 and last :
		asi.statut=Statut.objects.get(id=3)
		last.delete()

	else:
		last=Facture()
		asi.statut=Statut.objects.get(id=3)
		last.code=" "
		last.cout=0
		last.nombre=nombre
		last.total_item=total_item

	return last


def delete_all(request):
	asi=ASI.objects.all().delete()
	adi=ADI.objects.all().delete()
	dpi=DPI.objects.all().delete()
	ase=ASE.objects.all().delete()
	facture=Facture.objects.all().delete()
	return redirect('index')


##############################################################################################################
######################  FILTRAGE DES DIFFERENTTS CHAMPS AUTOCOMPLETION PRODUITS ##############################
##############################################################################################################

def get_produit(request, id):
	data=Produit.objects.filter(categorie=id)
	data = serializers.serialize('json', data)
	return HttpResponse(data, content_type='application/json')

def get_dc_autocompletion(request, dc):
	data=Produit.objects.filter(dc__contains=dc.lower())
	data = serializers.serialize('json', data)
	return HttpResponse(data, content_type='application/json')

def get_dci_autocompletion(request, dci):
	data=Produit.objects.filter(dci__contains=dci.lower())
	data = serializers.serialize('json', data)
	return HttpResponse(data, content_type='application/json')

def get_forme_autocompletion(request, name):
	data=Produit.objects.filter(forme__contains=name)
	data = serializers.serialize('json', data)
	return HttpResponse(data, content_type='application/json')

def get_dosage_autocompletion(request, name):
	data=Produit.objects.filter(dosage__contains=name.lower())
	data = serializers.serialize('json', data)
	return HttpResponse(data, content_type='application/json')

def get_presentation_autocompletion(request, name):
	data=Produit.objects.filter(presentation__contains=name.lower())
	data = serializers.serialize('json', data)
	return HttpResponse(data, content_type='application/json')

def verify_amm(categorie, dc, dosage):
	today=datetime.today()
	return Produit.objects.filter(categorie=categorie, dc__contains=dc, dosage__contains=dosage,expiration_amm__gte=today).exists()

