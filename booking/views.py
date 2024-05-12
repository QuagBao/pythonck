from django.shortcuts import render

# Create your views here.
def home(request):
    context = {}
    return render(request, 'booking/home.html', context)

def login(request):
    context={}
    return render(request, 'booking/login.html', context)
