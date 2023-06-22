from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.list, name='extracao'),
    path('areaconsumidor/', views.areaConsumidor, name='areaconsumidor'),
    path('extracao/<int:cli>', views.ConsumidorCopel, name='extracaoconsumidor'),
    path('extracaoG/<int:cli>', views.Gerador, name='extracaogerador'),

    path('extracaoA/<int:cli>', views.RelatorioAzulCopel, name='extracaoAzul'),
    path('areagerador/', views.areaGerador, name='areagerador'),
    path('areaazul/', views.areaAzul, name='areaazul'),
    path('FileExtracao/', views.uploadFile, name='FileExtracao'),
]

if settings.DEBUG: 
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root = settings.MEDIA_ROOT
    )