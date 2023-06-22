from django.shortcuts import render, redirect
from . import models
from .models import Document
from .copel import Copel
from .azul import Relatorio
from Clientes.models import Clientes
from Distribuidoras.models import Distribuidoras
from Administradores.models import Administradores
from Geradores.models import Geradores
import os
import pdfplumber


Relatorio = Relatorio()
Copel = Copel()


def list(request):
    if request.session.get('usuarioAdmin'):
        nivel=1
        nome = request.session['nome']
        return render(request, 'extracao.html',{'nome':nome,'nivel':nivel}) 
    else:
        return redirect('/login/?status=1')

def areaConsumidor(request):
    if request.session.get('usuarioAdmin'):
        nivel=1
        clientes = Clientes.objects.all()
        distribuidoras = Distribuidoras.objects.all()
        nome = request.session['nome']
        return render(request, 'consumidor.html', {'nome':nome,"clientes":clientes,"distribuidoras":distribuidoras,'nivel':nivel}) 
    else:
        return redirect('/login/?status=1')
    
def areaGerador(request):
    if request.session.get('usuarioAdmin'):
        nivel=1
        clientes = Clientes.objects.all()
        distribuidoras = Distribuidoras.objects.all()
        nome = request.session['nome']
        return render(request, 'gerador.html', {'nome':nome,"clientes":clientes,"distribuidoras":distribuidoras,'nivel':nivel}) 
    else:
        return redirect('/login/?status=1')
    
def areaAzul(request):
    if request.session.get('usuarioAdmin'):
        nivel=1
        clientes = Clientes.objects.all()
        distribuidoras = Distribuidoras.objects.all()
        nome = request.session['nome']
        return render(request, 'azul.html', {'nome':nome,"clientes":clientes,"distribuidoras":distribuidoras,'nivel':nivel}) 
    else:
        return redirect('/login/?status=1')
    
def deletar(request):
    if request.session.get('usuarioAdmin'):
        consumidor = Document.objects.all()
        consumidor.delete()
    else:
        return redirect('/login/?status=1')
    
def uploadFile(request):
    if request.session.get('usuarioAdmin'):

        if request.session.get('usuarioAdmin'):
                adm = request.session['usuarioAdmin']
                nomeUser = Administradores.objects.get(id=adm)

        elif request.session.get('usuario'):
            gerador = request.session['usuario']
            nomeUser = Geradores.objects.get(id=gerador)

        nivel=1
        cli = request.POST.get("cliente")
        tipo = request.POST.get('tipo')
        dist = request.POST.get('dist')

        dir = "media/Upload Files"

        try:
            for f in os.listdir(dir):
                os.remove(os.path.join(dir,f))
        except:
            pass

        if request.method == "POST":
            
            uploadedFile = request.FILES["uploadedFile"]

            document = models.Document( uploadedFile = uploadedFile )

            document.save()

        documents = models.Document.objects.all()

        url=[]
        for i in documents:
            url.append(i.uploadedFile.url)
        
        nome = url[0] 
        nome = nome.split('/')
        nome = nome[-1]
        
        if tipo == 'consumidor':
            return render(request, "consumidor.html", {'nome':nomeUser,"files": documents,"nomedoc": nome, "cli": cli, "dist": dist,'nivel':nivel})
        if tipo == 'gerador':
            return render(request, "gerador.html", {'nome':nomeUser,"files": documents,"nomedoc": nome, "cli": cli, "dist": dist,'nivel':nivel})
        if tipo == 'azul':
            return render(request, "azul.html", {'nome':nomeUser,"files": documents,"nomedoc": nome, "cli": cli, "dist": dist,'nivel':nivel})
    else:
        return redirect('/login/?status=1')
    
#----------------------- COPEL ---------------------------------#
def ConsumidorCopel(request, cli):
    if request.session.get('usuarioAdmin'):
        nivel=1
        def extracao(caminho,pdf_base, pagina):

            dic = {}
            texto = Copel.Tratatexto(caminho,pdf_base, pagina)
            ident = Copel.extraiIdentificacao(caminho, pdf_base)

            try:
                identific = ident.index('IDENTIFICAÇÃO')
            except:
                pass
            
            try:
                dic['identificacao'] = ident[identific+1]
            except:
                dic['identificacao'] = 0

            try:
                uc = Copel.extraiUC(caminho,pdf_base, pagina)
                dic['uc'] = uc  
            except:
                dic['uc'] =0
            
            try:
                valor = texto[0].index ('VALORAPAGAR')
            except:
                pass

            try:
                ref = texto[0].index ('REFERENCIA')
            except:
                pass

            try:
                referencia = texto[0][ref-2]
                referencia = referencia.replace('/', '')
                dic['referencia'] = referencia
                
            except:
                dic['referencia'] = 0

            try:
                valor = texto[0][valor+1]
                valor = str(valor).replace('.','')
                valor = Copel.virgulaemponto(valor)
                valor = float(valor)
                dic['valor'] = valor
            except:
                dic['valor'] =0    
            
            qtdconsumo = []
            precoconsumo = []
            valorconsumo = []
            qtdmpttusd = []
            precompttusd = []
            valormpttusd = []
            qtdmptte = []
            precomptte = []
            valormptte = []
            qtduss = []
            precouss = []
            valoruss = []
            qtdilupubli = []
            precoilupubli = []
            valorilupubli = []

            for valor in texto[1]:
                for i in valor[1]:
                    
                    nome = texto[0][i]

                    if nome == 'CONTILUMINPUBLICAMICIPIO':
                        
                        try:
                            qtdilupubli.append(texto[0][i+1])
                        except:
                            pass
                        
                        try:
                            retorno = Copel.virgulaemponto(texto[0][i+2])
                            precoilupubli.append(retorno)
                        except:
                            pass
                        
                        try:
                            retorno = Copel.virgulaemponto(texto[0][i+3])
                            valorilupubli.append(retorno)
                        except:
                            pass

                    if nome == 'ENERGIAELETCONSUMO':
                        qtdconsumo.append(texto[0][i+1])

                        retorno = Copel.virgulaemponto(texto[0][i+2])
                        precoconsumo.append(retorno)

                        retorno = Copel.virgulaemponto(texto[0][i+3])
                        valorconsumo.append(retorno)

                    if nome == 'ENERGIAELETUSOSISTEMA':
                        qtduss.append(texto[0][i+1])

                        retorno = Copel.virgulaemponto(texto[0][i+2])
                        precouss.append(retorno)

                        retorno = Copel.virgulaemponto(texto[0][i+3])
                        valoruss.append(retorno)
                
                    if nome == 'ENERGIAINJOUCMPTTE':

                        qtdmptte.append(texto[0][i+2])

                        retorno = Copel.virgulaemponto(texto[0][i+3])
                        precomptte.append(retorno)

                        retorno = Copel.virgulaemponto(texto[0][i+4])
                        valormptte.append(retorno)
                    
                    if nome == 'ENERGIAINJOUCMPTTUSD':
                        qtdmpttusd.append(texto[0][i+2])

                        retorno = Copel.virgulaemponto(texto[0][i+3])
                        precompttusd.append(retorno)

                        retorno = Copel.virgulaemponto(texto[0][i+4])
                        valormpttusd.append(retorno)
            try:
                qtdmptte = Copel.Trataqtd(qtdmptte)

                qtdmptte = Copel.Trasformaemvalor(qtdmptte)
                
                dic['qtdmptte'] = sum(qtdmptte)
            except:
                dic['qtdmptte'] = 0

            try:
                precomptte = Copel.Trasformaemvalor(precomptte)

                tamanho  = len(precomptte)
                dic['precomptte'] = round(sum(precomptte)/tamanho,6)
            except:
                dic['precomptte'] = 0

            try:
                valormptte = Copel.Trasformaemvalor(valormptte)

                dic['valormptte'] = round(sum(valormptte),2)
            except:
                dic['valormptte'] = 0

            try:
                qtdmpttusd = Copel.Trataqtd(qtdmpttusd)
                qtdmpttusd = Copel.Trasformaemvalor(qtdmpttusd)

                dic['qtdmpttusd'] = sum(qtdmpttusd)
            except:
                dic['qtdmpttusd'] = 0

            try:
                precompttusd = Copel.Trasformaemvalor(precompttusd)

                tamanho = len(precompttusd)
                dic['precompttusd'] = round(sum(precompttusd)/tamanho,6)
            except:
                dic['precompttusd'] = 0

            try:
                valormpttusd = Copel.Trasformaemvalor(valormpttusd)

                dic['valormpttusd'] = round(sum(valormpttusd),2)
            except:
                dic['valormpttusd'] = 0

            try:
                qtdconsumo = Copel.Trataqtd(qtdconsumo)        
                qtdconsumo = Copel.Trasformaemvalor(qtdconsumo)

                dic['qtdconsumo'] = sum(qtdconsumo)
            except:
                dic['qtdconsumo'] = 0

            try:
                precoconsumo = Copel.Trasformaemvalor(precoconsumo)
                
                tamanho = len(precoconsumo)
                dic['precoconsumo'] = round(sum(precoconsumo)/tamanho,6)
            except:
                dic['precoconsumo'] = 0

            try:
                valorconsumo = Copel.Trasformaemvalor(valorconsumo)

                dic['valorconsumo'] = round(sum(valorconsumo),2)
            except:
                dic['valorconsumo'] = 0

            try:
                qtduss = Copel.Trataqtd(qtduss)
                qtduss = Copel.Trasformaemvalor(qtduss)

                dic['qtduss'] = sum(qtduss)
            except:
                dic['qtduss'] = 0

            try:
                precouss = Copel.Trasformaemvalor(precouss)

                tamanho = len(precouss)
                dic['precouss'] = round(sum(precouss)/tamanho,6)
            except:
                dic['precouss'] = 0

            try:
                valoruss = Copel.Trasformaemvalor(valoruss)

                dic['valoruss'] = round(sum(valoruss),2)
            except:
                dic['valoruss'] = 0

            try:
                qtdilupubli = Copel.Trataqtd(qtdilupubli)
                qtdilupubli = Copel.Trasformaemvalor(qtdilupubli)

                dic['qtdilupubli'] = sum(qtdilupubli)
            except:
                dic['qtdilupubli'] = 0

            try:
                precoilupubli = Copel.Trasformaemvalor(precoilupubli)

                tamanho = len(precoilupubli)
                dic['precoilupubli'] = round(sum(precoilupubli)/tamanho,6)
            except:
                dic['precoilupubli'] = 0

            try:
                valorilupubli = Copel.Trasformaemvalor(valorilupubli)

                dic['valorilupubli'] = round(sum(valorilupubli),2)
            except:
                dic['valorilupubli'] = 0
            

            if dic['uc'] != 0:

                return dic

        caminho = f"media/Upload Files/"
        pdf_base = os.listdir("media/Upload Files/")
        pdf_base = pdf_base[0]

        pdf = pdfplumber.open(f'{caminho}/{pdf_base}')
        
        totalpages = len(pdf.pages)

        x=0
        repo = []
        while x < totalpages:
            dic = extracao(caminho,pdf_base, x)
            if dic != None:
                repo.append(dic)     
            x+=1
            
        dic = Copel.TrataRetornoDic(repo)

        for valor in dic:
            Copel.inserirConsumidor(valor['identificacao'],valor['uc'],round(valor['valor'],2),valor['referencia'],valor['qtdmptte'],round(valor['precomptte'],6),round(valor['valormptte'],2),valor['qtdmpttusd'],round(valor['precompttusd'],6),round(valor['valormpttusd'],2),valor['qtdconsumo'],round(valor['precoconsumo'],6), round(valor['valorconsumo'],2),valor['qtduss'],round(valor['precouss'],6), round(valor['valoruss'],2),valor['qtdilupubli'],round(valor['precoilupubli'],6),round(valor['valorilupubli'],2),1,1,1,cli)
            print(valor['identificacao'],valor['uc'],round(valor['valor'],2),valor['referencia'],valor['qtdmptte'],round(valor['precomptte'],6),round(valor['valormptte'],2),valor['qtdmpttusd'],round(valor['precompttusd'],6),round(valor['valormpttusd'],2),valor['qtdconsumo'],round(valor['precoconsumo'],6), round(valor['valorconsumo'],2),valor['qtduss'],round(valor['precouss'],6), round(valor['valoruss'],2),valor['qtdilupubli'],round(valor['precoilupubli'],6),round(valor['valorilupubli'],2),1,1,1,cli)
        
        dir = "media/Upload Files"

        nome = request.session['nome']
        return render(request, 'extracao.html',{'nome':nome,'nivel':nivel}) 
    else:
        return redirect('/login/?status=1')
    
def Gerador(request,cli):
    if request.session.get('usuarioAdmin'):
        nivel=1
        caminho = f"media/Upload Files/"
        arquivos = os.listdir("media/Upload Files/")

        for arquivo in arquivos:

            resultado = Copel.infoGerador(caminho,arquivo)

            uc = resultado[0]
            valor = resultado[1]
            Referencia = resultado[2]
            Referencia = Referencia.replace("/","")
            Referencia = Referencia.replace("-","")

            result = Copel.VerificaGerador(uc, Referencia,cli)

            if len(result) > 0:
                
                id = result[0][0]
                
                print('atualizando')
                Copel.AtualizarContaGerador(id, valor)

            else:
                print('Inserindo Gerador')
                Copel.inserirContaGerador(uc,valor,Referencia,0,0,0,0,0,0,0,0,1,1,1,cli)



        nome = request.session['nome']
        return render(request, 'gerador.html',{'nome':nome,'nivel':nivel}) 
    
    else:
        return redirect('/login/?status=1')
    
def RelatorioAzulCopel(request,cli):
    if request.session.get('usuarioAdmin'):
        nivel=1
        def extracaoRelatorio(pagina, repo):

            pdf = pdfplumber.open(f'{caminho}/{arquivo}')
            p = pdf.pages[pagina]
            tabela = p.extract_table()
            texto = p.extract_text() 

            pdf.close()

            dic = Relatorio.ExtrairValor(texto,tabela)

            retorno = Relatorio.Verificarepetidos(dic['uc'], dic['referencia'], repo)
            
            if retorno==True:
                print('ja existe')
            
            else:
                return dic
            
        caminho = r"media/Upload Files"
        arquivos = os.listdir(r"media/Upload Files")

        repo = []
        repoGerador = []
        for arquivo in arquivos:
            pdf = pdfplumber.open(f'{caminho}/{arquivo}')
            totalpages = len(pdf.pages)


            x=0
            while x < totalpages:

                pdf = pdfplumber.open(f'{caminho}/{arquivo}')
                p = pdf.pages[0]

                texto = p.extract_text()  

                uc = texto.split("UC :") 
                del uc[0]
                uc = uc[0]
                uc = uc.split("Tipo da Fase")
                uc = uc[0]
                uc = uc.replace(" ","")

                if x == 0:
                    dic = extracaoRelatorio(x,repoGerador)
                    if dic != None:
                        repoGerador.append(dic)
                else:
                    dic = extracaoRelatorio(x, repo)
                    
                    if dic != None:
                        repo.append(dic)
                    
                x+=1
            
                pdf.close()
                
        for i in repoGerador:  

            retorno = Copel.VerificaGerador(i['uc'],i['referencia'],cli)

            if len(retorno) > 0:

                Relatorio.AtualizarContaAzul(i['uc'],i['referencia'],i['Saldo_Anterior'],i['Cred_Receb'],i['Energia_Injetada'],i['Energia_Ativa'],i['Credito_Utilizado'],i['Saldo_Mes'],i['Saldo_Transferido'],i['Saldo_Final'], cli)
            else:
                Relatorio.inserirAzulcopelGerador(i['uc'],i['referencia'],i['Saldo_Anterior'],i['Cred_Receb'],i['Energia_Injetada'],i['Energia_Ativa'],i['Credito_Utilizado'],i['Saldo_Mes'],i['Saldo_Transferido'],i['Saldo_Final'],0,1,1,1,cli)


        for i in repo:

            retorno = Copel.Verificarelatorio(i['uc'],i['referencia'],cli)
    
            if len(retorno) > 0:

                print('Fatura Existente')
            else: 
                Relatorio.inserirAzulcopel(i['uc'],i['referencia'],i['Saldo_Anterior'],i['Cred_Receb'],i['Energia_Injetada'],i['Energia_Ativa'],i['Credito_Utilizado'],i['Saldo_Mes'],i['Saldo_Transferido'],i['Saldo_Final'],1,1,1,cli)
        
        nome = request.session['nome']
        return render(request, 'relatorio.html',{'nome':nome,'nivel':nivel})
    
    else:
        return redirect('/login/?status=1') 

 