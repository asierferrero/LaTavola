from django import forms
from django.contrib.auth import get_user_model
from .models import Produktua, Alergeno
User = get_user_model()


class LoginForm(forms.Form):
    username = forms.EmailField(
        label='Emaila',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sartu zure emaila',
            'required': True
        })
    )
    password = forms.CharField(
        label='Pasahitza',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sartu zure pasahitza',
            'required': True
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            try:
                user = User.objects.get(username=username)
                if not user.check_password(password):
                    self.add_error('', "Zerbait txarto sartu duzu.")
                elif not user.is_active:
                    self.add_error(None, "Zure kontua ez dago egiaztatuta.")
            except User.DoesNotExist:
                self.add_error('', "Zerbait txarto sartu duzu.")

        return cleaned_data


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Izena',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sartu zure izena',
            'required': True
        })
    )
    last_name = forms.CharField(
        label='Abizena',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sartu zure abizena',
            'required': True
        })
    )
    username = forms.EmailField(
        label='Emaila',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sartu zure emaila',
            'required': True
        })
    )
    password = forms.CharField(
        label='Pasahitza',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sartu zure pasahitza',
            'required': True
        })
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Email hau erregistratuta dago.")
        return username


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sartu zure izena',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sartu zure abizena',
                'required': True
            }),
            'username': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sartu zure emaila',
                'required': True
            }),
        }

class ProduktuaForm(forms.ModelForm):
     class Meta:
        model = Produktua
        fields = ['izena', 'deskripzioa', 'alergenoak','mota' ,  'img', 'prezioa', 'stock']
        

class AlergenoForm(forms.ModelForm):
     class Meta:
        model = Alergeno
        fields = ['izena', 'img']
        
