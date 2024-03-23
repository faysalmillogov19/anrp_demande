from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import ADI
from Demande.models import Demande, Type_expediteur, Voie_entree,Statut, Infos, Objet_demande
from Demandeur.models import Demandeur
from Produit.models import Produit, Categorie, Produit_demande, Devise
from Filing.views import uploadFile, deleteFile, generateQRCode, add_text_Recepice
import json
from datetime import datetime
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from SystemConf.Front_Control_Access import access_to_demande, is_demandeur
from emailing.views import Send_mailFile
from emailing.models import EmailMessage

@is_demandeur
def add(request, id_demande):
	
	if id_demande>0:
		element=ADI.objects.get(id=id_demande)
	else:
		element=ADI()

	if request.method=="POST":
		demandeur=Demandeur.objects.filter(user=request.user).first()
		element.demandeur=demandeur
		element.type_expediteur=Type_expediteur.objects.get( id=request.POST.get('type_expediteur') )
		element.voie_entree=Voie_entree.objects.get( id=request.POST.get('voie') )
		element.nom_expediteur=request.POST.get('nom_expediteur')
		element.adresse_expediteur=request.POST.get('adresse_expediteur')
		element.nom_transitaire=request.POST.get('nom_transitaire')
		element.adresse_transitaire=request.POST.get('adresse_transitaire')
		element.destinataire=request.POST.get('destinataire')
		element.objet_id=int( request.POST.get('objet') )

		if request.FILES.get("facture_proforma"):
			element.facture_proforma=request.FILES.get("facture_proforma")
		
		element.code_facture=request.POST.get("code_facture")
		element.date_facture=request.POST.get("date_facture")


		element.total_item=request.POST.get('nombre')
		element.devise_id=request.POST.get('devise')
		element.cout=request.POST.get('cout')
		element.date_soumission=datetime.today()
		element.statut=Statut.objects.get(id=3)
		element.save()

		code=str(element.date_soumission.strftime("%d%m%Y"))+str(element.id)
		info=Infos.objects.get(id=1)

		data=[	
				"Demande d’Attestation Dérogatoire d’Importation (ADI)",
				"Code: "+code,
				"Nom : "+demandeur.user.first_name,
				"Structure: "+demandeur.structure,
				"Téléphone: "+str(demandeur.tel),
				"Email: "+demandeur.user.email,
				"Total Produit: "+str(element.total_item),
				"Date: "+str(element.date_soumission.strftime("%d/%m/%Y"))
		]

		qr_code=generateQRCode(info.url_recepice+'adi/'+str(element.id), 'static/uploads/Recepice/')
		filename=add_text_Recepice(data,qr_code)
		msg=EmailMessage.objects.get(id=4)
		send=Send_mailFile(msg.objet, msg.message, demandeur.user.email, filename)
		deleteFile(qr_code)
		
		return render(request,'end_demande.html',{})

	else:
		objets=Objet_demande.objects.all()
		devises=Devise.objects.all()
		type_expediteurs=Type_expediteur.objects.all()
		voies=Voie_entree.objects.all()
		return render(request,'ADI/add.html',{'id_demande':id_demande,'type_expediteurs':type_expediteurs,'voies':voies,'objets':objets,'devises':devises})
