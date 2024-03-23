from django.contrib import admin
from django.urls import path,include, re_path
from . import views, ASE_BackC, DPI_Back, ADI_Back, ComptabiliteC
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.index, name='espace_client'),

    path("list_asi", views.list_asi, name='list_asi'),
    path("get_asi/<int:id>", views.get_asi, name='get_asi'),
    path("change_produit_amm", views.change_produit_amm, name='change_produit_amm'),
    path("change_produit_stupefiant", views.change_produit_stupefiant, name='change_produit_stupefiant'),
    path("note_stupefiant/<int:id>", views.note_stupefiant, name='note_stupefiant'),
    path("manage_asi_list_produit/<int:id>", views.asi_list_produit, name='manage_asi_list_produit'),
    path("treat_asi/<int:id>", views.treat_asi, name='treat_asi'),
    path("print_asi/<int:id>", views.print_asi, name='print_asi'),
    path("print_asi_stupefiant/<int:id>", views.print_asi_stupefiant, name='print_asi_stupefiant'),
    path("renvoie_modification_asi/", views.renvoie_modification, name='renvoie_modification_asi'),

    path("paiement", ComptabiliteC.paiement, name='paiement'),
    path("paiement_group", ComptabiliteC.paiement_group, name='paiement_group'),
    path("list_paiement", ComptabiliteC.list_paiement, name='list_paiement'),
    path("list_impaye_structure", ComptabiliteC.list_impaye_structure, name='list_impaye_structure'),
    path("list_impaye_groupby__structure/<str:structure_name>", ComptabiliteC.list_impaye_groupby__structure, name='list_impaye_groupby__structure'),
    path("list_goup_facture/<str:structure_name>", ComptabiliteC.list_goup_facture, name='list_goup_facture'),
    path("create_groupe_facture/<int:id_structure>", ComptabiliteC.create_groupe_facture, name='create_groupe_facture'),
    path("print_group_facture/<int:id_groupe_facture>", ComptabiliteC.print_group_facture, name='print_group_facture'),


    path("list_ase", ASE_BackC.list, name='list_ase'),
    path("manage_ase_list_produit/<int:id>", ASE_BackC.list_produit, name='manage_ase_list_produit'),
    path("treat_ase/<int:id>", ASE_BackC.treat, name='treat_ase'),
    path("print_ase/<int:id>", ASE_BackC.print_ase, name='print_ase'),
    path("renvoie_modification_ase/", ASE_BackC.renvoie_modification, name='renvoie_modification_ase'),

    path("list_dpi", DPI_Back.list, name='list_dpi'),
    path("manage_dpi_list_produit/<int:id>", DPI_Back.list_produit, name='manage_dpi_list_produit'),
    path("treat_dpi/<int:id>", DPI_Back.treat, name='treat_dpi'),
    path("print_dpi/<int:id>", DPI_Back.print_dpi, name='print_dpi'),
    path("renvoie_modification_dpi/", DPI_Back.renvoie_modification, name='renvoie_modification_dpi'),

    path("list_adi", ADI_Back.list, name='list_adi'),
    path("details_adi/<int:id>", ADI_Back.details, name='details_adi'),
    path("treat_adi/<int:id>", ADI_Back.treat, name='treat_adi'),
    path("print_adi/<int:id>", ADI_Back.print_adi, name='print_adi'),
    path("renvoie_modification_adi/", ADI_Back.renvoie_modification, name='renvoie_modification_adi'),

    
]
