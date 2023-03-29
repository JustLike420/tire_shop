from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import login, logout
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'registered')
            return redirect('/')
        else:
            messages.error(request, 'error')
    else:
        form = UserRegisterForm()

    return render(request, "register.html", {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = UserLoginForm
    return render(request, "login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect('/')
