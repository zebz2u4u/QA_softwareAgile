from django.contrib import admin

# Register your models here.

from . models import device_request, maintenance_request, other_request

admin.site.register(device_request)
admin.site.register(maintenance_request)
admin.site.register(other_request)
