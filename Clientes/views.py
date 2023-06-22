from django.shortcuts import render,redirect
from .models import Clientes
from Distribuidoras.models import Distribuidoras
from django.core.paginator import Paginator

def list(request):

    if request.session.get('usuarioAdmin'):
        nivel = 1
        clientes = Clientes.objects.all()
        dados_paginator = Paginator(clientes,20)
        page_num = request.GET.get('page')
        page = dados_paginator.get_page(page_num)
        nome = request.session['nome']
        return render(request, 'clientes.html', {'nome':nome,"clientes": page.object_list, "page": page,'nivel':nivel})
    else:
        return redirect('/login/?status=1')
    
def create(request):
    if request.session.get('usuarioAdmin'):
        nivel=1
        distribuidoras = Distribuidoras.objects.all()
        nome = request.session['nome']
        return render(request, 'createcliente.html', {'nome':nome,"distribuidoras":distribuidoras,'nivel':nivel}) 
    else:
        return redirect('/login/?status=1')
    
def salvar(request):
    if request.session.get('usuarioAdmin'):
        nome = request.POST.get("nome")
        end = request.POST.get("end")
        fone = request.POST.get("fone")

        Clientes.objects.create(nome=nome, end=end, fone=fone)
        return redirect(list) 
    else:
        return redirect('/login/?status=1')

def editar(request,id):
    if request.session.get('usuarioAdmin'):
        nivel=1
        distribuidora = Distribuidoras.objects.all()
        cliente = Clientes.objects.get(id=id)
        nome = request.session['nome']
        return render(request, 'updateCli.html', {'nome':nome,"cliente":cliente,"distribuidoras":distribuidora,'nivel':nivel}) 
    else:
        return redirect('/login/?status=1')
    
def update(request,id):
    if request.session.get('usuarioAdmin'):
        nome = request.POST.get("nome")
        end = request.POST.get("end")
        distribuidora = request.POST.get("distribuidora")
        status = request.POST.get("status")
        cliente = Clientes.objects.get(id=id)
        cliente.end = end
        cliente.distribuidora_id = distribuidora
        cliente.status = status
        cliente.nome = nome
        cliente.save()
        return redirect(list)
    else:
        return redirect('/login/?status=1')

def deletar(request,id):
    if request.session.get('usuarioAdmin'):
        cliente = Clientes.objects.get(id=id)
        cliente.delete()
        return redirect(list) 
    else:
        return redirect('/login/?status=1')