from django.shortcuts import render
from .models import *

# Create your views here.
def home(request):
    movies = Movie.objects.all()
    context = {'movies':movies}
    return render(request, 'booking/home.html', context)

def login(request):
    context={}
    return render(request, 'booking/login.html', context)
