from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def home(request):
    context = {}
    return render(request, 'booking/home.html', context)

def login(request):
    context={}
    return render(request, 'booking/login.html', context)

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'booking/register.html', context)
