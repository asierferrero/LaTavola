from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegisterForm, LoginForm, ProfileForm
from .tokens import generate_token
from django.contrib.auth.decorators import login_required

User = get_user_model()

def main(request):
    return render(request, 'home.html', {})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['pasahitza']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')

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
    message = f"Egin klik esteka honetan zure kontua egiaztatzeko: {
        verification_url}"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.username])

def verify_view(request, user_id, token):
    user = User.objects.get(id=user_id)
    if user.token == token:
        user.is_active = True
        user.save()
        return render(request, 'verify.html', {'success': 'Zure kontua egiaztatu da'})
    else:
        return render(request, 'verify.html', {'error': 'Zure kontua ezin izan da egiaztatu'})
    

@login_required
def profile_view(request):
    user_profile = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save() 
            return redirect('profile')  
        else:
            print(form.errors) 
    else:
        form = ProfileForm(instance=user_profile) 

    return render(request, 'profile.html', {'user_profile': user_profile, 'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
