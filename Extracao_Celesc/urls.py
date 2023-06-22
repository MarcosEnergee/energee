from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('extracao_celesc/<int:cli>', views.CelescConsumidor, name='extracao_celesc'),
    path('extracao_gerador_celesc/<int:cli>', views.CelescGerador, name='extracao_gerador_celesc'),
    path('extracaoAzulCelesc/<int:cli>', views.RelatorioAzulCelesc, name='extracaoAzulCelesc'),
]

if settings.DEBUG: 
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root = settings.MEDIA_ROOT
    )