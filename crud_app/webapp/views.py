from django.shortcuts import render

# Create views here


def homePage(request):

    return render(request, 'webapp/index.html')