from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('grafico_admin', views.grafico_admin, name='grafico_admin'),
]