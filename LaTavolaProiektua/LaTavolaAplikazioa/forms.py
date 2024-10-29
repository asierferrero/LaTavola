from django import forms
from .models import Erabiltzailea
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sartu zure emaila',
            'required': True
        })
    )
    pasahitza = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sartu zure pasahitza',
            'required': True
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        pasahitza = cleaned_data.get("pasahitza")

        if username and pasahitza:
            try:
                user = User.objects.get(username=username)
                if not user.check_password(pasahitza):
                    self.add_error('', "Zerbait txarto sartu duzu.") 
                elif not user.is_active:
                    self.add_error(None, "Zure kontua ez dago egiaztatuta.")
            except User.DoesNotExist:
                self.add_error('', "Zerbait txarto sartu duzu.")

        return cleaned_data


class RegisterForm(forms.ModelForm):
    pasahitza = forms.CharField(
        label='Pasahitza',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sartu zure pasahitza',
            'required': True
        })
    )

    class Meta:
        model = Erabiltzailea
        fields = ['izena', 'abizena', 'jaiotze_data', 'username', 'pasahitza']
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
            'username': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sartu zure emaila',
                'required': True
            }),
        }

    def clean_email(self):
        username = self.cleaned_data.get('username')
        if Erabiltzailea.objects.filter(username=username).exists():
            raise forms.ValidationError("Email hau erregistratuta dago.")
        return username
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Erabiltzailea
        fields = ['izena', 'abizena', 'username', 'jaiotze_data']
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
            'username': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sartu zure emaila',
                'required': True
            }),
            'jaiotze_data': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Jaiotze data',
                'type': 'date',
                'required': True
            }),
        }