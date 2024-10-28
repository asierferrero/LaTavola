from django.shortcuts import render,redirect
from django.contrib.auth import logout

# Create your views here.
def main(request):
    return render(request, 'home.html', {})

def sarrera(request):
    return render(request, 'sarrera.html', {})

def logout_view(request):
    logout(request)
    return redirect("/")