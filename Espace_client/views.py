from django.shortcuts import render,redirect
from ASI.models import ASI, Nature_impression_asi
from Demande.models import Demande, Type_expediteur, Voie_entree, Statut, Traitement, Signataire, Infos
from Demandeur.models import Demandeur
from Produit.models import Produit, Categorie, Produit_demande
from django.conf import settings
from django.shortcuts import render
from django.templatetags.static import static
from SystemConf.Back_Control_Access import access_to_demande, can_pay
from emailing.views import Send_mailText, Send_mailFile
from emailing.models import EmailMessage
from django.db.models import Q

@access_to_demande
def index(request):
	return render(request,'Espace_client/index.html',{})

@access_to_demande
def list_asi(request):
	user_is_sh=request.user.groups.filter(name="SERVICE_HOMOLOGATION").exists()
	user_is_dt=request.user.groups.filter(name="DIRECTEUR_TECHNIQUE").exists()
	user_is_dg=request.user.groups.filter(name="DIRECTEUR_GENERAL").exists()

	if user_is_sh:
		data=ASI.objects.filter(statut=3)
	elif user_is_dt:
		data=ASI.objects.filter(statut__gte=3, statut__lte=5)
	elif user_is_dg:
		data=ASI.objects.filter(statut__gt=5, statut__lte=7)
	else:
		data=ASI.objects.all()

	return render(request,'Espace_client/asi/list_asi.html',{'data':data})

@access_to_demande	
def get_asi(request, id):
	datum=ASI.objects.get(id=id)
	#datum.facture_proforma='media/'+str(datum.facture_proforma)
	return render(request,'Espace_client/asi/infos_asi.html',{'datum':datum})

@access_to_demande
def asi_list_produit(request, id):
	user_is_sh=request.user.groups.filter(name="SERVICE_HOMOLOGATION").exists()
	user_is_dt=request.user.groups.filter(name="DIRECTEUR_TECHNIQUE").exists()
	user_is_dg=request.user.groups.filter(name="DIRECTEUR_GENERAL").exists()
	can_treat=False;
	can_print=False;

	datum=ASI.objects.get(id=id)
	categories=Categorie.objects.all()
	natures=Nature_impression_asi.objects.all()
	
	if user_is_sh:
		statut=Statut.objects.filter(id=4)
		can_treat=True
	elif user_is_dt:
		statut=Statut.objects.filter( id__gte=3, id__lte=6 )#~Q(id=5),
		can_treat=True
		can_print=True
	elif user_is_dg:
		statut=Statut.objects.filter(id__gte=5, id__lte=7)
		can_print=True
	else:
		statut=Statut.objects.all()

	produits=Produit_demande.objects.filter(demande=Demande.objects.get(id=id))
	produit_amm=Produit.objects.all()
	return render(request,'Espace_client/asi/asi_list_produit.html',{'datum':datum,'produits':produits,'statut':statut,'categories':categories,'produit_amm':produit_amm,"can_treat":can_treat,"can_print":can_print,'natures':natures})

@access_to_demande
def change_produit_amm(request):
	if request.method=='POST':
		produit=Produit_demande.objects.get(id=int(request.POST.get('produit_id')))
		produit.amm=bool( int(request.POST.get('amm')) )
		produit.save()
		asi=ASI.objects.get(id=produit.demande.id)
		asi.nombre=Produit_demande.objects.filter(demande=asi, amm=False).count()
		asi.cout=asi.nombre*2000
		asi.save()

		return redirect('manage_asi_list_produit', id=produit.demande.id)

@access_to_demande
def change_produit_stupefiant(request):
	if request.method=='POST':
		produit=Produit_demande.objects.get(id=int(request.POST.get('produit_id')))
		produit.stupefiant=bool( int(request.POST.get('stupefiant')) )
		produit.save()
		return redirect('manage_asi_list_produit', id=produit.demande.id)

@access_to_demande
def note_stupefiant(request, id):
	if request.method=='POST':
		asi=ASI.objects.get(id=id)
		asi.note_stupefiant=request.POST.get('note')
		asi.save()
	return redirect('manage_asi_list_produit', id=id)

@access_to_demande
def treat_asi(request, id):
	if request.method=="POST":

		asi=ASI.objects.get(id=id)
		statut=Statut.objects.get(id=int(request.POST.get('statut')))
		asi.statut=statut
		asi.note=request.POST.get('note')

		if request.POST.get('nature'):
			asi.nature_impression=Nature_impression_asi.objects.get(id=int(request.POST.get('nature')))
		
		asi.save()
		if request.POST.get('commentaire'):
			traitement=Traitement()
			traitement.type_demande=1
			traitement.demande=asi
			traitement.statut=statut
			traitement.commentaire=request.POST.get('commentaire')
			traitement.save()
	return redirect('list_asi')

@access_to_demande
def renvoie_modification(request):
	if request.method=="POST":
		
		id=request.POST.get('id')
		element=Demande.objects.get(id=int(id))
		element.statut=Statut.objects.get(id=1)
		element.save()

		url=EmailMessage.objects.get(id=1).modif_url
		email=element.demandeur.user.email
		objet=request.POST.get('objet')
		message=request.POST.get('message')+'\n Cliquer sur le lien: '+url+id
		Send_mailText(objet, message, email)
		return redirect('list_asi')

@access_to_demande
def print_asi(request, id):

	datum=ASI.objects.get(id=id)
	produits=Produit_demande.objects.filter(demande=Demande.objects.get(id=id), amm=False, stupefiant=False)
	stupefiant=Produit_demande.objects.filter(demande=Demande.objects.get(id=id), stupefiant=True).exists()
	signataire=Signataire.objects.get(id=1)
	libelle_demande=""
	intitule_demande="AUTORISATION SPECIAL d'IMPORTATION "
	infos=Infos.objects.get(id=1)
	message=EmailMessage.objects.get(id=1)

	if datum.nature_impression_id == 1:
		intitule_demande="AUTORISATION SPECIAL D'IMPORTATION(ASI)"
		return render(request, "Espace_client/asi/ASI_print.html", {'datum':datum,'produits':produits,'signataire':signataire,'libelle_demande':libelle_demande,'intitule_demande':intitule_demande,'stupefiant':stupefiant, 'infos':infos,'message':message} )
	elif datum.nature_impression_id == 2:
		libelle_demande="Autorisation SPECIAL d'IMPORTATION  en Autorisation Retrait inspection (ARI)"
		intitule_demande="AUTORISATION RETRAIT INSPECTION "
		return render(request, "Espace_client/asi/ARI_print.html", {'datum':datum, 'produits':produits,'signataire':signataire,'libelle_demande':libelle_demande,'intitule_demande':intitule_demande, 'infos':infos,'message':message} )
	elif datum.nature_impression_id == 3:
		return render(request, "Espace_client/REJET.html", {'datum':datum, 'signataire':signataire,'libelle_demande':libelle_demande,'infos':infos,'message':message} )

	return redirect('list_asi')

@access_to_demande
def print_asi_stupefiant(request, id):
	datum=ASI.objects.get(id=id)
	produits=Produit_demande.objects.filter(demande=Demande.objects.get(id=id), stupefiant=True)
	signataire=Signataire.objects.get(id=1)
	libelle_demande=" l'importaion"
	intitule_demande="AUTORISATION SPECIAL D'IMPORTATION DE STUPEFIANT ET PSYCHOTROPES"
	infos=Infos.objects.get(id=1)
	message=EmailMessage.objects.get(id=1)
	return render(request, "Espace_client/asi/ASI_stupefiant_print.html", {'datum':datum,'produits':produits,'signataire':signataire,'libelle_demande':libelle_demande,'intitule_demande':intitule_demande, 'infos':infos,'message':message} )
