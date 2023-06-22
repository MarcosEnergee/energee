from django.urls import path
from . import views
from .views import login,valida_login,sair


urlpatterns = [
    path('', views.login, name='login'),
    path('valida_login/', views.valida_login, name='valida_login'),
    path('sair/', views.sair, name='sair'),
]
 
  