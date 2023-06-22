from django.db import models
from Clientes.models import Clientes

class Distribuidoras(models.Model):
    nome = models.CharField(max_length=100)
    status = models.IntegerField(default=1)
    cliente = models.ForeignKey(Clientes, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.nome
