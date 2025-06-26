# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import CustomUser
from games.models import Game
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/page/home')  # redirect to home after register
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/page/home')  # This should match your game page URL name
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'users/login.html')


@login_required
def home_view(request):
    return render(request, 'users/home.html')

def dashboard_view(request):
    games = Game.objects.all()
    return render(request, 'games/dashboard.html', {'games': games})

def logout_view(request):
    logout(request)
    return render(request, 'users/logout.html')  # Renders the logout page

