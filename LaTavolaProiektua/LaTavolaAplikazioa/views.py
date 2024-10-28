from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegisterForm, LoginForm
from .models import Erabiltzailea
from .tokens import generate_token

# Create your views here.
def main(request):
    return render(request, 'home.html', {})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['pasahitza']

            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    form.add_error(None, "Zure kontua ez dago egiaztatuta. Mesedez, egiaztatu zure posta elektronikoa.")
            else:
                return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['pasahitza'])
            user.is_active = False  # Erabiltzailea ez dago aktibatuta emaila egiaztatu arte
            user.save()

            # Kontua egiaztatzeko emaila bidali
            send_verification_email(user)

            return render(request, 'register.html', {'form': form, 'success': 'Zure kontua egiaztatzeko mezu elektroniko bat bidali da helbide elektronikora'})
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def send_verification_email(user):
    token = generate_token(user)
    user.token = token
    user.save()
    verification_url = f"{settings.SITE_URL}/verify/{user.id}/{token}"
    subject = "Zure kontua egiaztatu"
    message = f"Egin klik esteka honetan zure kontua egiaztatzeko: {verification_url}"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
    
def verify_view(request, user_id, token):
    user = Erabiltzailea.objects.get(id=user_id)
    if user.token == token:
        user.is_active = True
        user.save()
        return render(request, 'verify.html', {'success': 'Zure kontua egiaztatu da'})
    else:
        return render(request, 'verify.html', {'error': 'Zure kontua ezin izan da egiaztatu'})
    
def profile_view(request):
    return render(request, 'profile.html', {})

def logout_view(request):
    logout(request)
    return redirect('home') 