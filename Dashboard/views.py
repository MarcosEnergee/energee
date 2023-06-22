from django.shortcuts import render,redirect
from Relatorios.relatorio import Relatorio
from datetime import datetime
from django.http.response import HttpResponse, JsonResponse
Relatorio = Relatorio()


def grafico_admin(request):

    if request.session.get('usuarioAdmin'):
        consumo_celesc = Relatorio.consumoGraficoAdmin_celesc()
        geracao_celesc = Relatorio.GeracaoGraficoAdmin_celesc()
        consumo = Relatorio.consumoGraficoAdmin()
        geracao = Relatorio.GeracaoGraficoAdmin()

        meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
        consum = []
        gerac = []
        consum_celesc = []
        gerac_celesc = []
        labels = []

        mes = datetime.now().month
        ano = datetime.now().year

        for i in range(12):
            mes -= 1
            if mes == 0:
                mes = 12
                ano -= 1
            refsitem = str(mes)+str(ano)

            listaConsumo = []
            listaGeracao = []
            listaConsumo_celesc = []
            listaGeracao_celesc = []
            for c,g in zip(consumo,geracao):
                mesref = int(c[1][0:2])
                anoref = c[1]
                refbanco = str(mesref)+str(anoref)[2:6]

                
                if refbanco == refsitem:
                    listaConsumo.append(int(c[2]))
                    listaGeracao.append(int(g[2]))

            
            for s,h in zip(consumo_celesc,geracao_celesc):
                mesref = int(s[1][0:2])
                anoref = s[1]
                refbanco = str(mesref)+str(anoref)[2:6]
                if refbanco == refsitem:
                    
                    listaConsumo_celesc.append(int(s[2]))
                    listaGeracao_celesc.append(int(h[2]))


            consum.append(sum(listaConsumo))
            gerac.append(sum(listaGeracao))
            consum_celesc.append(sum(listaConsumo_celesc))
            gerac_celesc.append(sum(listaGeracao_celesc))
            labels.append(meses[mes-1])


            gerac_celesc = [349500,303002,305253,261261,279786,266857,213970,249974,270668,221991,191984,185212,198449]

            consum_celesc = [274902,278532,254098,254357,220864,270972,250318,248611,197049,184792,175680,135808]

            consum = [90912,100247,98878,90454,76557,137844,191416,210824,234143,213495,212736,140832]

            gerac = [145762,139392,115235,93325,162690,213034,194277,258807,245479,218964,232610,234637]

        data_json = {'consumo': consum,'geracao': gerac, 'labels': labels[::-1],'consumo_celesc': consum_celesc[::-1],'geracao_celesc': gerac_celesc[::-1]}
    
    elif request.session.get('usuario'):

        uc = request.session['uc']

        if request.session['dist'] == 1:
            
            consumo = Relatorio.consumoGrafico(uc)
            geracao = Relatorio.GeracaoGrafico(uc) 

            meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
            consum = []
            gerac = []
            labels = []
            mes = datetime.now().month
            ano = datetime.now().year

            for i in range(12):
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

        if request.session['dist'] == 2:
            
            consumo = Relatorio.consumoGrafico_celesc(uc)
            geracao = Relatorio.GeracaoGrafico_celesc(uc)
        

            meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
            consum = []
            gerac = []
            labels = []
            mes = datetime.now().month
            ano = datetime.now().year

            for i in range(12):
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
                        consum.append(int(c[2]))
                        gerac.append(int(g[2]))

            data_json = {'consumo': consum[::-1],'geracao': gerac[::-1], 'labels': labels[::-1]}

    
    return JsonResponse(data_json)

def dashboard(request):
    if request.session.get('usuarioAdmin') or request.session.get('usuario'):
        
        mes = datetime.now().month-2
        if len(str(mes)) < 2:
            mes = '0'+str(mes)
        ano = datetime.now().year
        ref = str(mes)+str(ano)

        if request.session.get('usuarioAdmin'):
            nivel=1
            dist = False
            
            N_geradores = Relatorio.ContaGeradores(1)
            N_consumidores = Relatorio.ContaConsumidores(1)
            geracao = Relatorio.GeracaoAdmin(ref)
            consumo = Relatorio.ConsumoAdmin(ref)
            injetada = Relatorio.InjetadoAdmin(ref)

            valor = {}
            valor['cabecalho'] = 'adm'
            valor['geradores'] = N_geradores
            valor['consumidores'] = N_consumidores
            valor['geracao'] = geracao
            valor['consumo'] = consumo
            valor['injecao'] = injetada

            
        #------------------------------------------------------#
        else:

            uc = request.session['uc']

            if request.session['dist'] == 1:
                consumo = Relatorio.consumoGrafico(uc,ref)[0][2]
                geracao = Relatorio.GeracaoGrafico(uc,ref)[0][2]
                injetada = int(Relatorio.InjetadaInd(uc,1,ref))
                armazenado = Relatorio.ArmazenadoNaUnd(uc,ref)[0][2]

            if request.session['dist'] == 2:
                consumo = Relatorio.consumoGrafico_celesc(uc,ref)[0][2]
                geracao = Relatorio.GeracaoGrafico_celesc(uc,ref)[0][2]
                injetada = Relatorio.InjetadaInd_Celesc(uc,1,ref)
                armazenado = Relatorio.ArmazenadoNaUnd_celesc(uc,ref)[0][2]

            nivel=0
            dist = request.session['dist']
            valor = {}

            valor['cabecalho'] = 'gerador'
            valor['consumo'] = consumo
            valor['geracao'] = geracao
            valor['injetada'] = injetada
            valor['armazenado'] = armazenado


        if request.session.get('usuario'):
            id = request.session["usuario"]
        if request.session.get('usuarioAdmin'):
            id=None

        nome = request.session['nome']
        return render(request, 'dashboard.html',{'nome':nome,'nivel':nivel,'id':id,'valores':valor, 'dist':dist})
    else:
        return redirect('/login/?status=1')