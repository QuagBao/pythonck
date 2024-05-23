from django.shortcuts import render

# Create your views here.
def home(request):
    context = {}
    return render(request, 'booking/home.html', context)

def login(request):
    context={}
    return render(request, 'booking/login.html', context)

def movie_detail(request):
    context={}
    return render(request, 'booking/movie_detail.html', context)