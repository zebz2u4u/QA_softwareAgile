from django.shortcuts import render, redirect
from .forms import CreateUser, LoginForm, CreateRequest, UpdateRequest

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required
from . models import Request


def homePage(request):

    return render(request, 'webapp/index.html')

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

@login_required(login_url='login')
def dashboard(request):
    requests = Request.objects.all()

    context = {'requests':requests}

    return render(request, "webapp/dashboard.html", context=context)

@login_required(login_url='login')
def createRecord(request):
    form = CreateRequest()
    if request.method == "POST":
        form = CreateRequest(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    context = {'form': form}
    return render(request, 'webapp/create-record.html', context=context)

@login_required(login_url='login')
def updateRecord(request, pk):
    requestId = Request.objects.get(id=pk)
    form = UpdateRequest(instance=requestId)
    if request.method == "POST":
        form = UpdateRequest(request.POST, instance=requestId)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    context = {'form': form}
    return render(request, 'webapp/update-record.html', context=context)

@login_required(login_url='login')
def viewRecord(request, pk):
    requestId = Request.objects.get(id=pk)
    context = {'request': requestId}
    return render(request, 'webapp/view-record.html', context=context)

@login_required(login_url='login')
def deleteRecord(request, pk):
    requestId = Request.objects.get(id=pk)
    requestId.delete()
    return redirect("dashboard")

def logout(request):
    auth.logout(request)
    return redirect("login")