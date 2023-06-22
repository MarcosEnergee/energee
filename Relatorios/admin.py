from django.contrib import admin
from .models import Consumidor,Gerador,Azul,ArmazenamentoTotal,ArmazenamentoMensal,Consumidor_Celesc,Azul_Celesc

admin.site.register(Consumidor)
admin.site.register(Gerador)
admin.site.register(Azul)
admin.site.register(ArmazenamentoTotal)
admin.site.register(ArmazenamentoMensal)
admin.site.register(Consumidor_Celesc)
admin.site.register(Azul_Celesc)