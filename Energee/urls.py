from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('Dashboard.urls')),
    path('admin/', admin.site.urls),
    path('geradores/', include('Geradores.urls')),
    path('consumidores/', include('Consumidores.urls')),
    path('relatorios/', include('Relatorios.urls')),
    path('extracao/', include('Extracao.urls')),
    path('extracao_celesc/', include('Extracao_Celesc.urls')),
    path('clientes/', include('Clientes.urls')),
    path('login/', include('Login.urls')),

]
