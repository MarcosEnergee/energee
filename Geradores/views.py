from django.shortcuts import render, redirect
from .models import Geradores,Distribuidoras
from django.core.paginator import Paginator
from Clientes.models import Clientes
from Relatorios.views import relatorios
from hashlib import sha256

def list(request):

    if request.session.get('usuarioAdmin'):
        nivel=1
        geradores = Geradores.objects.all()
        dados_paginator = Paginator(geradores,20)
        page_num = request.GET.get('page')
        page = dados_paginator.get_page(page_num)
        nome = request.session['nome']
        return render(request, 'listgerador.html', {'nome':nome,"geradores":page.object_list,"page":page,'nivel':nivel})
    else:
        return redirect('/login/?status=1')
    
def create(request):
    if request.session.get('usuarioAdmin'):
        nivel=1
        clientes = Clientes.objects.all()
        distribuidora = Distribuidoras.objects.all()
        nome = request.session['nome']
        return render(request, 'creategerador.html',{'nome':nome,"distribuidoras":distribuidora, "clientes":clientes,'nivel':nivel}) 
    else:    
        return redirect('/login/?status=1')
    
def salvar(request):
    if request.session.get('usuarioAdmin'):

        print(request.POST)

        nome = request.POST.get("nome")
        uc = request.POST.get("uc")
        descontoCliente = request.POST.get("descontoCliente")
        descontoGestao = request.POST.get("descontoGestao")
        cliente = request.POST.get("cliente")
        distribuidora = request.POST.get("distribuidora")
        senha = request.POST.get("senha")
        senha = sha256(senha.encode()).hexdigest()
        Geradores.objects.create(nome=nome, uc=uc,descontoCliente=descontoCliente,descontoGestao=descontoGestao,senha=senha,cliente_id=cliente,distribuidora_id=distribuidora)
        return redirect(list) 
    else:    
        return redirect('/login/?status=1')

def editar(request,id):
    if request.session.get('usuarioAdmin'):
        nivel=1
        gerador = Geradores.objects.get(id=id)
        clientes = Clientes.objects.all()
        distribuidora = Distribuidoras.objects.all()
        nome = request.session['nome']
        return render(request, 'updateGerador.html', {'nome':nome,"gerador":gerador,"distribuidoras":distribuidora, "clientes":clientes,'nivel':nivel}) 
    else:    
        return redirect('/login/?status=1')

def update(request,id): 
    if request.session.get('usuarioAdmin'):
        nome = request.POST.get("nome")
        descontoCliente = request.POST.get("descontoCliente")
        descontoGestao = request.POST.get("descontoGestao")
        cliente = request.POST.get("cliente")
        distribuidora = request.POST.get("distribuidora")
        status = request.POST.get("status") 
        gerador = Geradores.objects.get(id=id)
        gerador.nome = nome
        gerador.descontoCliente = descontoCliente
        gerador.descontoGestao = descontoGestao
        gerador.distribuidora_id = distribuidora
        gerador.cliente_id = cliente
        gerador.status = status
        gerador.save()
        return redirect(list)
    else:    
        return redirect('/login/?status=1')
    
def deletar(request,id):
    if request.session.get('usuarioAdmin'):
        gerador = Geradores.objects.get(id=id)
        gerador.delete()
        return redirect(list) 
    else:    
        return redirect('/login/?status=1')

#----GERADORES-------

def Geradoreditar(request,id):
    if request.session.get('usuario'):
        nivel=0
        id = request.session["usuario"]

        gerador = Geradores.objects.get(id=id)
        clientes = Clientes.objects.all()
        distribuidora = Distribuidoras.objects.all()
        nome = request.session['nome']
        return render(request, 'updateGerador_gerador.html', {'nome':nome,"id":id,"gerador":gerador,"distribuidoras":distribuidora, "clientes":clientes,'nivel':nivel}) 
    else:    
        return redirect('/login/?status=1')

def Geradorupdate(request,id): 
    if request.session.get('usuario'):
        nome = request.POST.get("nome")
        senha = request.POST.get("senha")
        senha = sha256(senha.encode()).hexdigest()
        gerador = Geradores.objects.get(id=id)
        gerador.nome = nome
        gerador.senha = senha
        gerador.save()
        return redirect(relatorios)
    else:    
        return redirect('/login/?status=1')