from django.urls import path
from . import views

urlpatterns = [
    path('', views.relatorios, name='relatorios'),
    path('consumo/', views.consumo, name='consumo'),
    path('valores_consumidor/<int:uc>', views.valoresConsumidor, name='valores_consumidor'),
    path('geracao/', views.geracao, name='geracao'),
    path('injetado/', views.injetado, name='injetado'),
    path('armazenado_mensal/', views.armazenadoMes, name='armazenado_mensal'),
    path('armazenado_total/', views.armazenadoTotal, name='armazenado_total'),
    path('update_armazenados/<int:dist>', views.update_armazenados, name='update_armazenados'),
    path('remanescente/',views.ConsumoReman, name='remanescente'),
    path('check/',views.Check, name='check'),
    path('update/<str:ref>',views.update, name='editarconsumo'),
    path('atualizar/<int:id>',views.atualizar, name='atualizaConsumo'),
    path('alterar/<int:id>',views.Alterar, name='Alterarconsumo'),
    path('updateGerador/<str:ref>',views.updategeracao, name='editargeracao'),
    path('atualizaGerador/<int:id>',views.atualizaGerador, name='atualizaGerador'),
    path('Alterargerado/<int:id>',views.Alterargerado, name='Alterargerado'),
    path('grafico_relatorio/<str:uc>',views.grafico_relatorio, name='grafico_relatorio'),
    path('grafico_relatorio_celesc/<str:uc>',views.grafico_relatorio_celesc, name='grafico_relatorio_celesc'),
    path('AlimentaSelect/<str:cli>',views.AlimentaSelect, name='AlimentaSelect'),
    path('AlimentaSelectDist/<str:cli>',views.AlimentaSelectDist, name='AlimentaSelectDist'),
    path('liberar/',views.liberar_acesso, name='liberar'),
    path('alterar_acesso/<str:ref>',views.alterar_acesso, name='alterar_acesso'),
    path('salvar_acesso/<str:ref>',views.salvar_acesso, name='salvar_acesso'),
    

    
]