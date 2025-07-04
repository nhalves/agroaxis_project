from django.urls import path
from . import views

app_name = 'herd'

urlpatterns = [
    path('', views.animal_list, name='animal_list'),
    path('add/', views.animal_create, name='animal_create'),
    path('<int:pk>/edit/', views.animal_update, name='animal_update'),
    path('<int:pk>/', views.animal_detail, name='animal_detail'),
    path('<int:animal_pk>/reproductive-event/add/', views.reproductive_event_create, name='reproductive_event_create'),
    path('reproductive-event/<int:pk>/edit/', views.reproductive_event_update, name='reproductive_event_update'),
    path('<int:animal_pk>/health-event/add/', views.health_event_create, name='health_event_create'),
    path('health-event/<int:pk>/edit/', views.health_event_update, name='health_event_update'),
]
