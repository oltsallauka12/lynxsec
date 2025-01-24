from django import forms
from .models import ClientUser
from .models import Host, IDS


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = ClientUser
        fields = ['company_name', 'phone']

class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = ['hostname', 'ip_address', 'os']
        widgets = {
            'os': forms.Select(choices=[('linux', 'Linux'), ('windows', 'Windows')]),
        }
        labels = {
            'hostname': 'Hostname',
            'ip_address': 'IP Address',
            'os': 'Operating System',
        }

class IDSForm(forms.ModelForm):
    class Meta:
        model = IDS
        fields = ['host', 'os', 'configuration']
        widgets = {
            'host': forms.Select(attrs={'class': 'form-control'}),
            'os': forms.Select(choices=[('linux', 'Linux'), ('windows', 'Windows')], attrs={'class': 'form-control'}),
            'configuration': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Suricata config as JSON'}),
        }
        labels = {
            'host': 'Select Host',
            'os': 'Operating System',
            'configuration': 'Suricata Configuration',
        }

class AddHostForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = ['hostname', 'ip_address', 'os', 'status']  # Adjust fields based on your model
        widgets = {
            'hostname': forms.TextInput(attrs={'class': 'form-control'}),
            'ip_address': forms.TextInput(attrs={'class': 'form-control'}),
            'os': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

class AddIDSForm(forms.ModelForm):
    class Meta:
        model = IDS
        fields = ['host', 'os', 'deployment_status', 'configuration']  # Adjust fields as needed
        widgets = {
            'host': forms.Select(attrs={'class': 'form-select'}),
            'os': forms.Select(attrs={'class': 'form-select'}),
            'deployment_status': forms.Select(attrs={'class': 'form-select'}),
            'configuration': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
class PasswordChangeForm(forms.ModelForm):
    class Meta:
        model = ClientUser
        fields = ['password']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'password': 'New Password',
        }