from django.contrib import admin
from django.urls import path,include, re_path

from . import views

urlpatterns = [
    path("add/<int:id_demande>", views.add, name='add_adi'),

]
