from django.db import models
from Distribuidoras.models import Distribuidoras

class Administradores(models.Model):
    nome = models.CharField(max_length=100)
    fone = models.CharField(max_length=15)
    end = models.CharField(max_length=200)
    distribuidora = models.ForeignKey(Distribuidoras, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.nome
