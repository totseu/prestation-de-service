from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class ClientRegistrationForm(UserCreationForm):

    class Meta:
        model = User

        fields = [
            'nom',
            'prenom',
            'email',
            'age',
            'sexe',
            'password1',
            'password2',
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'client'

        if commit:
            user.save()

        return user


class PrestataireRegisterForm(UserCreationForm):

    class Meta:
        model = User

        fields = [
            'nom',
            'prenom',
            'email',
            'age',
            'sexe',
            'photo_profil',
            'photo_cni',
            'certificat',
            'fonction',
            'password1',
            'password2',
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'prestataire'

        if commit:
            user.save()

        return user