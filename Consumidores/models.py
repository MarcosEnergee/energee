from django.db import models
from Distribuidoras.models import Distribuidoras
from Administradores.models import Administradores
from Clientes.models import Clientes
from Geradores.models import Geradores

class Consumidores(models.Model):
    nome = models.CharField(max_length=100)
    uc = models.CharField(max_length=50)
    status = models.IntegerField(default=1)
    gerador = models.ForeignKey(Geradores, on_delete=models.SET_NULL, null=True)
    distribuidora = models.ForeignKey(Distribuidoras, on_delete=models.SET_NULL, null=True)
    admin = models.ForeignKey(Administradores, on_delete=models.SET_NULL, null=True)
    cliente = models.ForeignKey(Clientes, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'consumidores_consumidores'
        
    def __str__(self) -> str:
        return self.nome
