from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from Demande.models import Demande, Type_expediteur, Voie_entree,Statut
from Demandeur.models import Demandeur
from Produit.models import Produit, Categorie, Produit_demande
from Demande.views import uploadFile, deleteFile
import json
import datetime
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def access_to_demande(views_func):
	def wrapper_func(request, *args, **kwargs):

		user_is_sh=request.user.groups.filter(name="SERVICE_HOMOLOGATION").exists()
		user_is_dt=request.user.groups.filter(name="DIRECTEUR_TECHNIQUE").exists()
		user_is_dg=request.user.groups.filter(name="DIRECTEUR_GENERAL").exists()
		user_is_admin=request.user.is_superuser

		if not request.user.is_authenticated:
			return redirect('user_signin')
		elif user_is_sh or user_is_dt or user_is_dg or user_is_admin :
			return views_func(request, *args, **kwargs)
		else:
			return render(request,'access_forbiden.html')

	return wrapper_func

def can_pay(views_func):
	def wrapper_func(request, *args, **kwargs):

		user_is_scp=request.user.groups.filter(name="SERVICE_COMPTABLE").exists()
		user_is_admin=request.user.is_superuser

		if not request.user.is_authenticated:
			return redirect('user_signin')
		elif user_is_scp or user_is_admin :
			return views_func(request, *args, **kwargs)
		else:
			return render(request,'access_forbiden.html')

	return wrapper_func


def is_admin(views_func):
	def wrapper_func(request, *args, **kwargs):

		user_is_admin=request.user.is_superuser

		if not request.user.is_authenticated:
			return redirect('user_signin')
		elif user_is_admin :
			return views_func(request, *args, **kwargs)
		else:
			return render(request,'access_forbiden.html')

	return wrapper_func

