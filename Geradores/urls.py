from django.urls import path
from . import views
from .views import salvar, editar,update,deletar,Geradoreditar,Geradorupdate


urlpatterns = [
    path('', views.list, name='geradores'),
    path('cadastrar/', views.create, name='cadastrarGerador'),
    path('salvar/', salvar, name='salvarGerador'),
    path('editar/<int:id>', editar, name='editarGerador'),
    path('update/<int:id>', update, name='updateGerador'),
    path('deletar/<int:id>', deletar, name='deletarGerador'),
    path('Geradoreditar/<int:id>', Geradoreditar, name='Geradoreditar'),
    path('updateGerador_gerador/<int:id>', Geradorupdate, name='updateGerador_gerador'),
    
]
 
  