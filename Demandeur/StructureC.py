from django.shortcuts import render, redirect
from .models import Demandeur, Structure
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from emailing.views import Send_mailFile, Send_mailText


def list_structure(request):
	data=Structure.objects.all()
	return render(request,'structure/list.html',{'data':data})

def add_structure(request, id):
	if request.method=='POST':
		if id>0:
			struct=Structure.objects.get(id=id)
		else:
			struct=Structure()
		struct.denomination=request.POST.get('denomination')
		struct.email=request.POST.get('email')
		struct.telephone=request.POST.get('telephone')
		struct.bp=request.POST.get('bp')
		struct.grossiste=bool(request.POST.get('grossiste'))
		struct.save()
		return redirect('list_structure')

def delete_structure(request, id):
	struct=Structure.objects.get(id=id).delete()
	return redirect('list_structure')


