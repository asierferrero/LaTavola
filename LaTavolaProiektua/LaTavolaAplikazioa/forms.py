from django import forms
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
    password = forms.CharField(
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
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
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
            'password': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sartu zure pasahitza',
                'type': 'password',
                'required': True
            }),
        }

    def clean_email(self):
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
