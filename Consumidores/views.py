from django.shortcuts import render, redirect
from .models import Consumidores
from django.core.paginator import Paginator
from Clientes.models import Clientes
from Distribuidoras.models import Distribuidoras

def list(request):
    if request.session.get('usuarioAdmin'):
        nivel=1
        consumidores = Consumidores.objects.all()
        nome = request.session['nome']
        return render(request, 'listconsumidor.html', {'nome':nome,"consumidores": consumidores, "page": None,'nivel':nivel})
    else:
        return redirect('/login/?status=1')
    
def create(request):
    if request.session.get('usuarioAdmin'):
        nivel=1
        clientes = Clientes.objects.all()
        distribuidora = Distribuidoras.objects.all()
        nome = request.session['nome']
        return render(request, 'createconsumidor.html', {'nome':nome,"clientes":clientes,"distribuidora":distribuidora,'nivel':nivel}) 
    else:
        return redirect('/login/?status=1')
    
def salvar(request):
    if request.session.get('usuarioAdmin'):
        nivel=1
        nome = request.POST.get("nome")
        uc = request.POST.get("uc")
        distribuidora = request.POST.get("distribuidora")
        cliente = request.POST.get("cliente")
        Consumidores.objects.create(nome=nome, uc=uc,cliente_id=cliente, distribuidora_id=distribuidora)
        return redirect(list) 
    else:
        return redirect('/login/?status=1')
    
def editar(request,id):
    if request.session.get('usuarioAdmin'):
        nivel=1
        consumidor = Consumidores.objects.get(id=id)
        clientes = Clientes.objects.all()
        distribuidora = Distribuidoras.objects.all()
        nome = request.session['nome']
        return render(request, 'updateConsumidor.html', {'nome':nome,"consumidor":consumidor,"clientes":clientes,"distribuidora":distribuidora,'nivel':nivel}) 
    else:
        return redirect('/login/?status=1')
    
def update(request,id):
    if request.session.get('usuarioAdmin'):
        nome = request.POST.get("nome")
        cliente = request.POST.get("cliente")
        distribuidora = request.POST.get("distribuidora")
        consumidor = Consumidores.objects.get(id=id)
        consumidor.nome = nome
        consumidor.cliente_id = cliente
        consumidor.distribuidora_id = distribuidora 
        consumidor.save()
        return redirect(list)
    else:
        return redirect('/login/?status=1')
    
def deletar(request,id):
    if request.session.get('usuarioAdmin'):
        consumidor = Consumidores.objects.get(id=id)
        consumidor.delete()
        return redirect(list) 
    else:
        return redirect('/login/?status=1')

