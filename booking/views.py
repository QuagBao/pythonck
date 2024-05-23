from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.
def home(request):
    movies = Movie.objects.all()
    context = {
        'movies':movies,
        'is_logged_in': request.user.is_authenticated,
        'messages': messages.get_messages(request),  # Truyền danh sách các message vào context
    }
    return render(request, 'booking/home.html', context)

def loginPage(request):
    if request.method == 'POST':
        username1 = request.POST.get('username')
        password1 = request.POST.get('password')
        user = authenticate(request, username=username1, password=password1)
        if user is not None:
            login(request, user)
            messages.success(request, 'Đăng nhập thành công')
            return redirect('home')
        else:
            messages.error(request, 'Tài khoản hoặc mặt khẩu chưa đúng. Hãy nhập lại!!')
    else:
        if request.user.is_authenticated:
            return redirect('home')
    
    context = {
        'messages': messages.get_messages(request),  # Truyền danh sách các message vào context
    }
    return render(request, 'booking/login.html', context)

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tạo tài khoản thành công! Hãy đăng nhập.')
            return redirect('loginPage')  # Chuyển hướng đến trang đăng nhập sau khi đăng ký thành công
    context = {
        'form': form,
        'messages': messages.get_messages(request),
    }
    return render(request, 'booking/register.html', context)

def logoutPage(request):
    logout(request)
    messages.success(request, 'Bạn đã đăng xuất thành công.')
    return redirect('home')
def movie_detail(request):
    context={}
    return render(request, 'booking/movie_detail.html', context)