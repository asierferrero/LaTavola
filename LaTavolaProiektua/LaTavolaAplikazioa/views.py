from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegisterForm, LoginForm, ProfileForm, ProduktuaForm
from .models import Produktua
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.db.models import Q

User = get_user_model()

def main(request):
    return render(request, 'home.html', {})

@login_required
def admin_home_view(request):
    if not request.user.is_staff:
        return redirect('home')
    
    user_profile = User.objects.get(id=request.user.id)
    return render(request, 'admin_home.html', {'user_profile': user_profile})

@login_required
def admin_bezeroak_list(request):
    if not request.user.is_staff:
        return redirect('home')
    
    query = request.GET.get('q')
    if query:
        bezero_list = User.objects.filter(
            Q(username__icontains=query)
        )
    else:
        bezero_list = User.objects.all()
    return render(request, 'bezero_zerrenda.html', {'bezero_list': bezero_list})

@login_required
def admin_produktuak_list(request):
    if not request.user.is_staff:
        return redirect('home')
    
    query = request.GET.get('q')  # Obtiene el name del input
    if query:
        # Filtra el nombre segun el input metido
        produktu_list = Produktua.objects.filter(
            Q(izena__icontains=query)
        )
    else:
        # Si no lo encuentra aparece toda la lista
        produktu_list = Produktua.objects.all()
    
    return render(request, 'produktu_zerrenda.html', {'produktu_list': produktu_list})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    if user.is_staff:
                        return redirect('admin_home')
                    else:
                        return redirect('home')

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False  # Erabiltzailea ez dago aktibatuta emaila egiaztatu arte
            user.save()

            # Kontua egiaztatzeko emaila bidali
            send_verification_email(user)

            return render(request, 'register.html', {'form': form, 'success': 'Zure kontua egiaztatzeko mezu elektroniko bat bidali da helbide elektronikora'})
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def send_verification_email(user):
    verification_url = f"{settings.SITE_URL}/verify/{user.id}/{user.username}/"
    subject = "Zure kontua egiaztatu"
    message = f"Egin klik esteka honetan zure kontua egiaztatzeko: {verification_url}"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.username])


def verify_view(request, id, username):
    user = User.objects.get(id=id)
    
    if user.username == username:
        user.is_active = True
        user.save()
        
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        
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

@login_required
def produktua_new(request):
    if not request.user.is_staff:
        return redirect('home')
    
    if request.method == 'POST':
        form = ProduktuaForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()  
            return redirect('produktuak-list')
    else:
        form = ProduktuaForm()
    
    return render(request, 'produktua_new.html', {'form': form})

@login_required
def produktuak_delete(request, id):
    
    if not request.user.is_staff:
        return redirect('home')
    
    produktuak = get_object_or_404(Produktua, id=id)
    if request.method == "POST":
        produktuak.delete()
        return redirect('produktuak-list')