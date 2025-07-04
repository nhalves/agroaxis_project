from django.urls import path
from . import views

app_name = 'utils'

urlpatterns = [
    path('useful-items/', views.useful_items_page, name='useful_items_page'),
]
