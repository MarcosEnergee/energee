from django.db import models
from Distribuidoras.models import Distribuidoras
from Administradores.models import Administradores
from Geradores.models import Geradores
from Consumidores.models import Consumidores
from Clientes.models import Clientes

class Consumidor_Celesc(models.Model):
    uc = models.CharField(max_length=50)
    referencia = models.CharField(max_length=50)
    MptTEQtd = models.CharField(max_length=50)#
    MptTEValor = models.CharField(max_length=50)#
    MptTUSDValor = models.CharField(max_length=50)#
    MptQtd = models.CharField(max_length=50)#
    MptValor = models.CharField(max_length=50)#
    OptTEQtd = models.CharField(max_length=50)#
    OptTEValor = models.CharField(max_length=50)#
    OptTUSDValor = models.CharField(max_length=50)#
    OptQtd = models.CharField(max_length=50)#
    OptValor = models.CharField(max_length=50)#
    PtMptTEQtd = models.CharField(max_length=50)#
    PtMptTUSDQtd = models.CharField(max_length=50,null=True)#
    PtMptTUSDValor = models.CharField(max_length=50)#
    PtMptValor = models.CharField(max_length=50)#
    FpMptTEValor = models.CharField(max_length=50)#
    FpMptTUSDValor = models.CharField(max_length=50)#
    FpMptValor = models.CharField(max_length=50)#
    PtMptTEValor = models.CharField(max_length=50,null=True)#
    status = models.IntegerField(default=1)
    distribuidora = models.ForeignKey(Distribuidoras, on_delete=models.CASCADE, null=True)
    admin = models.ForeignKey(Administradores, on_delete=models.CASCADE, null=True)
    cliente = models.ForeignKey(Clientes, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.uc

class Gerador_Celesc(models.Model):
    uc = models.CharField(max_length=50)
    valor = models.CharField(max_length=50)
    Referencia = models.CharField(max_length=50)
    Saldo_Anterior = models.CharField(max_length=50)
    Cred_Receb = models.CharField(max_length=50)
    Energia_Injetada = models.CharField(max_length=50)
    Energia_InjetadaFP = models.CharField(max_length=50)
    Energia_Ativa = models.CharField(max_length=50)
    Energia_AtivaFP = models.CharField(max_length=50)
    Credito_Utilizado = models.CharField(max_length=50)
    Saldo_Mes = models.CharField(max_length=50)
    Saldo_Transferido = models.CharField(max_length=50)
    Saldo_Final = models.CharField(max_length=50)
    status = models.IntegerField(default=1)
    distribuidora = models.ForeignKey(Distribuidoras, on_delete=models.CASCADE, null=True)
    admin = models.ForeignKey(Administradores, on_delete=models.CASCADE, null=True)
    cliente = models.ForeignKey(Clientes, on_delete=models.SET_NULL, null=True)
    up = models.IntegerField(default=0)
    liberado = models.IntegerField(default=0)
    Imposto = models.CharField(default=0,max_length=20)
    descontoCliente = models.IntegerField(default=0,)
    descontoGestao = models.IntegerField(default=0,)
    
    def __str__(self) -> str:
        return self.uc
#--------------------------------------------------------------#
class Consumidor(models.Model):
    identificacao = models.CharField(max_length=20)
    uc = models.CharField(max_length=50)
    valor = models.CharField(max_length=50)
    referencia = models.CharField(max_length=50)
    qtdmptte = models.CharField(max_length=50)
    precomptte = models.CharField(max_length=50)
    valormptte = models.CharField(max_length=50)
    qtdmpttusd = models.CharField(max_length=50)
    precompttusd = models.CharField(max_length=50)
    valormpttusd = models.CharField(max_length=50)
    qtdconsumo = models.CharField(max_length=50)
    precoconsumo = models.CharField(max_length=50)
    valorconsumo = models.CharField(max_length=50)
    qtduss = models.CharField(max_length=50)
    precouss = models.CharField(max_length=50)
    valoruss = models.CharField(max_length=50)
    qtdilupubli = models.CharField(max_length=50)
    precoilupubli = models.CharField(max_length=50)
    valorilupubli = models.CharField(max_length=50)
    status = models.IntegerField(default=1)
    distribuidora = models.ForeignKey(Distribuidoras, on_delete=models.CASCADE, null=True)
    admin = models.ForeignKey(Administradores, on_delete=models.CASCADE, null=True)
    cliente = models.ForeignKey(Clientes, on_delete=models.SET_NULL, null=True)
    
    def __str__(self) -> str:
        return self.uc

class Gerador(models.Model):
    uc = models.CharField(max_length=50)
    valor = models.CharField(max_length=50)
    Referencia = models.CharField(max_length=50)
    Saldo_Anterior = models.CharField(max_length=50)
    Cred_Receb = models.CharField(max_length=50)
    Energia_Injetada = models.CharField(max_length=50)
    Energia_Ativa = models.CharField(max_length=50)
    Credito_Utilizado = models.CharField(max_length=50)
    Saldo_Mes = models.CharField(max_length=50)
    Saldo_Transferido = models.CharField(max_length=50)
    Saldo_Final = models.CharField(max_length=50)
    status = models.IntegerField(default=1)
    distribuidora = models.ForeignKey(Distribuidoras, on_delete=models.CASCADE, null=True)
    admin = models.ForeignKey(Administradores, on_delete=models.CASCADE, null=True)
    cliente = models.ForeignKey(Clientes, on_delete=models.SET_NULL, null=True)
    up = models.IntegerField(default=0)
    liberado = models.IntegerField(default=0)
    Imposto = models.CharField(default=0,max_length=20)
    descontoCliente = models.IntegerField(default=0,)
    descontoGestao = models.IntegerField(default=0,)
    
    

    def __str__(self) -> str:

        apelido = f"{self.uc}"+f"_{self.Referencia}"
        return apelido

class Azul(models.Model):
    uc = models.CharField(max_length=50)
    Referencia = models.CharField(max_length=50)
    Saldo_Anterior = models.CharField(max_length=50)
    Cred_Receb = models.CharField(max_length=50)
    Energia_Injetada = models.CharField(max_length=50)
    Energia_Ativa = models.CharField(max_length=50)
    Credito_Utilizado = models.CharField(max_length=50)
    Saldo_Mes = models.CharField(max_length=50)
    Saldo_Transferido = models.CharField(max_length=50)
    Saldo_Final = models.CharField(max_length=50)
    status = models.IntegerField(default=1)
    distribuidora = models.ForeignKey(Distribuidoras, on_delete=models.CASCADE, null=True)
    admin = models.ForeignKey(Administradores, on_delete=models.CASCADE, null=True)
    cliente = models.ForeignKey(Clientes, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.uc

class Azul_Celesc(models.Model):
    uc = models.CharField(max_length=50)
    valor = models.CharField(max_length=50)
    Referencia = models.CharField(max_length=50)
    Saldo_Anterior = models.CharField(max_length=50)
    Cred_Receb = models.CharField(max_length=50)
    Energia_Injetada = models.CharField(max_length=50)
    Energia_InjetadaFP = models.CharField(max_length=50)
    Energia_Ativa = models.CharField(max_length=50)
    Energia_AtivaFP = models.CharField(max_length=50)
    Credito_Utilizado = models.CharField(max_length=50)
    Saldo_Mes = models.CharField(max_length=50)
    Saldo_Transferido = models.CharField(max_length=50)
    Saldo_Final = models.CharField(max_length=50)
    status = models.IntegerField(default=1)
    distribuidora = models.ForeignKey(Distribuidoras, on_delete=models.CASCADE, null=True)
    admin = models.ForeignKey(Administradores, on_delete=models.CASCADE, null=True)
    cliente = models.ForeignKey(Clientes, on_delete=models.SET_NULL, null=True)
    up = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return self.uc



class ArmazenamentoTotal(models.Model):
    uc = models.CharField(max_length=50)
    Referencia = models.CharField(max_length=50)
    valor = models.CharField(max_length=50)
    distribuidora = models.ForeignKey(Distribuidoras, on_delete=models.CASCADE, null=True)
    admin = models.ForeignKey(Administradores, on_delete=models.CASCADE, null=True)
    cliente = models.ForeignKey(Clientes, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.uc

class ArmazenamentoMensal(models.Model):
    uc = models.CharField(max_length=50)
    Referencia = models.CharField(max_length=50)
    valor = models.CharField(max_length=50)
    distribuidora = models.ForeignKey(Distribuidoras, on_delete=models.CASCADE, null=True)
    admin = models.ForeignKey(Administradores, on_delete=models.CASCADE, null=True)
    cliente = models.ForeignKey(Clientes, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.uc
    

class historico(models.Model):
    uc = models.CharField(max_length=50)
    Referencia = models.CharField(max_length=50)
    ValorBruto = models.CharField(max_length=50)
    splitConsumo = models.CharField(max_length=50)
    faturaGerador = models.CharField(max_length=50)
    descontoCliente = models.CharField(max_length=50)
    splitCliente = models.CharField(max_length=50)
    descontoGerador = models.CharField(max_length=50)
    splitGerador = models.CharField(max_length=50)
    descontoImpostos = models.CharField(max_length=50)
    splitBruto = models.CharField(max_length=50)
    distribuidora = models.ForeignKey(Distribuidoras, on_delete=models.CASCADE, null=True)
    admin = models.ForeignKey(Administradores, on_delete=models.CASCADE, null=True)
    cliente = models.ForeignKey(Clientes, on_delete=models.SET_NULL, null=True)
    splitFatura = models.CharField(max_length=50)