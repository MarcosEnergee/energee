from django.db import models
from Distribuidoras.models import Distribuidoras
from Administradores.models import Administradores
from Clientes.models import Clientes

class Geradores(models.Model):
    nome = models.CharField(max_length=100)
    uc = models.CharField(max_length=50)
    status = models.IntegerField(default=1)
    distribuidora = models.ForeignKey(Distribuidoras, on_delete=models.SET_NULL, null=True)
    admin = models.ForeignKey(Administradores, on_delete=models.SET_NULL, null=True)
    cliente = models.ForeignKey(Clientes, on_delete=models.SET_NULL, null=True)
    senha = models.CharField(max_length=100)

    class Meta:
        db_table = 'geradores_geradores'
    
    def __str__(self) -> str:
        return self.nome


