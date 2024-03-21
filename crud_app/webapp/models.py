from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings 

# Email validation, make sure that only emails ending with @arm are valid
email_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9_.+-]+@arm\.com$',
    message="Email must be a valid email address ending with @arm.com.",
)

class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fullName = models.CharField(max_length=255, verbose_name="Full Name")
    workEmail = models.CharField(max_length=255, verbose_name="Work Email", validators=[email_validator])
    lineManager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='line_managed')

    def __str__(self):
        return self.fullName

class Request(models.Model):
    REQUEST_TYPES = [
        ('DeviceRequest', 'Device Request'),
        ('MaintenanceRequest', 'Maintenance Request'),
        ('OtherRequest', 'Other'),
    ]

    dateCreated = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, related_name='requests')
    request = models.CharField(max_length=550)
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPES, verbose_name="Request Type")

    def __str__(self):
        return f"{self.id} - {self.employee.fullName}'s request"

class RequestUpdate(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='updates')
    update_date = models.DateTimeField(auto_now_add=True)
    update_text = models.TextField()

    def __str__(self):
        return f"Update for Request ID {self.request.id} on {self.update_date}"