from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import *
import json
import random
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def home(request):
    movie_now_showing = Movie.objects.filter(status='now_showing')
    movie_coming_soon = Movie.objects.filter(status='coming_soon')

    context = {
        'movie_now_showing': movie_now_showing,
        'movie_coming_soon': movie_coming_soon,
        'is_logged_in': request.user.is_authenticated,
        'messages': messages.get_messages(request),  # Truyền danh sách các message vào context
    }
    return render(request, 'booking/home.html', context)

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    showtimes = Showtime.objects.filter(movie=movie)

    context = {
        'movie': movie,
        'showtimes': showtimes,
        'is_logged_in': request.user.is_authenticated,
    }

    return render(request, 'booking/movie_detail.html', context)
    
def loginPage(request):
    if request.method == 'POST':
        username1 = request.POST.get('username')
        password1 = request.POST.get('password')
        user = authenticate(request, username=username1, password=password1)
        if user is not None:
            login(request, user)
            messages.success(request, 'Đăng nhập thành công')
            if any([user.is_superuser, user.is_staff]):
                return redirect('/admin')  # Chuyển hướng đến trang admin
            else:
                return redirect('home')  # Chuyển hướng đến trang chủ
        else:
            messages.error(request, 'Tài khoản hoặc mặt khẩu chưa đúng. Hãy nhập lại!!')
    else:
        if request.user.is_authenticated:
            if any([request.user.is_superuser, request.user.is_staff]):
                return redirect('/admin')  # Chuyển hướng đến trang admin
            else:
                return redirect('home')  # Chuyển hướng đến trang chủ
    
    context = {
        'messages': messages.get_messages(request),  # Truyền danh sách các message vào context
    }
    return render(request, 'booking/login.html', context)

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        if get_user_model().objects.filter(username=username).exists():
            messages.error(request, 'Tên người dùng này đã được sử dụng. Vui lòng chọn tên khác.')
        else:    
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 != password2:
                messages.error(request, 'Mật khẩu không khớp. Vui lòng nhập lại.')
            else:
                users = get_user_model().objects.create_user(username=username, email=email, password=password1)
                messages.success(request, 'Đăng ký tài khoản thành công.')
                return redirect('loginPage')  # Redirect to the login page after successful registration
    context = {
        'messages': messages.get_messages(request),
    }
    return render(request, 'booking/register.html', context)

def logoutPage(request):
    logout(request)
    messages.success(request, 'Bạn đã đăng xuất thành công.')
    return redirect('home')

def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        keys = Movie.objects.filter(Q(title__icontains=searched.upper()) | Q(title__icontains=searched.lower()))
    context = {
        'messages': messages.get_messages(request),
        'is_logged_in': request.user.is_authenticated,
        "searched": searched, 
        "keys": keys
    }
    return render(request, 'booking/search.html', context)

def movie_seating_booking(request):
    
    context = {
    }
    return render(request, 'booking/movie_seating_booking.html', context)

def change_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password == confirm_password:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)  # To keep the user logged in
            messages.success(request, 'Mật khẩu đã được thay đổi thành công.')
            return redirect('home')
        else:
            messages.error(request, 'Mật khẩu không trùng khớp. Vui lòng thử lại.')
    context = {
        'messages': messages.get_messages(request),
        'is_logged_in': request.user.is_authenticated,
    }
    return render(request, 'booking/change_password.html',  context)
