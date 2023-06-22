from django.shortcuts import render, redirect
from django.http import HttpResponse
from Geradores.models import Geradores
from Administradores.models import Administradores
from hashlib import sha256
from Dashboard.views import dashboard

def login(request):

    try:
        status = int(request.GET.get("status"))
    except:
        status = 0
        
    return render(request,'login.html', {'status':status})

def valida_login(request):
    
    uc = request.POST.get("uc")
    senha = request.POST.get("senha")
    senha = sha256(senha.encode()).hexdigest()

   
    usuario = Geradores.objects.filter(uc=uc).filter(senha=senha)
    usuarioAdmin = Administradores.objects.filter(senha=senha).filter(uc=uc)
    
   
    if len(usuario) > 0: 
        request.session['usuario'] = usuario[0].id
        request.session['uc'] = usuario[0].uc 
        request.session['nome'] = usuario[0].nome
        request.session['dist'] = usuario[0].distribuidora_id
        request.session['adm'] = usuario[0].admin_id
        request.session['cli'] = usuario[0].cliente_id

        return redirect(dashboard)
    
    if len(usuarioAdmin) > 0:

        request.session['usuarioAdmin'] = usuarioAdmin[0].id
        request.session['uc'] = usuarioAdmin[0].uc
        request.session['nome'] = usuarioAdmin[0].nome

        return redirect(dashboard)
    else: 
        return redirect('/login/?status=1')
    
    
def sair(request):
    request.session.flush()
    return redirect(login)
