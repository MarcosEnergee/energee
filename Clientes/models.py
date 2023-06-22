from django.db import models

class Clientes(models.Model):
    nome = models.CharField(max_length=100)
    end = models.CharField(max_length=250)
    fone = models.CharField(max_length=15)
    status = models.IntegerField(default=1)
    
    class Meta:
        db_table = 'Clientes_clientes'

    def __str__(self) -> str:
        return self.nome
