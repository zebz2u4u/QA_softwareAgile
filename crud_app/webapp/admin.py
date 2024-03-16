from django.contrib import admin

# Register your models here.

from .models import Request, RequestUpdate, Employee

admin.site.register(Request)
admin.site.register(Employee)
admin.site.register(RequestUpdate)
