from django.urls import path
from . import views
from .views import salvar, editar,update,deletar

urlpatterns = [
    path('', views.list, name='consumidores'),
    path('cadastrar/', views.create, name='cadastrarConsumidor'),
    path('salvar/', salvar, name='salvarConsum'),
    path('editar/<int:id>', editar, name='editarConsum'),
    path('update/<int:id>', update, name='updateConsum'),
    path('deletar/<int:id>', deletar, name='deletarConsum'),
]
 