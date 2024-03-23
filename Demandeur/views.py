from django.shortcuts import render, redirect
from .models import Demandeur, Structure
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from emailing.views import Send_mailFile, Send_mailText
from SystemConf.Back_Control_Access import is_admin

@is_admin
def list_demandeur(request):
	data=Demandeur.objects.all()
	structures=Structure.objects.all()
	return render(request,'Demandeur/list_demandeur.html',{'data':data, 'structures':structures})

@is_admin
def affectation_structure(request, id_demandeur):
	demandeur=Demandeur.objects.get(id=id_demandeur)
	demandeur.affect_structure=Structure.objects.get(id=request.POST.get('structure'))
	demandeur.save()
	return redirect('demandeur_list')

@is_admin
def change_state(request, user_id):
	print(user_id)
	if request.method=="POST":
		user=User.objects.get( id=user_id )
		user.is_active=request.POST.get('state')
		user.save()
	return redirect('demandeur_list')


def signin(request):

	if request.method=="POST":

		email=request.POST.get('email')
		password=request.POST.get('password')

		user=authenticate(username=email, password=password)

		if user is not None:
			login(request, user)
			return redirect('/')
		else:
			messages="Identifiants incorrectes !!!!"
			return render(request,'Demandeur/SignIn.html',{'email':email, 'password':password, 'messages':messages})
	else:
		return render(request,'Demandeur/SignIn.html')

def signout(request):
	if request.method=="POST":
		logout(request)
	return redirect('/')

def signup(request):

	if request.method=="POST":
		try:
			user=User.objects.create_user(username=request.POST.get("username"), email=request.POST.get("email"), password=request.POST.get("password"))
			group=Group.objects.get(id=1)
			user.first_name=request.POST.get("nom")
			user.save()
			user.groups.add(group)
			demandeur=Demandeur()
			demandeur.tel=request.POST.get("tel")
			demandeur.structure=request.POST.get("structure")
			demandeur.adresse=request.POST.get("adresse")
			demandeur.user=user
			demandeur.save()
			message="Votre compte a bien été crée sur la plateforme en ligne de l'ANRP. \n Ce message est envoyé par  un robot, \n Merci de ne pas répondre !!!!!"
			created=Send_mailText("Notification de création compte",message,user.email)
			login(request, user)

		except Exception as e:
			created=0
			data={
					'username':request.POST.get("username"), 
					'email':request.POST.get("email"), 
					'nom': request.POST.get("nom"),
					'password':request.POST.get("password"),
					'tel':request.POST.get("tel"),
					'structure':request.POST.get("structure"),
					'adresse':request.POST.get("adresse"),
					'message':'Cet utilisateur existe déjà. '
				}

		if created:
			return redirect('/')
		else:
			return render(request,'Demandeur/SignUp.html',data)
		
	else:

		return render(request,'Demandeur/SignUp.html')