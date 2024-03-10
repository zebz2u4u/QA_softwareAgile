from django.db import models

# Create your model

class Request(models.Model):
    REQUEST_TYPES = [
        ('DeviceRequest', 'Device Request'),
        ('MaintenanceRequest', 'Maintenance Request'),
        ('OtherRequest', 'Other'),
    ]

    # id = models.AutoField(primary_key=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    fullName = models.CharField(max_length=255, verbose_name="Full Name")
    workEmail = models.CharField(max_length=255, verbose_name="Work Email")
    lineManager = models.CharField(max_length=255, verbose_name="Line Manager")
    request = models.CharField(max_length=550)
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPES)

    def __str__(self):
        return f"{self.id} - {self.fullName}"