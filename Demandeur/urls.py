from django.contrib import admin
from django.urls import path,include, re_path

from . import views,StructureC

urlpatterns = [
    path("signin/", views.signin, name='demandeur_signin'),
    path("signup/", views.signup, name='demandeur_signup'),
    path("logout/", views.signout, name='demandeur_logout'),
    path("list/", views.list_demandeur, name='demandeur_list'),
    path("affect_structure/<int:id_demandeur>", views.affectation_structure, name='affect_structure'),
    path("state/<int:user_id>", views.change_state, name='change_state_demandeur'),
    path("structure/", StructureC.list_structure, name='list_structure'),
    path("add_stucture/<int:id>", StructureC.add_structure, name='add_structure'),
    path("delete_structure/<int:id>", StructureC.delete_structure, name='delete_structure'),
]
