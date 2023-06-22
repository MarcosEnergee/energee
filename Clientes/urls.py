from django.urls import path
from . import views
#from .views import salvar, editar,update,deletar

urlpatterns = [
    path('', views.list, name='clientes'),
    path('cadastrar/', views.create, name='cadastrarCliente'),
    path('salvar/', views.salvar, name='salvarCli'),
    path('editar/<int:id>', views.editar, name='editarCli'),
    path('update/<int:id>', views.update, name='updateCli'),
    path('deletar/<int:id>', views.deletar, name='deletarCli'),
]
 