from django.urls import path
from . import views

app_name = 'milk_quality'

urlpatterns = [
    path('', views.milk_quality_list, name='milk_quality_list'),
    path('add/', views.milk_quality_create, name='milk_quality_create'),
    path('<int:pk>/edit/', views.milk_quality_update, name='milk_quality_update'),
]
