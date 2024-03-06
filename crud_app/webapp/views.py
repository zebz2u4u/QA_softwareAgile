from django.shortcuts import render, redirect
from .forms import CreateUser, LoginForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required
from .models import device_request, maintenance_request, other_request

def homePage(request):

    return render(request, 'webapp/index.html')


#- register view

def register(request):
    form = CreateUser()
    if request.method == "POST":
        form = CreateUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    
    context = {'form':form}
    return render(request, 'webapp/register.html', context=context)


def login(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)

                return redirect("dashboard")

    context = {'form':form}
    return render(request, 'webapp/login.html', context=context)


#dashboard
@login_required(login_url='login')
def dashboard(request):
    userDevice = device_request.objects.all()
    #userMaintainence = maintenance_request.objects.all()
    #userOther = other_request.objects.all()

    context = {'request':userDevice}

    return render(request, "webapp/dashboard.html", context=context)










def logout(request):
    auth.logout(request)
    return redirect("login")