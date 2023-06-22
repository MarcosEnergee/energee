from django.shortcuts import render, redirect
from . import models
from .celesc import Celesc
from .azul import Relatorio
from Clientes.models import Clientes
from Extracao.models import Document
from Distribuidoras.models import Distribuidoras
import os
import pdfplumber

Relatorio = Relatorio()
Celesc = Celesc()
#----------------------- CELESC --------------------------------#

def CelescConsumidor(request,cli):
    if request.session.get('usuarioAdmin'):
        nivel=1
        caminho = f"media/Upload Files/"
        arquivos = os.listdir("media/Upload Files/")
        arquivo = arquivos[0]


        pdf = pdfplumber.open(f'{caminho}/{arquivo}')
        totalpages = len(pdf.pages)

        def processamento(texto, dic):

            di = {}

            retorno = Celesc.PegaPosicao(texto)
            retorno = Celesc.CorrigeDic(retorno)
            retorno = Celesc.Tratalista(retorno)
            retorno = Celesc.distribuiDic(retorno)

            
            ucFatura = Celesc.PegaUC(texto)
            di.update(dic)
            di.update(ucFatura)
            di.update(retorno) 

            Celesc.Insere_Consumidor_Celesc(di['uc'],di['referencia'],di['MptTEQtd'],di['MptTEValor'],di['MptTUSDValor'],di['MptQtd'],di['MptValor'],di['OptTEQtd'],di['OptTEValor'],di['OptTUSDValor'],di['OptQtd'],di['OptValor'],di['PtMptTEQtd'],di['PtMptTEValor'],di['PtMptTUSDValor'],di['PtMptValor'],di['FpMptTEValor'],di['FpMptTUSDValor'],di['FpMptValor'],di['PtMptTUSDQtd'],1,1,cli,2)    

            consumidores = Celesc.VerificaAdmin()

            for i in consumidores:
                Celesc.AtualizarSituacao(i[0], i[1], di['referencia'],cli)



        def extracaoRelatorio_celesc(pagina):

            dic = {}

            pdf = pdfplumber.open(f'{caminho}/{arquivo}')
            p = pdf.pages[pagina]
            texto = p.extract_words()

            textos = []

            for i in range(len(texto)):
                if texto[i]['text'] == 'Nome:':
                    textos.append(i)
                
                if texto[i]['text'] =='Referência:':
                    referencia = texto[i+1]['text']
                    referencia = referencia.replace('-','')
                    dic['referencia'] = referencia

                if texto[i]['text'] =='Documento:':
                    dic['numDoc'] = texto[i+1]['text']+texto[i+2]['text']+texto[i+3]['text']
                
            
            
            try:
                texto1 = texto[textos[0]:textos[1]]
                processamento(texto1, dic)

                texto2 = texto[textos[1]:]
                processamento(texto2, dic)

            except:
                texto1 = texto[textos[0]:]
                processamento(texto1, dic)


        x=1
        while x < totalpages:
            extracaoRelatorio_celesc(x)
            x+=1 
        return render(request, 'extracao.html',{'nivel':nivel})
    
    else:
        return redirect('/login/?status=1')

def CelescGerador(request,cli):
    if request.session.get('usuarioAdmin'): 
        nivel=1
        dic = {}

        caminho = f"media/Upload Files/"
        arquivos = os.listdir("media/Upload Files/")
        arquivo = arquivos[0]

        for arquivo in arquivos:
                
            pdf = pdfplumber.open(f'{caminho}/{arquivo}')
            p = pdf.pages[0]
            texto = p.extract_text()

            resultado = Celesc.infoGerador(texto)

            try:
                ref = resultado.index('REFERENCIA')
            except:
                ref = resultado.index('REFERÊNCIA:')

            try:
                dic['referencia'] = (resultado[ref+1].replace('/',''))
            except:
                dic ['referencia'] = '-'

            try:
                uc = resultado.index('UNIDADECONSS')
            except:
                pass

            try:
                dic['uc'] = resultado[uc-1]
            except:
                dic ['uc'] = '-'

            try:
                valor = resultado.index('VALORCONTA')
            except:
                pass

            try:
                dic['valor'] = resultado[valor+1]
            except:
                dic ['valor'] = '-'


            uc = dic['uc']
            Referencia = dic['referencia']
            valor = dic['valor']
            valor = Celesc.Trasformaemvalor(valor)

            result = Celesc.VerificaGerador(uc, Referencia)
            
            if len(result) > 0:

                Celesc.AtualizarContaGerador(uc, valor, Referencia)
            
            else:
                Celesc.inserirContaGerador(uc,valor,Referencia,0,0,0,0,0,0,0,0,0,0,1,0,1,cli,2)

        return render(request, 'extracao.html',{'nivel':nivel})
    else:
        return redirect('/login/?status=1')
    
def RelatorioAzulCelesc(request,cli):

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
                uc = uc[-1]
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

        #------ Gerador ------#        
        for i in repoGerador:  

            retorno = Celesc.VerificaGerador(i['uc'],i['referencia'],cli)

            if len(retorno) > 0:

                Relatorio.AtualizarContaAzul(i['uc'],i['referencia'],i['Saldo_Anterior'],i['Cred_Receb'],i['Energia_Injetada'],i['Energia_InjetadaFP'],i['Energia_Ativa'],i['Energia_AtivaFP'],i['Credito_Utilizado'],i['Saldo_Mes'],i['Saldo_Transferido'],i['Saldo_Final'], cli)
            else:
                Relatorio.inserirAzulCelescGerador(i['uc'],i['referencia'],i['Saldo_Anterior'],i['Cred_Receb'],i['Energia_Injetada'],i['Energia_InjetadaFP'],i['Energia_Ativa'],i['Energia_AtivaFP'],i['Credito_Utilizado'],i['Saldo_Mes'],i['Saldo_Transferido'],i['Saldo_Final'],1,0,1,1,1,cli)

        #------Consumidor------#
        for i in repo:
            retorno = Relatorio.Verificarelatorio_celesc(i['uc'],i['referencia'],cli)
    
            if len(retorno) > 0:

                print('Fatura Existente')
            else: 
                Relatorio.inserirAzulCelesc(i['uc'],i['referencia'],i['Saldo_Anterior'],i['Cred_Receb'],i['Energia_Injetada'],i['Energia_InjetadaFP'],i['Energia_Ativa'],i['Energia_AtivaFP'],i['Credito_Utilizado'],i['Saldo_Mes'],i['Saldo_Transferido'],i['Saldo_Final'],1,0,1,1,1,cli)
                
        return render(request, 'extracao.html',{'nivel':nivel}) 

    else:
        return redirect('/login/?status=1')
 