import requests
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegisterForm, LoginForm, ProfileForm
from .models import Produktua
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProduktuakSerializers
from rest_framework import status
from django.http import Http404

User = get_user_model()


def main(request):
    if request.method == 'GET':
        # REST API-ra GET eskaera egin
        # URL hau aldatu beharko da
        response = requests.get('http://127.0.0.1:8000/api/produktuak/')

        if response.status_code == 200:
            items = response.json()  # Erantzuna JSON formatura bihurtu

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse(items, safe=False)
            else:
                context = {'menu_items': items}
                return render(request, 'home.html', context)
        else:
            return JsonResponse({'error': 'APItik datuak lortzean errorea gertatu da'}, status=500)


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
    # REST API-ra GET eskaera egin
    # URL hau aldatu beharko da
    response = requests.get('http://127.0.0.1:8000/api/produktuak/')

    if response.status_code == 200:
        items = response.json()  # Erantzuna JSON formatura bihurtu

        if request.method == 'GET':
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse(items, safe=False)
            else:
                context = {'menu_items': items}
                return render(request, 'saskia.html', context)
    else:
        return JsonResponse({'error': 'APItik datuak lortzean errorea gertatu da'}, status=500)


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
