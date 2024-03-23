from django.shortcuts import render,redirect
from ASI.models import ASI, Nature_impression_asi, Facture, Group_facture
from Demande.models import Demande, Type_expediteur, Voie_entree, Statut, Traitement, Signataire, Infos
from Demandeur.models import Demandeur, Structure
from Produit.models import Produit, Categorie, Produit_demande
from django.conf import settings
from django.shortcuts import render
from django.templatetags.static import static
from SystemConf.Back_Control_Access import access_to_demande, can_pay
from emailing.views import Send_mailText, Send_mailFile
from emailing.models import EmailMessage
from django.db.models import Q, Sum
from datetime import datetime
from num2words import num2words
import locale
locale.setlocale(locale.LC_TIME, 'fr_FR')


@can_pay
def paiement(request):
	asi=[]
	code_facture=''
	num_quittance=''
	inexistant=False
	if request.method=="POST":
		code_facture=request.POST.get('num_facture')
		num_quittance=request.POST.get('num_quittance')
		facture=Facture.objects.filter(code=code_facture).first()
		print(facture)
		if facture:
			facture.num_quittance=num_quittance
			facture.payer=True
			facture.save()
			asi=ASI.objects.get(id=facture.asi_id)
			asi.statut=Statut.objects.get(id=3)
			asi.save()
		else:
			inexistant=True

	return render(request,'Espace_client/comptabilite/paiement.html',{'asi':asi,'code_facture':code_facture,'num_quittance':num_quittance,'inexistant':inexistant})

@can_pay
def list_paiement(request):
	data=Facture.objects.filter(cout__gt=0)
	paye=Facture.objects.filter(payer=True).aggregate(Sum("cout", default=0))
	non_paye=Facture.objects.filter(payer=False).aggregate(Sum("cout", default=0))
	return render(request,'Espace_client/comptabilite/list_paiement.html',{'data':data, 'paye':paye, 'non_paye':non_paye})

def list_impaye_structure(request):
	data=Facture.objects.filter(payer=False).values('asi__demandeur__affect_structure_id').values('asi__demandeur__affect_structure__denomination').annotate(cout=Sum('cout')).order_by('asi__demandeur__affect_structure_id')
	return render(request,'Espace_client/comptabilite/liste_impaye_structure.html',{'data':data})

def list_impaye_groupby__structure(request, structure_name):
	structure=Structure.objects.filter(denomination=structure_name).first()
	data=Facture.objects.filter(payer=False, asi__demandeur__affect_structure_id=structure.id)
	return render(request,'Espace_client/comptabilite/list_impaye_groupby__structure.html',{'data':data, 'structure':structure})

def list_goup_facture(request, structure_name):

	structure=Structure.objects.filter(denomination=structure_name).first()
	data=Group_facture.objects.filter(structure=structure, payer=False)
	
	return render(request,'Espace_client/comptabilite/list_group_facture.html',{'data':data, 'structure':structure})


def create_groupe_facture(request, id_structure):
	if request.method=='POST':
		structure=Structure.objects.get(id=id_structure)
		factures=request.POST.getlist('choix[]')
		if len(factures)>0:
			group_facture=Group_facture()
			group_facture.structure=structure
			group_facture.save()
			cout=0

			for id_fact in factures:
				facture=Facture.objects.get(id=id_fact)
				facture.group_facture=group_facture
				facture.save()
				cout+=facture.cout

			group_facture.cout= cout
			group_facture.code=str(datetime.today().strftime("%d%m%Y"))+str(group_facture.id)
			group_facture.save()

			return redirect('list_goup_facture', structure_name=structure.denomination)
		
	return redirect('list_impaye_groupby__structure', structure_name=structure.denomination)


def print_group_facture(request, id_groupe_facture):
	group_facture= Group_facture.objects.get(id=id_groupe_facture)
	num_to_text=num2words(group_facture.cout, lang='fr')
	structure=Structure.objects.get(id=group_facture.structure.id)
	signataire=Signataire.objects.get(id=2)
	data=Facture.objects.filter(payer=False, group_facture=group_facture)
	periode=[]
	for d in data:
		#d.updated_at.strftime('%A %d %B %Y')
		periode.append(d.updated_at.strftime('%B'))
	return render(request,'Espace_client/comptabilite/print_group_facture.html',{'data':data, 'structure':structure, 'group_facture':group_facture,'num_to_text':num_to_text,'periode':periode,'signataire':signataire})
		
def paiement_group(request):
	if request.method=="POST":
		group_facture=Group_facture.objects.filter( code=request.POST.get('code'), payer=False ).first()


		num_quittance=request.POST.get('num_quittance') 

		if group_facture:

			group_facture.num_quittance=num_quittance
			group_facture.payer=True
			group_facture.save()

			structure=Structure.objects.get(id=group_facture.structure.id)

			factures=Facture.objects.filter(group_facture=group_facture)
			for facture in factures:
				facture.payer=True
				facture.num_quittance=num_quittance
				facture.save()

			data=Facture.objects.filter(group_facture=group_facture)
			signataire=Signataire.objects.get(id=2)

			return render(request,'Espace_client/comptabilite/print_group_facture.html',{'data':data, 'structure':structure, 'group_facture':group_facture, 'signataire':signataire})
		else:
			message="Une erreur est survénue lors du paiment !!!! Cette facture n'existe pas, ou a déjà l'objet d'un paiement."
			color="text-danger"
			return render(request,'Espace_client/comptabilite/message_paiement.html',{'message':message, 'color':color})

	return render(request,'Espace_client/comptabilite/paiement_group.html')