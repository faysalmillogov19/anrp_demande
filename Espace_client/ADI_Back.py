from django.shortcuts import render,redirect
from ADI.models import ADI
from Demande.models import Demande, Type_expediteur, Voie_entree, Statut, Traitement, Nature_impression, Signataire, Infos
from Demandeur.models import Demandeur
from Produit.models import Produit, Categorie, Produit_demande
from django.conf import settings
from django.shortcuts import render
from django.templatetags.static import static
from SystemConf.Back_Control_Access import access_to_demande
from emailing.views import Send_mailText, Send_mailFile
from emailing.models import EmailMessage
from django.db.models import Q



@access_to_demande
def list(request):
	user_is_sh=request.user.groups.filter(name="SERVICE_HOMOLOGATION").exists()
	user_is_dt=request.user.groups.filter(name="DIRECTEUR_TECHNIQUE").exists()
	user_is_dg=request.user.groups.filter(name="DIRECTEUR_GENERAL").exists()

	if user_is_sh:
		data=ADI.objects.filter(statut=3)
	elif user_is_dt:
		data=ADI.objects.filter(statut__gte=3, statut__lte=5)
	elif user_is_dg:
		data=ADI.objects.filter(statut__gt=5, statut__lte=7)
	else:
		data=ADI.objects.all()

	return render(request,'Espace_client/adi/list_adi.html',{'data':data})


@access_to_demande
def details(request, id):
	user_is_sh=request.user.groups.filter(name="SERVICE_HOMOLOGATION").exists()
	user_is_dt=request.user.groups.filter(name="DIRECTEUR_TECHNIQUE").exists()
	user_is_dg=request.user.groups.filter(name="DIRECTEUR_GENERAL").exists()
	can_treat=False;
	can_print=False;

	datum=ADI.objects.get(id=id)
	categories=Categorie.objects.all()
	natures=Nature_impression.objects.all()

	
	if user_is_sh:
		statut=Statut.objects.filter(id=4)
		can_treat=True
	elif user_is_dt:
		statut=Statut.objects.filter(~Q(id=5), id__gte=3, id__lte=6)
		can_treat=True
	elif user_is_dg:
		statut=Statut.objects.filter(id__gte=5, id__lte=7)
		can_print=True
	else:
		statut=Statut.objects.all()

	
	return render(request,'Espace_client/adi/details.html',{'datum':datum,'statut':statut,'categories':categories, "can_treat":can_treat,"can_print":can_print,'natures':natures})


def treat(request, id):
	if request.method=="POST":

		statut=Statut.objects.get(id=int(request.POST.get('statut')))

		demande=ADI.objects.get(id=id)
		demande.statut=statut
		demande.note=request.POST.get('note')
		if request.POST.get('nature'):
			demande.nature_impression=Nature_impression.objects.get(id=int(request.POST.get('nature')))

		
		demande.save()
		if request.POST.get('commentaire'):
			traitement=Traitement()
			traitement.type_demande=2
			traitement.demande=demande
			traitement.statut=statut
			traitement.commentaire=request.POST.get('commentaire')
			traitement.save()
	return redirect('list_adi')


def renvoie_modification(request):
	if request.method=="POST":
		
		id=request.POST.get('id')
		element=Demande.objects.get(id=int(id))
		element.statut=Statut.objects.get(id=1)
		element.save()

		url=EmailMessage.objects.get(id=4).modif_url
		email=element.demandeur.user.email
		objet=request.POST.get('objet')
		message=request.POST.get('message')+'\n Cliquer sur le lien: '+url+id
		Send_mailText(objet, message, email)
		return redirect('list_adi')


def print_adi(request, id):

	datum=ADI.objects.get(id=id)
	produits=Produit_demande.objects.filter(demande=Demande.objects.get(id=id))
	signataire=Signataire.objects.get(id=1)
	libelle_demande="l’importation"
	intitule_demande="ATTESTATION DEROGATOIRE D’IMPORTATION"
	infos=Infos.objects.get(id=1)
	message=EmailMessage.objects.get(id=4)

	if datum.nature_impression_id == 1:
		return render(request, "Espace_client/adi/print_adi.html", {'datum':datum,'produits':produits,'signataire':signataire, 'libelle_demande':libelle_demande,'intitule_demande':intitule_demande,'infos':infos,'message':message} )
	elif datum.nature_impression_id == 2:
		return render(request, "Espace_client/REJET.html", {'datum':datum, 'signataire':signataire,'libelle_demande':libelle_demande,'infos':infos,'message':message} )

	return redirect('list_asi')
