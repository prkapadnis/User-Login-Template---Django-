from django.contrib.auth.models import User
from django.db import reset_queries
from django.forms.forms import Form
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegister, UserUpdateForm, ProfileUpdateForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get(
            'username'), password=request.POST.get('password'))
        if user is None:
            messages.error(request, 'Invalid Username or Password')
            return redirect('/login')
        login(request, user)
        return redirect('/dashboard')
    return render(request, 'accounts/login-view.html', {})


@login_required
def dashboard(request):
    u_form = UserUpdateForm(request.user)
    p_form = ProfileUpdateForm(request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('/dashboard')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user)
    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'accounts/dashboard.html', context=context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    form = UserRegister()
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'Your account has been created! You are now able to log in')
            return redirect('/login')
    context = {'form': form}
    return render(request, "accounts/register-view.html", context=context)
