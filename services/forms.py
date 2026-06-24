# services/forms.py
from django import forms
from .models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['titre', 'description', 'prix', 'categorie']
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex : Création logo professionnel'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Décrivez votre service en détail...'
            }),
            'prix': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Prix en FCFA'
            }),
            'categorie': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex : Design, Développement web...'
            }),
        }