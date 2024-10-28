from django import forms
from .models import Erabiltzailea
from django.contrib.auth import get_user_model




User = get_user_model()

class LoginForm(forms.Form):
    email = forms.EmailField(
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
        email = cleaned_data.get("email")
        pasahitza = cleaned_data.get("pasahitza")

        if email and pasahitza:
            try:
                user = User.objects.get(email=email)
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
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Erabiltzailea.objects.filter(email=email).exists():
            raise forms.ValidationError("Email hau erregistratuta dago.")
        return email
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Erabiltzailea
        fields = ['izena', 'abizena', 'email', 'jaiotze_data']
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
            'email': forms.EmailInput(attrs={
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