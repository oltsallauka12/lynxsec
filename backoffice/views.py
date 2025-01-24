from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import IDS, Host, Network, SecurityAlert
from .forms import HostForm, IDSForm , AddHostForm, AddIDSForm, UpdateProfileForm
from django.contrib.auth.forms import PasswordChangeForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'backoffice/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    return render(request, 'backoffice/dashboard.html')

def update_profile_view(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was updated successfully!')
            return redirect('dashboard')
    else:
        form = UpdateProfileForm(instance=request.user)
    return render(request, 'backoffice/update_profile.html', {'form': form})

def alerts_view(request):
    alerts = SecurityAlert.objects.all().order_by('-created_at')
    return render(request, 'backoffice/alerts.html', {'alerts': alerts})

def host_list_view(request):
    hosts = Host.objects.all()
    return render(request, 'backoffice/hosts.html', {'hosts': hosts})

def deploy_ids_view(request):
    if request.method == 'POST':
        host_id = request.POST['host']
        network_id = request.POST['network']
        os = request.POST['os']
        # Create IDS instance
        ids = IDS.objects.create(
            host_id=host_id,
            network_id=network_id,
            os=os,
            status='pending'
        )
        # Run deployment script here (e.g., async task)
        return redirect('ids_list')
    hosts = Host.objects.all()
    networks = Network.objects.all()
    return render(request, 'backoffice/deploy_ids.html', {'hosts': hosts, 'networks': networks})

# List all hosts
def host_list_view(request):
    hosts = Host.objects.all()
    return render(request, 'backoffice/host_list.html', {'hosts': hosts})

# Add a new host
def add_host_view(request):
    if request.method == 'POST':
        form = HostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('host_list')
    else:
        form = HostForm()
    return render(request, 'backoffice/add_host.html', {'form': form})

def ids_list_view(request):
    ids_instances = IDS.objects.all()
    return render(request, 'backoffice/ids_list.html', {'ids_instances': ids_instances})

def add_ids_view(request):
    if request.method == 'POST':
        form = IDSForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ids_list')  # Redirect to IDS list view after saving
    else:
        form = IDSForm()
    return render(request, 'backoffice/add_ids.html', {'form': form})

def host_list_view(request):
    hosts = Host.objects.all()
    form = AddHostForm()

    if request.method == 'POST':
        form = AddHostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('host_list')  # Redirect to the host list after adding the host

    return render(request, 'backoffice/host_list.html', {'hosts': hosts, 'form': form})


def ids_list_view(request):
    ids_instances = IDS.objects.select_related('host').all()
    form = AddIDSForm()

    if request.method == 'POST':
        form = AddIDSForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ids_list')  # Redirect back to the IDS list

    return render(request, 'backoffice/ids_list.html', {'ids_instances': ids_instances, 'form': form})
def update_profile_view(request):
    user = request.user
    profile_form = UpdateProfileForm(instance=user)

    if request.method == 'POST':
        if 'update_profile' in request.POST:  # Check which form was submitted
            profile_form = UpdateProfileForm(request.POST, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Your profile has been updated.")
                return redirect('update_profile')
        elif 'change_password' in request.POST:  # Check for password change submission
            password_form = PasswordChangeForm(user=user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, user)  # Keep the user logged in after password change
                messages.success(request, "Your password has been updated.")
                return redirect('update_profile')
            else:
                messages.error(request, "Please correct the errors below.")

    password_form = PasswordChangeForm(user=user)
    return render(request, 'backoffice/update_profile.html', {
        'profile_form': profile_form,
        'password_form': password_form
    })