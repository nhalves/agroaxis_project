from django.urls import path
from . import views

app_name = 'analysis'

urlpatterns = [
    path('', views.analysis_dashboard, name='analysis_dashboard'),
]
