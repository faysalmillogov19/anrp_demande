from django.urls import path,include, re_path
from . import views

urlpatterns = [
    path('asi/<int:id>', views.get_asi_recepice, name='recepice_asi'),
    path('ase/<int:id>', views.get_ase_recepice, name='recepice_ase'),
    path('dpi/<int:id>', views.get_dpi_recepice, name='recepice_dpi'),
    path('adi/<int:id>', views.get_adi_recepice, name='recepice_adi'),
]