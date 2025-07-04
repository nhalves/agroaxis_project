from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('', views.transaction_list, name='transaction_list'),
    path('add/', views.transaction_create, name='transaction_create'),
    path('<int:pk>/edit/', views.transaction_update, name='transaction_update'),
    path('report/', views.finance_report, name='finance_report'),
]
