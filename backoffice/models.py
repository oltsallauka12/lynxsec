from django.contrib.auth.models import AbstractUser
from django.db import models

class ClientUser(AbstractUser):
    company_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username
    
class SecurityAlert(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Host(models.Model):
    hostname = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    os = models.CharField(max_length=50, choices=[('linux', 'Linux'), ('windows', 'Windows')])
    status = models.CharField(max_length=20, default='inactive', choices=[('active', 'Active'), ('inactive', 'Inactive')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.hostname

class Network(models.Model):
    name = models.CharField(max_length=255)
    cidr = models.CharField(max_length=50)  # e.g., 192.168.1.0/24
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.cidr})"
    
class IDS(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name="ids_instances")
    deployment_status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('deployed', 'Deployed'), ('failed', 'Failed')],
        default='pending'
    )
    os = models.CharField(max_length=50, choices=[('linux', 'Linux'), ('windows', 'Windows')])
    configuration = models.JSONField(blank=True, null=True)  # Store deployment settings here
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"IDS on {self.host.hostname} - {self.deployment_status}"
    
class EDR(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name='edr_instances')
    os = models.CharField(max_length=50, choices=[('linux', 'Linux'), ('windows', 'Windows')])
    status = models.CharField(max_length=20, default='pending', choices=[('pending', 'Pending'), ('deployed', 'Deployed'), ('failed', 'Failed')])
    last_health_check = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"EDR on {self.host.hostname}"
