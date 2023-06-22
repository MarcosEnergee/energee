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
    
    def __str__(self) -> str:
        return self.nome


""" <label class="block text-sm mt-4">
    <span class="text-gray-700 dark:text-gray-400">Desconto do Cliente %</span>
    <input
      class="block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input"
      type="number" name="descontoCliente"
    />
  </label>

  <label class="block text-sm mt-4">
    <span class="text-gray-700 dark:text-gray-400">Desconto de Gestao %</span>
    <input
      class="block w-full mt-1 text-sm dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:text-gray-300 dark:focus:shadow-outline-gray form-input"
      type="number" name="descontoGestao"
    />
  </label>
 """