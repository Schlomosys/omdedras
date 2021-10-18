from django.forms import ModelForm
from django import forms

from .models import Ordremission
from django.core.exceptions import ValidationError



class OrdremissionForm(ModelForm):
    
   # meta data for displaying a form
   class Meta:
      # model
      model = Ordremission

      # displaying fields
      fields = ['objetmission', 'datedepart', 'dateretour', 'adressemission', 'transport', 'adressehebergement', 'adresseemploye', 'fichier_an_one', 'fichier_an_two'] 
      labels = {'objetmission':'Objet de la mission','datedepart':'Date de départ', 'dateretour':'Date de retour', 'adressemission':'Adresse de la mission','transport': 'Moyens de transport','adressehebergement':'Adresse Hébergement','adresseemploye':'Adresse du demandeur', 'fichier_an_one':'Fichier Annexe 1', 'fichier_an_two':'Fichier Annexe 2'}
      widgets = {
        'datedepart': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        'dateretour': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        #'fichier_an_one':forms.FileInput(attrs={'accept': 'application/pdf', 'required':'required'})
      }  

 