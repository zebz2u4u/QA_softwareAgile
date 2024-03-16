from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, CreateRequest, UpdateRequest
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import Request, Employee

def homePage(request):

    return render(request, 'webapp/index.html')

def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Assuming you have a 'login' url name
    else:
        form = CreateUserForm()
    return render(request, 'webapp/register.html', {'form': form})

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
    # Ensure that we only get requests related to the logged-in user's employee profile
    try:
        employee = request.user.employee
        requests = Request.objects.filter(employee=employee)
    except Employee.DoesNotExist:
        requests = []

    context = {'requests': requests}
    return render(request, "webapp/dashboard.html", context=context)

@login_required(login_url='login')
def createRecord(request):
    if request.method == "POST":
        form = CreateRequest(request.POST)
        if form.is_valid():
            # Save the form but don't commit to DB yet, so we can add the employee
            request_instance = form.save(commit=False)
            # Assuming the current user is the one making the request
            # Ensure there's an Employee instance related to the user
            try:
                employee = request.user.employee
                request_instance.employee = employee
                request_instance.save()
                return redirect("dashboard")
            except Employee.DoesNotExist:
                form.add_error(None, "Employee profile not found for the user.")
    else:
        form = CreateRequest()

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