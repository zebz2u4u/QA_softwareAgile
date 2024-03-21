from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUserForm, LoginForm, CreateRequest, UpdateRequest, RequestUpdateForm
from django.contrib.auth.models import auth
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from .models import Request, Employee, RequestUpdate
from django.contrib import messages

# create view here. Will need views for homepage, dashboard, login, various forms etc

def homePage(request):

    return render(request, "webapp/index.html")

def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You're registered!")
            return redirect('login')
    else:
        form = CreateUserForm()
    
    context = {'form': form}
    return render(request, "webapp/register.html", context=context)

def login(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                # Check if the user is an admin
                if user.is_staff:
                    return redirect("admin-dashboard")  # Redirect to the admin dashboard
                else:
                    return redirect("dashboard")  # Redirect to the general dashboard

    context = {'form': form}
    return render(request, "webapp/login.html", context=context)

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

@staff_member_required
def adminDashboard(request):
    all_requests = Request.objects.all().order_by('-dateCreated')
    context = {'all_requests': all_requests}
    return render(request, "webapp/admin-dashboard.html", context=context)

@staff_member_required
def adminUpdateRequest(request, pk):
    requestID = get_object_or_404(Request, pk=pk)
    if request.method == 'POST':
        form = RequestUpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.request = requestID
            update.save()
            messages.success(request, "Request update sent")
            return redirect("admin-dashboard")
    else:
        form = RequestUpdateForm()
    
    context = {'form': form, 'request': requestID}
    return render(request, "webapp/admin-updates.html", context=context)

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
                messages.success(request, "Record created successfully.")
                return redirect("dashboard")
            except Employee.DoesNotExist:
                form.add_error(None, "Employee profile not found for the user.")
    else:
        form = CreateRequest()

    context = {'form': form}
    return render(request, "webapp/create-record.html", context=context)

@login_required(login_url='login')
def updateRecord(request, pk):
    requestId = Request.objects.get(id=pk)
    form = UpdateRequest(instance=requestId)
    if request.method == "POST":
        form = UpdateRequest(request.POST, instance=requestId)
        if form.is_valid():
            form.save()
            messages.success(request, "Request updated successfully.")
            return redirect("dashboard")
    context = {'form': form}
    return render(request, "webapp/update-record.html", context=context)

@login_required(login_url='login')
def viewRecord(request, pk):
    requestId = Request.objects.get(id=pk)
    isAdmin = request.user.is_staff
    context = {'request': requestId, 'isAdmin': isAdmin}
    return render(request, "webapp/view-record.html", context=context)

@login_required(login_url='login')
def deleteRecord(request, pk):
    requestId = Request.objects.get(id=pk)

    if request.method == "POST":
        requestId.delete()
        messages.success(request, "Request deleted successfully.")
        return redirect("dashboard")
    else:
        return render(request, "webapp/confirm-delete.html", {'request': requestId})

def logout(request):
    auth.logout(request)
    messages.success(request, "See you soon!")
    return redirect("login")