# forms.py
from django import forms
from .models import Erabiltzailea

class LoginForm(forms.ModelForm):
    class Meta:
        model = Erabiltzailea
        fields = ['email', 'pasahitza']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sartu zure emaila',
                'required': True
            }),
            'pasahitza': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sartu zure pasahitza',
                'required': True
            }),
        }

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Erabiltzailea
        fields = ['izena', 'abizena', 'jaiotze_data', 'email', 'pasahitza']
        widgets = {
            'izena': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sartu zure izena',
                'required': True
            }),
            'abizena': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sartu zure abizena',
                'required': True
            }),
            'jaiotze_data': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Jaiotze data (YYYY-MM-DD)',
                'type': 'date',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sartu zure emaila',
                'required': True
            }),
            'pasahitza': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sartu zure pasahitza',
                'required': True
            }),
        }
