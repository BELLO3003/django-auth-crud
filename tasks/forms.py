from django.forms import ModelForm
from .models import Task
from django.db import models
from django import forms

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task #Especificar en que modelo va a estar basado este formulario
        fields = ['title', 'description', 'important']
        widgets = { #Dar estilos de Bootstrap a los elementos del Form 
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Titulo'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Descripcion'}),
            'important': forms.CheckboxInput()
        }