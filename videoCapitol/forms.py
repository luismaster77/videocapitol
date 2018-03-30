# -*- coding: utf-8 -*-
from django import forms
from models import *
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    rut = forms.CharField(required=True)
    nombres = forms.CharField(required=True)
    apellidos = forms.CharField(required=True)
    direccion = forms.CharField(required=True)
    telefono = forms.CharField(required=True)
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'E-mail address'}))

    class Meta:
        model = User
        fields = ('nombres', 'apellidos', 'email', 'username', 'password1', 'password2')

def clean_email(self):
    email = self.cleaned_data["email"]
    try:
        User._default_manager.get(email=email)
    except User.DoesNotExist:
        return email
    raise forms.ValidationError('email duplicado')

#modificamos el metodo save() así podemos definir  user.is_active a False la primera vez que se registra
def save(self, commit=True):        
    user = super(RegistrationForm, self).save(commit=False)
    user.email = self.cleaned_data['email']
    if commit:
        user.is_active = False # No esta activo hasta que active el vínculo de verificacion
        user.save()

    return user