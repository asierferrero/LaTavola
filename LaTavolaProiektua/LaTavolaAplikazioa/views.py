from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse, Http404
from .forms import RegisterForm, LoginForm, ProfileForm, ProduktuaForm, AlergenoForm,ChangePasswordForm, IritziaForm
from .models import Produktua, Alergeno, T2Product, Iritzia
from .serializers import ProduktuakSerializers, T2ProduktuakSerializer, T2AlergenoSerializer
from .import consume
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token

User = get_user_model()


def main(request):
    return render(request, 'home.html', {})

@login_required
def admin_home_view(request):
    if not request.user.is_staff:
        return redirect('home')
    
    user_profile = request.user  # Obtener el perfil del usuario
    
    # Obtener los datos necesarios para el gráfico
    productos = Produktua.objects.all()
    nombres = [producto.izena for producto in productos]
    stock = [producto.stock for producto in productos]
    precios = [float(producto.prezioa) for producto in productos]
    
    return render(request, 'admin_home.html', {
        'user_profile': user_profile,
        'nombres': nombres,
        'stock': stock,
        'precios': precios,
    })

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

def pasahitza_aldatu_view(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            Email = form.cleaned_data['Emaila']
            send_password_email(Email)
            return render(request, 'login.html', {'form': form})
    else:
        form = ChangePasswordForm()
    return render(request,'login.html',{'form': form})


def send_password_email(Email):
    try:
        verification_url = f"{settings.SITE_URL}/verify/{"user.id"}/"#hay que cambiar el user id
        subject = "Zure kontua egiaztatu"
        message = f"Egin klik esteka honetan zure kontua egiaztatzeko: {
            verification_url}"
        send_mail(subject, message, settings.EMAIL_HOST_USER, [Email])
    except Exception as e:
        print(f"Errorea emaila bidaltzerakoan: {e}")

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
            return render(request, 'register.html', {'form': form, 'error': 'Ezin izan da zure kontua egiaztatzeko mezu elektroniko bat bidali'})
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def send_verification_email(user):
    try:
        verification_url = f"{settings.SITE_URL}/verify/{user.id}/"
        subject = "Zure kontua egiaztatu"
        message = f"Egin klik esteka honetan zure kontua egiaztatzeko: {
            verification_url}"
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.username])
    except Exception as e:
        print(f"Errorea emaila bidaltzerakoan: {e}")


def verify_view(request, id):
    try:
        user = User.objects.get(id=id)
        user.is_active = True
        user.save()

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        return render(request, 'verify.html', {'success': 'Zure kontua egiaztatu da'})
    except Exception as e:
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

  
def saskia(request):
    return render(request, 'saskia.html', {})
  

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
    
    if produktuak.img:
        produktuak.img.delete(save=False) 
        
    if request.method == "POST":
        produktuak.delete()
        return redirect('produktuak-list')
    
@login_required
def produktuak_edit(request, id):
    if not request.user.is_staff:
        return redirect('home')
    
    produktuak = get_object_or_404(Produktua, id=id)
    
    if request.method == "POST":
        form = ProduktuaForm(request.POST, request.FILES, instance=produktuak)
        if form.is_valid():
            form.save()
            return redirect('produktuak-list')  # Redirigir a la lista de productos
    else:
        form = ProduktuaForm(instance=produktuak)
    
    return render(request, 'produktua_new.html', {'form': form, 'produktuak': produktuak})

@login_required
def bezeroak_delete(request, id):
    
    if not request.user.is_staff:
        return redirect('home')
    
    bezeroak = get_object_or_404(User, id=id)
    
    if request.method == "POST":
        bezeroak.delete()
        return redirect('bezeroak-list')
    

@login_required
def bezero_edit(request, id):
    if not request.user.is_staff:
        return redirect('home')

    user = get_object_or_404(User, id=id)

    if request.method == "POST":
        is_staff = request.POST.get('is_staff') == 'on'
        user.is_staff = is_staff 
        user.save()
        return redirect('bezeroak-list')

    return render(request, 'bezero_edit.html', {'user': user})

@login_required
def admin_alergenoak_list(request):
    if not request.user.is_staff:
        return redirect('home')
    
    query = request.GET.get('q')
    if query:
        alergenoak_list = Alergeno.objects.filter(
            Q(izena__icontains=query)
        )
    else:
        alergenoak_list = Alergeno.objects.all()
    return render(request, 'alergeno_zerrenda.html', {'alergenoak_list': alergenoak_list})


@login_required
def alergenoak_delete(request, id):
    
    if not request.user.is_staff:
        return redirect('home')
    
    alergenoak = get_object_or_404(Alergeno, id=id)
    
    if alergenoak.img:
        alergenoak.img.delete(save=False) 
        
    if request.method == "POST":
        alergenoak.delete()
        return redirect('alergeno-list')
    

@login_required
def alergenoa_new(request):
    if not request.user.is_staff:
        return redirect('home')
    
    if request.method == 'POST':
        form = AlergenoForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()  
            return redirect('alergeno-list')
    else:
        form = AlergenoForm()
    
    return render(request, 'alergenoa_new.html', {'form': form})


@login_required
def alergenoak_edit(request, id):
    if not request.user.is_staff:
        return redirect('home')
    
    alergenoak = get_object_or_404(Alergeno, id=id)
    
    if request.method == "POST":
        form = AlergenoForm(request.POST, request.FILES, instance=alergenoak)
        if form.is_valid():
            form.save()
            return redirect('alergeno-list')  # Redirigir a la lista de productos
    else:
        form = AlergenoForm(instance=alergenoak)
    
    return render(request, 'alergenoa_new.html', {'form': form, 'produktuak': alergenoak})


class Produktuak_APIView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        produktuak = Produktua.objects.prefetch_related('alergenoak').all()  # Produktuak bakoitzaren alergenoekin erlazionatu
        serializer = ProduktuakSerializers(produktuak, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProduktuakSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Produktuak_APIView_Detail(APIView):
    def get_object(self, pk):
        try:
            return Produktua.objects.get(pk=pk)
        except Produktua.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        produktua = self.get_object(pk)
        serializer = ProduktuakSerializers(produktua)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        produktua = self.get_object(pk)
        serializer = ProduktuakSerializers(produktua, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        produktua = self.get_object(pk)
        produktua.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#TODO terminar las funciones para consumir el REST API cuando el grupo de Alberdi tenga terminado el API
class T2Consume_API(APIView):
    def get(self, request, format=None, *args, **kwargs):
        produktuak = requests.get('http://192.168.73.26:8000/v1/product')
        serializer = T2ProduktuakSerializer(produktuak, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = T2ProduktuakSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class T2Consume_APIView_Detail(APIView):
    def get_object(self, pk,request):
        try:
            return T2Product.objects.get(pk=pk)
        except Produktua.DoesNotExist:
            raise Http404


@login_required
def iritzia_sartu(request):
    if request.method == 'POST':
        form = IritziaForm(request.POST)
        if form.is_valid():
            opinion = form.save(commit=False)  
            opinion.erabiltzailea = request.user     
            opinion.save()                     
            return redirect('home')
    else:
        form = IritziaForm()
    
    return render(request, 'iritzia_sartu.html', {'form': form})
        

@login_required
def order_confirmation(request):
    user_profile = request.user
    return render(request, 'order_confirmation.html', {'user_profile': user_profile})


@login_required
def admin_iritziak_list(request):
    if not request.user.is_staff:
        return redirect('home')
    
    query = request.GET.get('q')  # Gets the search input
    if query:
        # Filters the name based on the input
        iritzia_list = Iritzia.objects.filter(
            Q(izena__icontains=query)
        )
    else:
        # If no query, display all items
        iritzia_list = Iritzia.objects.all()
    
    return render(request, 'iritzia_zerrenda.html', {'iritzia_list': iritzia_list})


@login_required
def iritziak_delete(request, id):
    if not request.user.is_staff:
        return redirect('home')
    
    iritziak = get_object_or_404(Iritzia, id=id) 

    if request.method == "POST":
        iritziak.delete() 
        return redirect('iritziak-list') 

