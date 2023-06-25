from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from .models import Gerador,Gerador_Celesc
from Geradores.models import Geradores
from Clientes.models import Clientes
from Distribuidoras.models import Distribuidoras
from django.core.paginator import Paginator
from Administradores.models import Administradores
from datetime import datetime
import numpy as np
from .relatorio import Relatorio

Relatorio = Relatorio()
cli=1

#----------------------------------------------------------#
def AlimentaSelectDist(request,cli):
    if request.session.get('usuario') or request.session.get('usuarioAdmin'):
        distribuidoras = Relatorio.SelectDist(cli)
        if len(distribuidoras)>0:
            dist = []
            for i in distribuidoras:
                dist.append(f'<option value="89" >Selecione a Distribuidora</option><option value="{i[0]}" >{i[1]}</option>')

                data_json = {'distribuidoras':dist}
        else:
            data_json = {'distribuidoras':'<option >Nada Cadastrado</option>'}

        return JsonResponse(data_json)
    else:
        return redirect('/login/?status=1')

def AlimentaSelect(request,cli):
    if request.session.get('usuario') or request.session.get('usuarioAdmin'):
        cli = cli.split('&')
        dist = cli[0]
        cli = cli[1]

        ref = Relatorio.Referencias(cli)
        r = Relatorio.ucsSelect(cli,dist)
        
        if len(r)>0:
            referencias = []
            for i in ref:
                referencias.append(f'<option >{i}</option>')

            ucs = [] 
            for i in r:
                ucs.append(f'<option value="{i[2]}">{i[1]}</option>')

            data_json = {'ucs':ucs, 'refs':referencias[::-1]}
        
        else:
            data_json = {'ucs':'<option >Nada Cadastrado</option>', 'refs':'<option >Nada Cadastrado</option>'}
        return JsonResponse(data_json)
    else:
        return redirect('/login/?status=1')

def grafico_relatorio(request,uc):
    if request.session.get('usuario') or request.session.get('usuarioAdmin'):

        try:

            if request.session.get('usuarioAdmin'):
                consumo = Relatorio.consumoGrafico(uc)
                geracao = Relatorio.GeracaoGrafico(uc)
            
            if request.session.get('usuario') and request.session['dist'] == 1:
                consumo = Relatorio.consumoGrafico(uc)
                geracao = Relatorio.GeracaoGrafico(uc)

            if request.session.get('usuario') and request.session['dist'] == 2:
                consumo = Relatorio.consumoGrafico_celesc(uc)
                geracao = Relatorio.GeracaoGrafico_celesc(uc)



            meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
            consum = []
            gerac = []
            labels = []
            cont = 0
            mes = datetime.now().month + 1
            ano = datetime.now().year

            for i in range(13):
                mes -= 1
                if mes == 0:
                    mes = 12
                    ano -= 1

                refsitem = str(mes)+str(ano)
                for c,g in zip(consumo,geracao):
                    mesref = int(c[1][0:2])
                    anoref = c[1]

                    refbanco = str(mesref)+str(anoref)[2:6]
                    if refbanco == refsitem:

                        labels.append(meses[mes-1])
                        consum.append(c[2])
                        gerac.append(g[2])

            data_json = {'consumo': consum[::-1],'geracao': gerac[::-1], 'labels': labels[::-1]}
        
            return JsonResponse(data_json)

        except:
            data_json = {}
        
            return JsonResponse(data_json)
    
    else:
        return redirect('/login/?status=1')

def grafico_relatorio_celesc(request,uc):
    if request.session.get('usuarioAdmin'):

        try:
            consumo = Relatorio.consumoGrafico_celesc(uc)
            geracao = Relatorio.GeracaoGrafico_celesc(uc)

            meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
            consum = []
            gerac = []
            labels = []
            cont = 0
            mes = datetime.now().month + 1
            ano = datetime.now().year

            for i in range(13):
                mes -= 1
                if mes == 0:
                    mes = 12
                    ano -= 1

                refsitem = str(mes)+str(ano)
                for c,g in zip(consumo,geracao):
                    mesref = int(c[1][0:2])
                    anoref = c[1]

                    refbanco = str(mesref)+str(anoref)[2:6]
                    if refbanco == refsitem:

                        labels.append(meses[mes-1])
                        consum.append(c[2])
                        gerac.append(g[2])

            data_json = {'consumo': consum[::-1],'geracao': gerac[::-1], 'labels': labels[::-1]}
        
            return JsonResponse(data_json)

        except:
            data_json = {}
        
            return JsonResponse(data_json)
    
    else:
        return redirect('/login/?status=1')
    
def update_armazenados(request,dist):

    if request.session.get('usuario') or request.session.get('usuarioAdmin'):
        if dist == 1:

            Relatorio.ApagarArmM(dist)
            Relatorio.ApagarArmT(dist)

            Relatorio.Armazenamento_Copel(cli,dist)

            Relatorio.AtualizarUp()
        
        elif dist == 2:
            
            Relatorio.ApagarArmM(dist)
            Relatorio.ApagarArmT(dist)

            Relatorio.Armazenamento_Celesc(cli,dist)
            
            Relatorio.AtualizarUp_Celesc()

        return redirect(relatorios)
    
    else:
        return redirect('/login/?status=1')

def valoresConsumidor(request,uc):

    uc_Session = request.session["uc"]
    dist = int(request.GET.get("dist"))

    if uc_Session == str(uc):
        pass
    else:
        return redirect('/login/?status=2')

    if request.session.get('usuario'):
        nivel = 0

        id = request.session["usuario"]
        mensal = Relatorio.RelatorioGerador_mensal(uc,dist)
        total = Relatorio.RelatorioGerador_total(uc,dist)
        
        if dist ==1:
            valores = Relatorio.RelatorioGerador(uc)
            
            rep = []
            for v,m,t in zip(valores[::-1],mensal[::-1],total[::-1]):
                rep.append([v[0],int(v[1]),int(v[2]),int(v[3]),int(v[4]),int(m),int(t)])
        
        elif dist ==2:
            valores = Relatorio.RelatorioGerador_Celesc(uc)

            rep = []
            for v,m,t in zip(valores[::-1],mensal[::-1],total[::-1]):
                rep.append([v[0],v[1],v[2],v[3],v[4],v[5],v[6],m,t])

        c = tuple(rep)
        dados_paginator = Paginator(c,12)
        page_num = request.GET.get('page')
        page = dados_paginator.get_page(page_num)

        return render(request, 'valoresGerador.html', {'valores':page.object_list,'id':id, 'page':page,'dist':dist,'nivel':nivel,})
    else:
        return redirect('/login/?status=1')
    
def relatorios(request):
    if request.session.get('usuario') or request.session.get('usuarioAdmin'):

        if request.session.get('usuario'):
            id = request.session["usuario"]
        if request.session.get('usuarioAdmin'):
            id=None

        referencia = request.GET.get("referencia")

        clientes = Clientes.objects.all()
        up_copel = Relatorio.VerificaUpdate()
        up_celesc = Relatorio.VerificaUpdate_Celesc()
        
        update = {}
        if len(up_copel) > 0 or len(up_celesc) > 0:

            if len(up_copel) > 0:
                update['valor'] = up_copel[0][-5] 
                update['distribuidora'] = up_copel[0][-7]
            
            if len(up_celesc) > 0:
                update['valor'] = up_celesc[0][-8] 
                update['distribuidora'] = up_celesc[0][-5]

        else:
            update['valor'] = 0
        

        if request.session.get('usuarioAdmin'):

            adm = request.session['usuarioAdmin']
            cli = 1
            uc = request.GET.get("uc")
            cliente = request.GET.get("cliente")
            dist = request.GET.get("dist")
            nivel = 1
            nomeUser = Administradores.objects.get(id=adm)
            ref = Relatorio.Referencias(cli)


        elif request.session.get('usuario'):
            uc = request.session['uc']
            dist = request.session['dist']
            cliente = request.session['cli']
            cli = request.session['cli']
            gerador = request.session['usuario']
            nivel = 0
            nomeUser = Geradores.objects.get(id=gerador)

            if dist == 1:
                ref = Relatorio.ReferenciasGerador(cli)
            if dist == 2:
                ref = Relatorio.ReferenciasGerador_celesc(cli)
            
        
        und= Relatorio.ucs(cli) 

        nomeDist = Distribuidoras.objects.filter(id=dist)
        

        dic = {}
        if (uc and uc != 'Selecione a UC' and uc != 'Nada Cadastrado') and (referencia and referencia != 'Selecione a Referencia') and (cliente and cliente != 'Selecione o Cliente'):

            dist = int(dist)

            historico = ['072018','082018','092018','102018','112018','122018','012019','022019','032019','042019','052019','062019','072019','082019','092019','102019','112019','122019','012020','022020','032020','042020','052020','062020','072020','082020','092020','102020','112020','122020','012021','022021','032021','042021','052021','062021','072021','082021','092021','102021','112021','122021','012022','022022','032022','042022','052022','062022','072022','082022','092022','102022','112022','122022','012023','022023','032023','042023','052023']

            if dist == 2:

                if referencia in historico:
                    dadosgerador = Relatorio.valorGerador_Celesc(referencia,cli, uc)
                    dic.update(dadosgerador) 

                    valoresHistorico = Relatorio.SelecionaHistorico(referencia,uc)
                    dic.update(valoresHistorico) 

                    men = Relatorio.ArmMensal(referencia,uc,cliente,dist)
                    total = Relatorio.ArmTotal(referencia,uc,cliente,dist)

                    dic['ArmazenadoMensal'] = men
                    dic['ArmazenadoTotal'] = total

                    dic = Relatorio.TrataDic(dic)

                else:

                    print('deu erro celesc')

                    """ try:
                        dadosgerador = Relatorio.valorGerador_Celesc(referencia,cli, uc)
                        dic.update(dadosgerador) 

                        men = Relatorio.ArmMensal(referencia,uc,cliente,dist)
                        total = Relatorio.ArmTotal(referencia,uc,cliente,dist)

                        CredB = Relatorio.CredBruto_Celesc(referencia,cli)

                        dic['ArmazenadoMensal'] = men
                        dic['ArmazenadoTotal'] = total

                        split = Relatorio.splitConsumo_Celesc(referencia,uc,cli,dist)
                        dic['CompensadoMes'] = int(split)
            

                        somaSplit = Relatorio.SomaSplit_Celesc(referencia,cli,dist)

                        dic['valorBruto'] = int(str(round(CredB*(split/somaSplit),2)).replace('.',''))
                        
                        try:
                            dic['UnitBruto'] = round(round(dic['valorBruto']/dic['CompensadoMes'],1)/100,3)
                        except:
                            dic['UnitBruto'] = 0
                        
                        try:
                            valor = int(str(dadosgerador['fatura']).replace('.','').replace(',',''))

                        except:
                            valor = 0
                        
                        try:
                            dic['faturaGerador'] = int(str(dic['valorBruto']))-valor
                            dic['UnitFatura'] = round(int(dic['faturaGerador'])/dic['CompensadoMes']/100,3)
                        except:
                            dic['faturaGerador'] = dic['valorBruto']
                            dic['UnitFatura'] = dic['UnitBruto']

                        try:
                            dic['descontoCliente'] = str(round(dadosgerador['descontoCli']*dic['valorBruto'],2))[0:len(str(dic['faturaGerador']))]
                            dic['UnitCliente'] = round((int(dic['descontoCliente'])/dic['CompensadoMes'])/100,3)
                        except:
                            dic['descontoCliente'] = dic['faturaGerador']
                            dic['UnitCliente'] = dic['UnitFatura']

                        try:
                            dic['descontoGestao'] = str(int(dic['descontoCliente'])*int(dadosgerador['descontoGest']))[0:len(str(dic['descontoCliente']))]
                            dic['UnitGestao'] = round((int(dic['descontoGestao'])/int(dic['CompensadoMes']))/100,3)
                        except:
                            dic['descontoGestao'] = dic['descontoCliente']
                            dic['UnitGestao'] = 0
                            

                        FM66 =  dic['faturaGerador'] # insira o valor correspondente aqui
                        HU4 =  0.87  # insira o valor correspondente aqui
                        E66 =  valor # insira o valor correspondente aqui

                        try:
                            result = FM66 * HU4
                        except:
                            result = 0


                        result = result if result > 0 else -E66
                        valor_imposto = result*(dadosgerador['descontoGest'])-dadosgerador['imposto']

                        try:
                            dic['descontoImposto'] = str(int(valor_imposto))[0:len(str(dic['descontoCliente']))]
                        except:
                            dic['descontoImposto'] = dic['descontoGestao'] 
                        
                        
                        dic['ValorFinal'] = dic['descontoImposto']

                        
                        
                        dic = Relatorio.TrataDic(dic)

                    except IndexError:  
                        return redirect('/relatorios/?status=1')
                    
                    except ZeroDivisionError:
                        return redirect('/relatorios/?status=2') """
                
            if dist == 1:

                #print('credito kwh ->',Relatorio.CredCompensado(referencia,cli))# relatorios_consumidor
                #print('Credito R$ ->',Relatorio.CreditoBruto(referencia))# relatorios_consumidor
                #print('Arm kwh ->', Relatorio.SaldoFinalCli(referencia,cli))# relatorios_azul
                #print('consumo total->', Relatorio.TotalConsumo(referencia)[0][1])# relatorios_consumidor

                if referencia in historico:
                    dadosgerador = Relatorio.valorGerador(referencia,cli, uc)
                    dic.update(dadosgerador) 

                    valoresHistorico = Relatorio.SelecionaHistorico(referencia,uc)
                    dic.update(valoresHistorico) 

                    men = Relatorio.ArmMensal(referencia,uc,cliente,dist)
                    total = Relatorio.ArmTotal(referencia,uc,cliente,dist)

                    dic['ArmazenadoMensal'] = men
                    dic['ArmazenadoTotal'] = total

                    dic = Relatorio.TrataDic(dic)

                else:
                    
                    print('deu erro copel')

                    """ try:
                        men = Relatorio.ArmMensal(referencia,uc,cliente,dist)
                        total = Relatorio.ArmTotal(referencia,uc,cliente,dist)

                        dic['ArmazenadoMensal'] = men
                        dic['ArmazenadoTotal'] = total
                    
                        split = Relatorio.splitConsumo(referencia,uc,cli,dist)

                        dic['CompensadoMes'] = int(split)

                        CredB = Relatorio.CreditoBruto(referencia)
                        
                        somaSplit = Relatorio.SomaSplit(referencia,cli,total,dist)
                        
                        dic['valorBruto'] = round(CredB*(split/somaSplit),2)

                        try:
                            dic['UnitBruto'] = round(dic['valorBruto']/dic['CompensadoMes'],3)
                        except:
                            dic['UnitBruto'] = 0

                        dadosgerador = Relatorio.valorGerador(referencia,cli, uc)
                        
                    
                        try:
                            dic['descontoCliente'] = int(round(dadosgerador['descontoCli']*dic['valorBruto'],2))
                            dic['UnitCliente'] = round((dic['descontoCliente']/dic['CompensadoMes'])/100,3)
                        except:
                            dic['descontoCliente'] = dic['valorBruto']
                            dic['UnitCliente'] = dic['UnitBruto']

                        try:
                            dic['descontoGestao'] = dic['descontoCliente']*dadosgerador['descontoGest']
                            dic['descontoGestao'] = str(dic['descontoGestao'])[0:len(str(dic['descontoCliente']))]

                            dic['UnitGestao'] = round(int(dic['descontoGestao'])/dic['CompensadoMes']/100,3)
                        except:
                            dic['descontoGestao'] = dic['descontoCliente']
                            dic['UnitGestao'] = dic['UnitCliente']

                        
                        try:
                            dic['faturaGerador'] = int(str(dic['descontoGestao']).replace('.',''))-int(str(dadosgerador['fatura']).replace('.',''))
                        except:
                            dic['faturaGerador'] = -int(str(dadosgerador['fatura']))
                        
                        try:
                            dic['UnitFatura'] = round(int(dic['faturaGerador'])/dic['CompensadoMes']/100,3)
                        except:
                            dic['UnitFatura'] = 0

                        try:
                            dic['descontoImposto'] = int(dic['faturaGerador'])-int(str(dadosgerador['imposto']).replace(',','').replace('.',''))
                        except:
                            dic['descontoImposto'] = dic['faturaGerador'] 
                        
                        
                        dic['ValorFinal'] = dic['descontoImposto']
                    
                        dic.update(dadosgerador) 
                        dic = Relatorio.TrataDic(dic)

                        #print()
                        #print('Credito Bruto ->',Relatorio.CreditoBruto(referencia))
                        #print()

                    except IndexError:  
                        return redirect('/relatorios/?status=1')
                    except ZeroDivisionError:
                        return redirect('/relatorios/?status=2') """
        else:
            dic=None
            
        return render(request, 'relatorios.html',{'dadosgerador':dic,'id':id, 'clientes':clientes, 'ref':ref[::-1],'und':und, 'uc':uc, 'update':update, 'nivel':nivel, 'nomeDist':nomeDist, 'nome':nomeUser, 'dist':dist})
    else:
        return redirect('/login/?status=1')
    
def injetado(request):
    if request.session.get('usuarioAdmin'):
        if request.session.get('usuarioAdmin'):
                adm = request.session['usuarioAdmin']
                nomeUser = Administradores.objects.get(id=adm)

        elif request.session.get('usuario'):
            gerador = request.session['usuario']
            nomeUser = Geradores.objects.get(id=gerador)

        nivel=1
        dist = request.GET.get("dist")

        distribuidoras = Distribuidoras.objects.filter(cliente_id=cli)

        if (dist and dist != 'Selecione a Distribuidora'):

            distribuidoras = Distribuidoras.objects.filter(cliente_id=cli)

            if dist =='1':
                und= Relatorio.ucs(cli)
                ref = Relatorio.Referencias()
                injetada = Relatorio.EnergiaInj()
                
            elif dist =='2':
                und= Relatorio.ucs_Celesc(cli)
                ref = Relatorio.Referencias_Celesc()
                injetada = Relatorio.Injecao_Celesc(cli)
            
            rep = Relatorio.agrega_lista(injetada,dist)

            c = tuple(rep)
            dados_paginator = Paginator(c,10*112)
            page_num = request.GET.get('page')
            page = dados_paginator.get_page(page_num)

            nomes = Relatorio.NomesGeradores(dist)

            return render(request, 'injetado.html', {'nivel':nivel,'nome':nomeUser,'injetados':page.object_list[::-1],'ucs':und, 'page':page, 'opcoes':distribuidoras,'nomes':nomes,'nivel':nivel})
        else:
            distribuidoras = Distribuidoras.objects.filter(cliente_id=cli)

            return render(request, 'injetado.html', {'nivel':nivel,'nome':nomeUser,'distribuidoras':distribuidoras})
    else:
        return redirect('/login/?status=1')
    
def armazenadoMes(request):
    if request.session.get('usuarioAdmin'):
        nivel=1
        dist = request.GET.get("dist")

        if (dist and dist != 'Selecione a Distribuidora'):

            distribuidoras = Distribuidoras.objects.filter(cliente_id=cli)

            if dist =='1':
                und= Relatorio.ucs(cli)
                ref = Relatorio.Referencias()
                
            elif dist =='2':
                und= Relatorio.ucs_Celesc(cli)
                ref = Relatorio.Referencias_Celesc()
                        
            arm = Relatorio.ArmMensalTodos(dist)
            rep = Relatorio.agrega_lista(arm,dist)
            
            c = tuple(rep)
            dados_paginator = Paginator(c,10*112)
            page_num = request.GET.get('page')
            page = dados_paginator.get_page(page_num)

            nomes = Relatorio.NomesGeradores(dist)

            return render(request, 'armazenado_mensal.html', {'armazenados':page.object_list[::-1],'ucs':und, 'page':page, 'opcoes':distribuidoras,'nomes':nomes,'nivel':nivel})
        else:
            distribuidoras = Distribuidoras.objects.filter(cliente_id=cli)

            return render(request, 'armazenado_mensal.html', {'distribuidoras':distribuidoras,'nivel':nivel})
    else:
        return redirect('/login/?status=1')
    
def armazenadoTotal(request):
    if request.session.get('usuarioAdmin'):
        if request.session.get('usuarioAdmin'):
                adm = request.session['usuarioAdmin']
                nomeUser = Administradores.objects.get(id=adm)

        elif request.session.get('usuario'):
            gerador = request.session['usuario']
            nomeUser = Geradores.objects.get(id=gerador)

        nivel=1
        dist = request.GET.get("dist")
        if (dist and dist != 'Selecione a Distribuidora'):

            distribuidoras = Distribuidoras.objects.filter(cliente_id=cli)

            if dist =='1':
                und= Relatorio.ucs(cli)
                ref = Relatorio.Referencias()
                
            elif dist =='2':
                und= Relatorio.ucs_Celesc(cli)
                ref = Relatorio.Referencias_Celesc()
                        
            arm = Relatorio.ArmTotalTodos(dist)
            rep = Relatorio.agrega_lista(arm,dist)
            
            c = tuple(rep)
            dados_paginator = Paginator(c,10*112)
            page_num = request.GET.get('page')
            page = dados_paginator.get_page(page_num)

            nomes = Relatorio.NomesGeradores(dist)

            return render(request, 'armazenado_total.html', {'nome':nomeUser,'armazenados':page.object_list[::-1],'ucs':und, 'page':page, 'opcoes':distribuidoras,'nomes':nomes,'nivel':nivel})
        else:
            distribuidoras = Distribuidoras.objects.filter(cliente_id=cli)

            return render(request, 'armazenado_total.html', {'nome':nomeUser,'distribuidoras':distribuidoras,'nivel':nivel})
    else:
        return redirect('/login/?status=1')
    
def ConsumoReman(request):
    if request.session.get('usuarioAdmin'):
        nivel=1
        Ref = Relatorio.Referencias()
        und= Relatorio.ucs()
        undCons= Relatorio.ucsConsum()

        lista = []
        for uc in undCons:
            r = Relatorio.ContaConsumo(uc)
            t=[]
            for valor in r:
                t.append(valor[0])
            
            lista.append(t)
        

        media = []
        for i in lista:
            r = i[-13:-1]
            r=Relatorio.TrasformaemvalorLista(r)
            tamanho = len(r)
            m= (sum(r)/tamanho)-100
            if '0' in r:
                m=0
            
            media.append(m)

        repositorio = []
        for r in Ref:
            repoMaiorSoma = []
            repoMaior = []
            repoMaior.append(r)
            repo = Relatorio.consumoTotal(r)
            somaCons = Relatorio.TotalConsumo(r)
            maior = Relatorio.consumoTotalMaior(r)
            count = Relatorio.CountConsumo(r)
            armaz = Relatorio.SaldoFinalCli(r,cli)
            menor = Relatorio.CountConsumoMenor(r)
            
            for i in maior:
                if i[1]>0:
                    repoMaior.append(i[1])

            repoMaiorSoma.append(repo[0][0])
            repoMaiorSoma.append(int(repo[0][1]))
            repoMaiorSoma.append(len(repoMaior[1:])*100)
            repoMaiorSoma.append(int(repo[0][1]-(len(repoMaior[1:])*100)))
            repoMaiorSoma.append(int((1-((repo[0][1]-(len(repoMaior[1:])*100))/somaCons[0][1]))*100))
            repoMaiorSoma.append(menor[0][0])
            repoMaiorSoma.append(count[0][0])
            repoMaiorSoma.append(int((armaz/sum(media))*100))
            
            repositorio.append(tuple(repoMaiorSoma))
        
        repositorio = tuple(repositorio)
        
        dados_paginator = Paginator(repositorio[::-1],12)
        page_num = request.GET.get('page')
        page = dados_paginator.get_page(page_num)
        return render(request,'consumoRemanescente.html',{'remanescente':page.object_list, 'page':page,'nivel':nivel})
    else:
        return redirect('/login/?status=1')
    
def Check(request):
    if request.session.get('usuarioAdmin'):
        nivel=1
        Ref = Relatorio.Referencias()
        und= Relatorio.ucsConsum()

        repositorio = []
        for ref in Ref[-2:]:
            RefAnt = Relatorio.ReferenciaAnterior(ref)
            undCons= Relatorio.ucsStatusConsum(ref)
            remanescente = Relatorio.consumoTotalMaior(ref)
            creditocli = Relatorio.CreditoCli(ref)
            saldoFinal = Relatorio.SaldoFinalCliInd(ref)
            saldoAnt = Relatorio.SaldoFinalCliInd(RefAnt)

            repo = []
            lista = []
            for uc in und:
                r = Relatorio.ContaConsumo(uc)
                t=[]
                for valor in r:
                    t.append(valor[0])
                lista.append(t)
            
            media = []
            for i in lista:
                r = i[-13:-1]
                r=Relatorio.TrasformaemvalorLista(r)
                tamanho = len(r)
                m= (sum(r)/tamanho)-100
                if '0' in r:
                    m=0   
                media.append(m)
    
            for u,s,m,i,r,k,p,t in zip(undCons[0],undCons[1],media,lista,remanescente,creditocli, saldoFinal,saldoAnt):
                if m <0:
                    m=0
                
                if p>t:
                    check = 'positivo'
                else:
                    check = 'negativo'

                repo.append((ref,u,s,int(m),i[-2],int(r[1]),k[0],p[0],t[0],check))
            
            repositorio.append(tuple(repo))

        dados_paginator = Paginator(repositorio[::-1],1)
        page_num = request.GET.get('page')
        page = dados_paginator.get_page(page_num)

        return render(request,'check.html',{"check":page.object_list, 'page':page,'nivel':nivel})

    else:
        return redirect('/login/?status=1')
    
#---Consumidor---#
def consumo(request):
    
    if request.session.get('usuarioAdmin'):

        if request.session.get('usuarioAdmin'):
                adm = request.session['usuarioAdmin']
                nomeUser = Administradores.objects.get(id=adm)

        elif request.session.get('usuario'):
            gerador = request.session['usuario']
            nomeUser = Geradores.objects.get(id=gerador)

        nivel=1
        dist = request.GET.get("dist")
        distribuidoras = Distribuidoras.objects.filter(cliente_id=cli)

        if (dist and dist != 'Selecione a Distribuidora'):

            distribuidoras = Distribuidoras.objects.filter(cliente_id=cli)

            if dist =='1':
                und= Relatorio.ucs(cli)
                ref = Relatorio.Referencias()
                consumo = Relatorio.consumoGd()
                
            elif dist =='2':
                und= Relatorio.ucs_Celesc(cli)
                ref = Relatorio.Referencias_Celesc()
                consumo = Relatorio.consumoGd_Celesc()
            
            rep = Relatorio.agrega_lista(consumo,dist)

            c = tuple(rep)
            dados_paginator = Paginator(c,10*112)
            page_num = request.GET.get('page')
            page = dados_paginator.get_page(page_num)

            nomes = Relatorio.NomesGeradores(dist)

            
            return render(request, 'consumo.html', {'nome':nomeUser,'consumos':page.object_list[::-1],'ucs':und, 'page':page, 'opcoes':distribuidoras,'distribuidora':dist,'nomes':nomes,'nivel':nivel})
        else:
            distribuidoras = Distribuidoras.objects.filter(cliente_id=cli)

            return render(request, 'consumo.html', {'nome':nomeUser,'distribuidoras':distribuidoras,'nivel':nivel}) 
    else:
        return redirect('/login/?status=1')
    
def update(request,ref):
    if request.session.get('usuarioAdmin'):
        nivel=1
        distribuidora = request.GET.get('distribuidora')
        if distribuidora == '1':
            resultado = Gerador.objects.filter(Referencia=ref)
        elif distribuidora == '2':
            resultado = Gerador_Celesc.objects.filter(Referencia=ref)

        if request.session.get('usuarioAdmin'):
                adm = request.session['usuarioAdmin']
                nomeUser = Administradores.objects.get(id=adm)

        elif request.session.get('usuario'):
            gerador = request.session['usuario']
            nomeUser = Geradores.objects.get(id=gerador)

        return render(request, 'updateRelatorio.html', {'nome':nomeUser,"resultado":resultado,"distribuidora":distribuidora,'nivel':nivel}) 
    else:
        return redirect('/login/?status=1')

def atualizar(request,id):
    if request.session.get('usuarioAdmin'):
        nivel=1
        distribuidora = request.GET.get('distribuidora')
        if distribuidora == '1':
            consumo = Gerador.objects.get(id=id)
        elif distribuidora == '2':
            consumo = Gerador_Celesc.objects.get(id=id)
        
        if request.session.get('usuarioAdmin'):
                adm = request.session['usuarioAdmin']
                nomeUser = Administradores.objects.get(id=adm)

        elif request.session.get('usuario'):
            gerador = request.session['usuario']
            nomeUser = Geradores.objects.get(id=gerador)

        return render(request, 'atualizaRelatorio.html',{'nome':nomeUser, "consumo":consumo,"distribuidora":distribuidora,'nivel':nivel}) 
    else:
        return redirect('/login/?status=1')
    
def Alterar(request,id):
    if request.session.get('usuarioAdmin'):

        distribuidora = request.GET.get('distribuidora')
        Energia_Ativa = request.GET.get("Energia_Ativa")

        if distribuidora == '1':
            consumos = Gerador.objects.get(id=id)
        elif distribuidora == '2':
            consumos = Gerador_Celesc.objects.get(id=id)
        
        consumos.Energia_Ativa = Energia_Ativa
        consumos.save()
        return redirect(consumo)
    else:
        return redirect('/login/?status=1')
#---Gerador----#
def geracao(request):
    if request.session.get('usuarioAdmin'):
        nivel=1
        dist = request.GET.get("dist")

        if request.session.get('usuarioAdmin'):

            adm = request.session['usuarioAdmin']
            nomeUser = Administradores.objects.get(id=adm)


        elif request.session.get('usuario'):
            gerador = request.session['usuario']
            nomeUser = Geradores.objects.get(id=gerador)

        distribuidoras = Distribuidoras.objects.filter(cliente_id=cli)

        if (dist and dist != 'Selecione a Distribuidora'):

            distribuidoras = Distribuidoras.objects.filter(cliente_id=cli)

            if dist =='1':
                und= Relatorio.ucs(cli)
                ref = Relatorio.Referencias()
                geracao = Relatorio.Geracao()
                
            elif dist =='2':
                und= Relatorio.ucs_Celesc(cli)
                ref = Relatorio.Referencias_Celesc()
                geracao = Relatorio.Geracao_Celesc()
            
            rep = Relatorio.agrega_lista(geracao,dist)

            c = tuple(rep)
            dados_paginator = Paginator(c,10*112)
            page_num = request.GET.get('page')
            page = dados_paginator.get_page(page_num)

            nomes = Relatorio.NomesGeradores(dist)

            return render(request, 'geracao.html', {'nome':nomeUser,'gerados':page.object_list[::-1],'ucs':und, 'page':page, 'opcoes':distribuidoras, 'distribuidora':dist,'nomes':nomes,'nivel':nivel})
        else:
            distribuidoras = Distribuidoras.objects.filter(cliente_id=cli)
            return render(request, 'geracao.html', {'nome':nomeUser,'distribuidoras':distribuidoras,'nivel':nivel})
    else:
        return redirect('/login/?status=1')
    
def updategeracao(request,ref):
    if request.session.get('usuarioAdmin'):
        nivel=1
        distribuidora = request.GET.get('distribuidora')

        if distribuidora == '1':
            resultado = Gerador.objects.filter(Referencia=ref)
        elif distribuidora == '2':
            resultado = Gerador_Celesc.objects.filter(Referencia=ref)
        
        if request.session.get('usuarioAdmin'):
            adm = request.session['usuarioAdmin']
            nomeUser = Administradores.objects.get(id=adm)


        elif request.session.get('usuario'):
            gerador = request.session['usuario']
            nomeUser = Geradores.objects.get(id=gerador)

        return render(request, 'updateRelatorioGerador.html', {'nome':nomeUser, "resultado":resultado,"distribuidora":distribuidora,'nivel':nivel}) 
    else:
        return redirect('/login/?status=1')
    
def atualizaGerador(request,id):
    if request.session.get('usuarioAdmin'):
        nivel=1
        distribuidora = request.GET.get('distribuidora')

        if distribuidora == '1':
            gerado = Gerador.objects.get(id=id)
        elif distribuidora == '2':
            gerado = Gerador_Celesc.objects.get(id=id)
        
        if request.session.get('usuarioAdmin'):
            adm = request.session['usuarioAdmin']
            nomeUser = Administradores.objects.get(id=adm)

        elif request.session.get('usuario'):
            gerador = request.session['usuario']
            nomeUser = Geradores.objects.get(id=gerador)

        return render(request, 'atualizaRelatorioGerador.html',{'nome':nomeUser, "gerado":gerado,"distribuidora":distribuidora,'nivel':nivel}) 
    else:
        return redirect('/login/?status=1')
    
def Alterargerado(request,id):
    if request.session.get('usuarioAdmin'):
        distribuidora = request.GET.get('distribuidora')
        Energia_Injetada = request.GET.get("Energia_Injetada")

        if distribuidora == '1':
            gerados = Gerador.objects.get(id=id)
        elif distribuidora == '2':
            gerados = Gerador_Celesc.objects.get(id=id)
        
        gerados.Energia_Injetada = Energia_Injetada
        gerados.up = 1
        gerados.save()
        return redirect(geracao)
    else:
        return redirect('/login/?status=1')

def liberar_acesso(request):

    if request.session.get('usuarioAdmin'):
 
        dist = request.GET.get("dist")
        cli = 1
        adm = request.session['usuarioAdmin']
        nomeUser = Administradores.objects.get(id=adm)
        distribuidoras = Distribuidoras.objects.filter(cliente_id=cli)
        nivel=1


        if (dist and dist != 'Selecione a Distribuidora'):
            
            if dist == '1':
                geradores = Relatorio.ReferenciasAdm()
            if dist == '2':
                geradores = Relatorio.ReferenciasAdm_celesc()

            return render(request, 'LiberarAcesso.html', {'nome':nomeUser, 'dist':dist, 'nivel':nivel,'geradores':geradores[::-1]})
        else:
            return render(request, 'LiberarAcesso.html', {'nome':nomeUser,'distribuidoras':distribuidoras, 'nivel':nivel})
    else:
        return redirect('/login/?status=1')
    
def alterar_acesso(request,ref):

    if request.session.get('usuarioAdmin'):
        nivel=1
        dist = request.GET.get('dist')
        status = request.GET.get('status')
        adm = request.session['usuarioAdmin']
        nomeUser = Administradores.objects.get(id=adm)

        return render(request, 'AlterarAcesso.html', {'status':status,'ref':ref,'nome':nomeUser,'dist':dist,'nivel':nivel})
    else:
        return redirect('/login/?status=1')

def salvar_acesso(request,ref):

    status = request.GET.get('status')
    dist = request.GET.get('dist')

    if dist == '1':
        Relatorio.Atualiza_liberado_copel(ref,status)
    if dist == '2':  
        Relatorio.Atualiza_liberado_celesc(ref,status)

    return redirect(liberar_acesso)
