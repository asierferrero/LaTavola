from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm

# Create your views here.


def main(request):
    return render(request, 'home.html', {})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid:
            login = form.save()
            login.save()
        return redirect('home')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid:
            register = form.save()
            register.save()
        return redirect('home')
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
