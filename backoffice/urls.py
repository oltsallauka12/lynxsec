from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/update/', views.update_profile_view, name='update_profile'),
    path('alerts/', views.alerts_view, name='alerts'),
    path('hosts/', views.host_list_view, name='host_list'),
    path('hosts/add/', views.add_host_view, name='add_host'),
    path('ids/', views.ids_list_view, name='ids_list'),
    path('ids/add/', views.add_ids_view, name='add_ids'),
]
