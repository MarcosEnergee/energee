from django.db import models
from Distribuidoras.models import Distribuidoras

class Administradores(models.Model):
    nome = models.CharField(max_length=100)
    end = models.CharField(max_length=250)
    fone = models.CharField(max_length=15)
    distribuidora = models.ForeignKey(Distribuidoras, on_delete=models.SET_NULL, null=True)
    senha = models.CharField(max_length=100)
    uc = models.CharField(max_length=50)

    class Meta:
        db_table = 'administradores_administradores'

    def __str__(self) -> str:
        return self.nome
