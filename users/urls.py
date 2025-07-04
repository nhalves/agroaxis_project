from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    # URLs de autenticação
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),

    # URLs de gestão de produtores (Admin)
    path('producers/', views.producer_list, name='producer_list'),
    path('producers/add/', views.producer_create, name='producer_create'),
    path('producers/<int:pk>/edit/', views.producer_update, name='producer_update'),
    path('producers/<int:pk>/impersonate/', views.impersonate_producer, name='impersonate_producer'),
    path('producers/<int:pk>/toggle-status/', views.toggle_producer_status, name='toggle_producer_status'),
]
