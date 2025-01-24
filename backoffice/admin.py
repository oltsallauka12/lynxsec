from django.contrib import admin
from .models import ClientUser

@admin.register(ClientUser)
class ClientUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'company_name', 'phone', 'is_staff']
