from django.db import connection

class Relatorio:

    #---------------Dashboard------------------------------------------
    def ContaGeradores(self,adm):
        geradores = {}
        query = f' SELECT count(*) FROM `Geradores_geradores` WHERE admin_id={adm} '
        cursor = connection.cursor()
        cursor.execute(query)
        geradores['total'] = cursor.fetchall()[0][0]

        query = f' SELECT count(*) FROM `Geradores_geradores` WHERE admin_id={adm} AND distribuidora_id=1 '
        cursor = connection.cursor()
        cursor.execute(query)
        geradores['copel'] = cursor.fetchall()[0][0]

        geradores['celesc'] = geradores['total']-geradores['copel']
        
        return geradores
    
    def ContaConsumidores(self,adm):
        consumidores = {}
        query = f' SELECT count(*) FROM `Consumidores_consumidores` WHERE admin_id={adm} '
        cursor = connection.cursor()
        cursor.execute(query)
        consumidores['total'] = cursor.fetchall()[0][0]

        query = f' SELECT count(*) FROM `Consumidores_consumidores` WHERE admin_id={adm} AND distribuidora_id=1 '
        cursor = connection.cursor()
        cursor.execute(query)
        consumidores['copel'] = cursor.fetchall()[0][0]

        consumidores['celesc'] = consumidores['total']-consumidores['copel']
        
        return consumidores

    def consumoGraficoAdmin(self):
        query = f'SELECT uc,referencia,qtdconsumo-qtdmptte FROM relatorios_consumidor'

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        return resultado
    
    def consumoGraficoAdmin_celesc(self):
        query = ' SELECT uc,Referencia,Energia_Ativa+Energia_AtivaFP FROM relatorios_gerador_celesc '

        cursor = connection.cursor()
        cursor.execute(query)
        resultado = cursor.fetchall()

        return resultado
    
    def GeracaoGraficoAdmin(self):
        query = ' SELECT uc,Referencia, SUM(Energia_Injetada) FROM `relatorios_gerador` GROUP BY Referencia'

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        return resultado
    
    def GeracaoGraficoAdmin_celesc(self):
        query = ' SELECT uc,Referencia,Energia_Injetada+Energia_InjetadaFP FROM relatorios_gerador_celesc '

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        return resultado

    def GeracaoAdmin(self, referencia):

        geracao = {}
        query = f' SELECT SUM(Energia_Injetada) FROM relatorios_gerador WHERE referencia= {referencia}'
        cursor = connection.cursor()
        cursor.execute(query)
        try:
            geracao['copel'] = int(cursor.fetchall()[0][0])
        except:
            geracao['copel'] = 0
        

        query = f' SELECT SUM(Energia_Injetada+Energia_InjetadaFP) FROM relatorios_gerador_celesc WHERE referencia= {referencia}'
        cursor = connection.cursor()
        cursor.execute(query)

        try:
            geracao['celesc'] = int(cursor.fetchall()[0][0])
        except:
            geracao['celesc'] = 0
    
        geracao['total'] = geracao['copel']+geracao['celesc']

        return geracao
    
    def ConsumoAdmin(self, referencia):

        consumo = {}
        query = f' SELECT SUM(Energia_Ativa) FROM relatorios_gerador WHERE referencia= {referencia}'
        cursor = connection.cursor()
        cursor.execute(query)
        try:
            consumo['copel'] = int(cursor.fetchall()[0][0])
        except:
            consumo['copel'] = 0

        query = f' SELECT SUM(Energia_Ativa) FROM relatorios_gerador_celesc WHERE referencia= {referencia}'
        cursor = connection.cursor()
        cursor.execute(query)

        try:
            consumo['celesc'] = int(cursor.fetchall()[0][0])
        except:
            consumo['celesc'] = 0

        consumo['total'] = consumo['copel']+consumo['celesc']

        return consumo

    def InjetadoAdmin(self, referencia):

        injetado = {}
        query = f' SELECT SUM(Energia_Injetada)-SUM(Energia_Ativa) FROM relatorios_gerador WHERE referencia= {referencia}'
        cursor = connection.cursor()
        cursor.execute(query)

        try:
            injetado['copel'] = int(cursor.fetchall()[0][0])
        except:
            injetado['copel'] = 0

        query = ' SELECT Energia_Injetada, Energia_Ativa, Energia_InjetadaFP,Energia_AtivaFP '
        query += f' FROM relatorios_gerador_celesc  WHERE referencia= {referencia}'
        cursor = connection.cursor()
        cursor.execute(query)
        resultado = cursor.fetchall()

        lista = []
        for i in resultado:

            injetada = int(i[0])-int(i[1])
            if injetada <0:
                injetada=0

            if int(i[2]) > 0 :
                acrescimo = int(i[2])-int(i[3])
                if acrescimo <0:
                    acrescimo=0

                injetada = (injetada*1.62)+acrescimo

            if injetada > 0:

                lista.append(injetada)
        
        injetado['celesc'] = int(sum(lista))

        injetado['total'] = int(injetado['copel']+injetado['celesc'])
        

        return injetado
    #-----------------------------------------------------------------#

    def NomesGeradores(self,dist):
        
        query = f' SELECT nome FROM `Geradores_geradores` WHERE distribuidora_id={dist} '
        cursor = connection.cursor()
        cursor.execute(query)
        resultado = cursor.fetchall()

        lista = []
        for i in resultado:
            lista.append(i[0])

        return lista
    
    def ApagarArmM(self,dist):

        query = f'DELETE FROM relatorios_ArmazenamentoMensal WHERE distribuidora_id={dist} '
        
        cursor = connection.cursor()
        cursor.execute(query)

        cursor.fetchone()

    def ApagarArmT(self,dist):

        query = f'DELETE FROM relatorios_armazenamentototal WHERE distribuidora_id={dist}  '
        
        cursor = connection.cursor()
        cursor.execute(query)

        cursor.fetchone()
        
    def AtualizarUp(self):
        
        query = f'UPDATE relatorios_gerador SET up = 0'
        
        cursor = connection.cursor()
        cursor.execute(query)

        cursor.fetchone()

    def AtualizarUp_Celesc(self):
        
        query = f'UPDATE relatorios_gerador_celesc SET up = 0'
        
        cursor = connection.cursor()
        cursor.execute(query)

        cursor.fetchone()

    def VerificaUpdate(self):

        query = f' SELECT * FROM relatorios_gerador WHERE up=1 '

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()
        
        return resultado

    def VerificaUpdate_Celesc(self):

        query = f' SELECT * FROM relatorios_gerador_celesc WHERE up=1 '

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()
        
        return resultado
    
    def inserirAmarzenadoM(self,uc,Referencia,valor,admin_id,distribuidora_id,cliente_id):
        query = 'INSERT INTO relatorios_ArmazenamentoMensal (uc,Referencia,valor,admin_id,distribuidora_id,cliente_id)'
        query+= f' VALUES ("{uc}","{Referencia}","{valor}","{admin_id}","{distribuidora_id}","{cliente_id}")'

        cursor = connection.cursor()
        cursor.execute(query)

        cursor.fetchone()

    def inserirAmarzenadoT(self,uc,Referencia,valor,admin_id,distribuidora_id,cliente_id):
        query = 'INSERT INTO relatorios_armazenamentototal (uc,Referencia,valor,admin_id,distribuidora_id,cliente_id)'
        query+= f' VALUES ("{uc}","{Referencia}","{valor}","{admin_id}","{distribuidora_id}","{cliente_id}")'

        cursor = connection.cursor()
        cursor.execute(query)

        cursor.fetchone()

    def CreditoCli(self,ref):
        query = f'SELECT qtdmptte FROM relatorios_consumidor WHERE referencia= {ref}'

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        return resultado

    def virgulaemponto(self,texto):

        texto = texto.replace(',','.')

        return texto

    def TrasformaemvalorLista(self,lista):
        
        resultado = []
        for i in lista:
            i = self.virgulaemponto(str(i))
            if '.' in i:
                try:
                    valor = float(i)
                except:
                    valor = i
            else:
                try:
                    valor = int(i)
                except:
                    valor = i
                    
        
            resultado.append(valor)

        return resultado

    def TrasformaemvalorUnit(self,valor):
        valor = self.virgulaemponto(str(valor))
        lista = []
        lista.append(valor)
        for i in lista:
            if '.' in i:
                try:
                    valor = float(valor)
                except:
                    valor = valor
            else:
                try:
                    valor = int(valor)
                except:
                    valor = valor

        return valor

    def ReferenciaAnterior(self,referencia):
        referencia = str(referencia)
        mes = referencia[0:2]
        ano = referencia[2:6]

        if mes == '01':
            mes = 12
            ano = int(ano)-1
        else:
            mes = int(mes)-1
            if mes <10:
                mes = '0'+str(mes)

        referencia = str(mes)+str(ano)
        
        return referencia

    def ReferenciaPosterior(self,referencia):
        referencia = str(referencia)
        mes = referencia[0:2]
        ano = referencia[2:6]

        if mes == '12':
            mes = '01'
            ano = int(ano)+1
        else:
            mes = int(mes)+1
            if mes <10:
                mes = '0'+str(mes)

        referencia = str(mes)+str(ano)
        
        return referencia

    def Referencias(self,cli=None):
        lista=[]
        query = f' SELECT DISTINCT(Referencia) FROM relatorios_gerador '

        if cli !=None:
            query += f' WHERE cliente_id= {cli} '

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        for i in resultado:
            lista.append(i[0])
        
        return lista
    
    def ReferenciasAdm(self,cli=None):
        query = f' SELECT DISTINCT(Referencia), liberado FROM relatorios_gerador '

        if cli !=None:
            query += f' WHERE cliente_id= {cli} '

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        dic = []
        for i in resultado:
            valor = {}
            valor['ref'] = i[0]
            valor['status'] = i[1]
            dic.append(valor)
        
        return dic
    
    def ReferenciasAdm_celesc(self,cli=None):
        query = f' SELECT DISTINCT(Referencia), liberado FROM relatorios_gerador_celesc '

        if cli !=None:
            query += f' WHERE cliente_id= {cli} '

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()
        #print(resultado)

        dic = []
        for i in resultado:
            valor = {}
            valor['ref'] = i[0]
            valor['status'] = i[1]
            dic.append(valor)
        
        return dic

    def ReferenciasGerador(self,cli=None):
        lista=[]
        query = f' SELECT DISTINCT(Referencia) FROM relatorios_gerador '
        query += f' WHERE liberado=1 '


        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        for i in resultado:
            lista.append(i[0])
        
        return lista

    def ReferenciasGerador_celesc(self,cli=None):
        lista=[]
        query = f' SELECT DISTINCT(Referencia) FROM relatorios_gerador_celesc '
        query += f' WHERE liberado=1 '


        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        for i in resultado:
            lista.append(i[0])
        
        return lista

    def Referencias_Celesc(self, cli=None):
        lista=[]
        query = f' SELECT DISTINCT(Referencia) FROM relatorios_gerador_celesc '

        if cli !=None:
            query += f' WHERE cliente_id= {cli} '

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        for i in resultado:
            lista.append(i[0])
        
        return lista

    def ucsSelect(self,cli=None,dist=None):
        lista=[]
        query = f' SELECT * FROM Geradores_geradores '

        if cli !=None:
            query += f' WHERE cliente_id= {cli} '
        
        if dist !=None:
            query += f' AND distribuidora_id= {dist} '

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        for i in resultado:
            lista.append([i[0],i[1],i[2]])
        
        return lista
  
    def ucs(self,cli=None):
        lista=[]
        query = f' SELECT uc FROM Geradores_geradores '
        query += f' WHERE distribuidora_id=1 '
        if cli !=None:
            query += f' AND cliente_id= {cli} '

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        for i in resultado:
            lista.append(i[0])
        
        return lista
    
    def ucs_Celesc(self,cli=None):
        lista=[]
        query = f' SELECT uc FROM Geradores_geradores '
        query += f' WHERE distribuidora_id=2 '
        if cli !=None:
            query += f' AND cliente_id= {cli} '

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        for i in resultado:
            lista.append(i[0])
        
        return lista

    def ucsConsum(self):
        lista=[]
        query = ' SELECT DISTINCT(uc) FROM relatorios_consumidor '

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        for i in resultado:
            lista.append(i[0])
        
        return lista

    def ucsStatusConsum(self, ref):
        uc=[]
        status = []
        query = f' SELECT uc,status FROM relatorios_consumidor WHERE referencia= {ref}'

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        for i in resultado:
            uc.append(i[0])
            status.append(i[1])
        
        return uc,status

    def consumoGd(self,referencia=None):
        query = ' SELECT uc,Referencia,Energia_Ativa FROM relatorios_gerador '

        if referencia != None: 
            query += f' WHERE referencia= {referencia}'

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        return resultado

    def consumoGrafico(self,uc, ref=None):
        query = ' SELECT uc,Referencia,Energia_Ativa FROM relatorios_gerador '

        if uc != None: 
            query += f' WHERE uc= {uc}'

        if ref != None: 
            query += f' AND Referencia= {ref}'

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        return resultado

    def ArmazenadoNaUnd(self,uc, ref=None):
        query = ' SELECT uc,Referencia,Saldo_Final FROM relatorios_gerador '

        if uc != None: 
            query += f' WHERE uc= {uc}'

        if ref != None: 
            query += f' AND Referencia= {ref}'

        cursor = connection.cursor()
        cursor.execute(query)
        resultado = cursor.fetchall()

        return resultado
    
    def ArmazenadoNaUnd_celesc(self,uc, ref=None):
        query = ' SELECT uc,Referencia,Saldo_Final FROM relatorios_gerador_celesc '

        if uc != None: 
            query += f' WHERE uc= {uc}'

        if ref != None: 
            query += f' AND Referencia= {ref}'

        cursor = connection.cursor()
        cursor.execute(query)
        resultado = cursor.fetchall()

        return resultado
   
    def consumoGrafico_celesc(self,uc, ref=None):
        query = ' SELECT uc,Referencia,Energia_Ativa+Energia_AtivaFP FROM relatorios_gerador_celesc '

        if uc != None: 
            query += f' WHERE uc= {uc}'
        
        if ref != None: 
            query += f' AND Referencia= {ref}'

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        return resultado

    def GeracaoGrafico(self,uc, ref=None):
        query = ' SELECT uc,Referencia,Energia_Injetada FROM relatorios_gerador '

        if uc != None: 
            query += f' WHERE uc= {uc}'
        
        if ref != None: 
            query += f' AND Referencia= {ref}'

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        return resultado

    def GeracaoGrafico_celesc(self,uc, ref=None):
        query = ' SELECT uc,Referencia,Energia_Injetada+Energia_InjetadaFP FROM relatorios_gerador_celesc '

        if uc != None: 
            query += f' WHERE uc= {uc}'
        
        if ref != None: 
            query += f' AND Referencia= {ref}'

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        return resultado

    def Geracao(self,referencia=None):
        query = ' SELECT uc,Referencia,Energia_Injetada FROM relatorios_gerador '

        if referencia != None: 
            query += f' WHERE referencia= {referencia}'

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        return resultado

    def InjetadaInd(self,uc,cli,ref=None):
        query = f' SELECT Energia_Injetada-Energia_Ativa FROM relatorios_gerador WHERE uc= {uc} ' 
        query += f' AND cliente_id= {cli} '

        if ref != None: 
            query += f' AND referencia= {ref} '

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()[0][0]

        if resultado < 0:
            resultado = 0

        return resultado

    def EnergiaInj(self,referencia=None):
        query = ' SELECT uc,Referencia,Energia_Injetada-Energia_Ativa FROM relatorios_gerador '

        if referencia != None: 
            query += f' WHERE referencia= {referencia}'

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()
        r=[]
        for i in resultado:
            
            if i[2] <0:
                valor=0
            else:
                valor=i[2]
            
            result=[i[0],i[1],valor]
            result = tuple(result)
            r.append(result)
        
        return r

    def SaldoFinalTotal(self,referencia):
        query = ' SELECT SUM(Saldo_Final) '
        query += f' FROM relatorios_azul  WHERE referencia= {referencia}'

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()[0][0]

        return resultado

    def InjecaoTotal(self,referencia,cli):

        query = ' SELECT Energia_Injetada, Energia_Ativa '
        query += f' FROM relatorios_gerador  WHERE referencia= {referencia}'
        query += f' AND cliente_id= {cli} '

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        lista = []
        for i in resultado:
            resultado = int(i[0])-int(i[1])
            if resultado > 0:
                lista.append(resultado)
        
        resultado =sum(lista)

        return resultado

    def valorGerador(self,referencia, cli, uc=None):
        dic = {} 

        query = 'SELECT * FROM relatorios_gerador as r JOIN Geradores_geradores AS g   ON r.uc = g.uc'
        query += f' WHERE r.Referencia= {referencia}'
        query += f' AND r.cliente_id= {cli}'

        if uc != None: 
            query += f' AND r.uc= {uc}'

        cursor = connection.cursor()
        cursor.execute(query)

        r = cursor.fetchall()[0]

        dic['uc'] = r[1]
        dic['nome'] = r[22]
        dic['referencia'] = r[3]
        dic['fatura'] = str(r[2]).replace(',','')
        dic['geracao'] = r[6]
        dic['consumo'] = r[7]
        dic['acumulado'] = r[11]

        if r[18] != 0:
            dic['imposto'] = r[18]
        
        if r[19] != 0:
            dic['descontoCli'] = 100-r[19]
                
        if r[20] != 0:
            dic['descontoGest'] = 100-r[20]
        
        injetada = int(r[6])-int(r[7])
        if injetada <0:
            injetada=0

        dic['injetada'] = injetada
        
        return dic

    def Armazenamento_Copel(self,cli,dist):

        self.insere_mensal_anteriorCopel(cli,dist)
        self.insere_total_anteriorCopel(cli,dist)

        tamanho_gerado = self.Conta_gerados_copel()
        tamanho = self.Conta_ArmazenadosMCopel()

        dif = tamanho_gerado-tamanho

        Ref = self.Lista_ref(dif)
        und= self.ucs(cli)

        mensal = self.ArmMensalTodos(dist,'042023')
        total = self.ArmTotalTodos(dist,'042023')

        t=[]
        m=[]
        for me,to in zip(mensal,total):
            t.append(int(to[2]))
            m.append(int(me[2]))

        for i in range(len(und)-len(m)):
            t.append(0)
            m.append(0)

        mensal = [m]
        total = [t]
        
        for ref in Ref:

            valor = []
            x=0
            for uc in und:
                RefAn = self.ReferenciaAnterior(ref)
                try:
                    SaldoFinalAn = int(self.SaldoFinalCli(RefAn,cli))#GJ48
                except:
                    SaldoFinalAn = 0
                try:
                    SaldoFinal = int(self.SaldoFinalCli(ref,cli))#GJ49
                except:
                    SaldoFinal = 0
                try:
                    injetada = int(self.InjetadaInd(uc,cli, ref))#BF49
                except:
                    injetada = 0
                try:
                    injetadatotal = int(self.InjecaoTotal(ref,cli))#SOMA INJ
                except:
                    injetadatotal = 0

                if SaldoFinal > SaldoFinalAn:

                    arm = int((SaldoFinal-SaldoFinalAn)*(injetada/injetadatotal))
                    valor.append(arm)
                    
                else:
                    try:
                        totalAnt = total[-1]
                    except:
                        totalAnt = total
                    try:
                        arm = int((SaldoFinal-SaldoFinalAn)*(totalAnt[x]/sum(total[-1])))
                    except:
                        arm = 0
                    valor.append(arm)
                #print(uc,'---',arm)
                x+=1
            

            mensal.append(valor)

            repo = []
            for v,t in zip(mensal[-1],total[-1]):
                repo.append(int(v)+int(t))
            total.append(repo)
        
        repo = []
        for r,p in zip(Ref[::-1],total[::-1]):
            v=[]
            v.append(r)
            for valor in p:
                v.append(valor)
            repo.append(v)
        total = repo

        repo = []
        for r,p in zip(Ref[::-1],mensal[::-1]):
            v=[]
            v.append(r)
            for valor in p:
                v.append(valor)
            repo.append(v)
        mensal = repo

        for valor in mensal:
            for uc,v in zip(und,valor[1:]):
                self.inserirAmarzenadoM(uc,valor[0],v,1,dist,cli)
        
        for valor in total:
            for uc,v in zip(und,valor[1:]):
                self.inserirAmarzenadoT(uc,valor[0],v,1,dist,cli)
        

        return mensal,total

    def ArmMensal(self,referencia,uc,cli,dist):

        query = f'SELECT valor FROM relatorios_ArmazenamentoMensal a WHERE Referencia= {referencia}'
        query += f' AND uc= {uc}'
        query += f' AND cliente_id= {cli}'
        query += f' AND distribuidora_id= {dist}'

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()[0][0]

        return resultado

    def ArmMensalTodos(self,dist,referencia=None):

        query = f'SELECT uc,Referencia,valor FROM relatorios_ArmazenamentoMensal '
        query += f' WHERE distribuidora_id= {dist}'

        if referencia != None: 
            query += f' AND referencia= {referencia}'

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        return resultado

    def ArmTotalTodos(self,dist, referencia=None):

        query = f'SELECT uc,Referencia,valor FROM relatorios_armazenamentototal '
        query += f' WHERE distribuidora_id= {dist}'

        if referencia != None: 
            query += f' AND referencia= {referencia}'

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        return resultado

    def ArmTotal(self,referencia,uc,cli,dist):

        query = f'SELECT valor FROM relatorios_armazenamentototal a WHERE Referencia= {referencia}'
        query += f' AND uc= {uc}'
        query += f' AND cliente_id= {cli}'
        query += f' AND distribuidora_id= {dist}'

        cursor = connection.cursor()
        cursor.execute(query)

        try:
            resultado = cursor.fetchall()[0][0]
        except:
            resultado = 0

        return resultado

    def ArmTotalucs(self,referencia):

        query = f'SELECT SUM(valor) FROM relatorios_armazenamentototal a WHERE Referencia= {referencia}'

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()[0][0]

        return resultado

    def SaldoFinalCliInd(self,referencia):

        query = f'SELECT Saldo_Final FROM relatorios_azul a WHERE Referencia= {referencia}'

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        return resultado

    def SaldoFinalCli(self,referencia,cli):

        query = f'SELECT SUM(Saldo_Final) FROM relatorios_azul a WHERE Referencia= {referencia}'
        query += f' AND cliente_id= {cli}'
        query += f' AND status= 1'

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()[0][0]

        return resultado

    def CredCompensado(self,referencia,cli):
        query = f'SELECT SUM(qtdmptte) FROM relatorios_consumidor WHERE referencia= {referencia}'
        query += f' AND cliente_id= {cli}'

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()[0][0]

        return resultado

    def splitConsumo(self,referencia,uc,cli,dist):
        
        RefAnt = self.ReferenciaAnterior(referencia)

        total = self.ArmTotalTodos(dist,RefAnt)
        
        l = []
        for i in total:
            v = self.TrasformaemvalorUnit(i[2])
            l.append(v)

        armtot = sum(l)
        tot= self.ArmTotal(RefAnt,uc,cli,dist)
        tot = self.TrasformaemvalorUnit(tot)
        arm = tot

        armTotal = armtot
        armTotal = self.TrasformaemvalorUnit(armTotal)
        
    
        credComp = self.CredCompensado(referencia,cli)#GO49
        credComp = self.TrasformaemvalorUnit(credComp)


        try:
            injetada = self.valorGerador(referencia,cli, uc)['injetada']#BF49
            injetada = self.TrasformaemvalorUnit(injetada)

        except:
            injetada=0

        injTotal = self.InjecaoTotal(referencia,cli)#BF49:BV49
        injTotal = self.TrasformaemvalorUnit(injTotal)

        #print('credComp--->', credComp)
        #print('injetada--->', injetada)
        #print('injTotal--->', injTotal)
        #print('--', )

        
        split = credComp*(injetada/injTotal) 
        if credComp > injTotal:

            adicional = ((credComp-injTotal)*(arm/armTotal))
            split = split+adicional

        return split
    
    def SomaSplit(self,referencia,cli,total,dist):
        
        lista = []
        unds = self.ucs(cli)
        for i in unds:
            lista.append(self.splitConsumo(referencia,i,cli,dist))
        
        return sum(lista)

    def CreditoBruto(self,referencia):
        query = f'SELECT SUM(valormptte+valormpttusd) FROM relatorios_consumidor a WHERE Referencia= {referencia}'

        cursor = connection.cursor()
        cursor.execute(query)
        resultado = cursor.fetchall()[0][0]
        return resultado
    # 141335.77
    # 2856
    #-15%
    
    def consumoTotal(self, ref=None):
        
        query = f'SELECT referencia,SUM(qtdconsumo-qtdmptte) FROM relatorios_consumidor'

        if ref != None: 
            query += f' WHERE Referencia= {ref}'

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        return resultado

    def consumoTotalMaior(self, ref=None):
        
        query = f'SELECT referencia,qtdconsumo-qtdmptte FROM relatorios_consumidor'

        if ref != None: 
            query += f' WHERE Referencia= {ref}'

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        return resultado

    def TotalConsumo(self, ref=None):
        
        query = f'SELECT referencia,sum(qtdconsumo) FROM relatorios_consumidor'

        if ref != None: 
            query += f' WHERE Referencia= {ref}'

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        return resultado

    def CountConsumo(self, ref):
        query = f'SELECT COUNT(qtdconsumo-qtdmptte) FROM relatorios_consumidor WHERE qtdconsumo-qtdmptte > 500 '
        query += f' AND referencia= {ref}'

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        return resultado
    
    def ContaConsumo(self, uc):
        query = f'SELECT qtdconsumo FROM `relatorios_consumidor` WHERE uc="{uc}" '
        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        return resultado
        
    def CountConsumoMenor(self,ref):
        query = f'SELECT COUNT(`qtdconsumo`) FROM `relatorios_consumidor` WHERE `qtdconsumo` <200 AND referencia="{ref}" AND status=1'
        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        return resultado

    def TrataCentavos(self,valor):
        try:
            valor = str(valor).split('.')    
            valor1= valor[0]
            valor2 = valor[1]

            if len(valor1) > 2 and len(valor2) < 2:
                valor2 = valor2+'0'

            return valor1+valor2
        except:
            return valor[0]

    def trataValorInd(self,valor):

        valor = str(valor).replace('.','')

        if len(valor) == 4:
            valor = valor[0:2]+','+valor[2:4]
            return valor
        
        if len(valor) == 5:
            valor = valor[0:3]+','+valor[3:5]
            return valor
        
        if len(valor) == 6:
            valor = valor[0:1]+'.'+valor[1:4]+','+valor[4:6]
            return valor
        
        if len(valor) == 7:
            valor = valor[0:2]+'.'+valor[2:5]+','+valor[5:7]
            return valor

        if len(valor) > 7:
            valor = valor[0:3]+'.'+valor[3:6]+','+valor[6:8]
            return valor
        
    def TrataDic(self,dic):

        if 'valorBruto' in dic:
            valor = self.TrataCentavos(dic['valorBruto'])
            dic['valorBruto'] = self.trataValorInd(valor)
            
        if 'faturaGerador' in dic:
            dic['faturaGerador'] = self.trataValorInd(dic['faturaGerador'])
        
        if 'fatura' in dic:
            dic['fatura'] = self.trataValorInd(dic['fatura'])

        if 'descontoCliente' in dic:
            dic['descontoCliente'] = self.trataValorInd(dic['descontoCliente'])

        if 'descontoGestao' in dic:
            dic['descontoGestao'] = self.trataValorInd(dic['descontoGestao'])

        if 'descontoImposto' in dic:
            dic['descontoImposto'] = self.trataValorInd(dic['descontoImposto'])
                
        if 'ValorFinal' in dic:
            dic['ValorFinal'] = self.trataValorInd(dic['ValorFinal']) 

        
        return dic

    def SelectDist(self,cli):
        query = f'SELECT * FROM Distribuidoras_distribuidoras WHERE cliente_id = {cli}'
        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        return resultado

    def ValorFatura(self,valorFat, valorGest):
        #print(valorFat)
        #print(valorGest)

        if len(str(valorFat)) < 7:
            valorFat = str(valorFat).replace('.','')
        elif len(str(valorFat)) >= 7:
            pass

        if len(str(valorGest)) >= 7:
            valorGest = str(valorGest).replace('.','')
            valorGest = valorGest.replace(',','')
            valorGest = valorGest[(len(valorGest)-len(valorFat))-1:]

        #print(int(valorGest)-int(valorFat))

    def Tratamento(self,valorB,valor):

        bruto = len(str(valorB).split('.')[0])
        if int(bruto) <= 3:
            valor = str(valor).split('.')[0]
            valor1 = valor[:bruto]
            resto = valor[-2:]
            resultado = valor1+'.'+resto
            
            resultado = self.TrasformaemvalorUnit(resultado)
            return round(resultado,2)
            
        else:
            resultado = self.trataValorInd(valor)

            return resultado
    
    def insere_mensal_anteriorCopel(self,cli,dist):

        mensal = [['072019','0','103710124'],
                ['082019','0','103710124'],
                ['092019','0','103710124'],
                ['102019','0','103710124'],
                ['112019','0','103710124'],
                ['122019','2283','103710124'],
                ['012020','-1245','103710124'],
                ['022020','-1038','103710124'],
                ['032020','613','103710124'],
                ['042020','875','103710124'],
                ['052020','-176','103710124'],
                ['062020','2853','103710124'],
                ['072020','7979','103710124'],
                ['082020','3607','103710124'],
                ['092020','-5074','103710124'],
                ['102020','-2660','103710124'],
                ['112020','-4296','103710124'],
                ['122020','1187','103710124'],
                ['012021','1344','103710124'],
                ['022021','-2027','103710124'],
                ['032021','-1143','103710124'],
                ['042021','110','103710124'],
                ['052021','13032','103710124'],
                ['062021','12329','103710124'],
                ['072021','11218','103710124'],
                ['082021','-567','103710124'],
                ['092021','0','103710124'],
                ['102021','-9721','103710124'],
                ['112021','-127','103710124'],
                ['122021','-13535','103710124'],
                ['012022','-3459','103710124'],
                ['022022','-3001','103710124'],
                ['032022','618','103710124'],
                ['042022','-207','103710124'],
                ['052022','-4201','103710124'],
                ['062022','6788','103710124'],
                ['072022','7934','103710124'],
                ['082022','1922','103710124'],
                ['092022','-1837','103710124'],
                ['102022','7755','103710124'],
                ['112022','6490','103710124'],
                ['122022','-792','103710124'],
                ['012023','2492','103710124'],
                ['022023','-608','103710124'],
                ['032023','-1636','103710124'],
                ['042023','973','103710124'],
                ['052023','-35052','103710124'],
                ['072019','0','9198750'],
                ['082019','0','9198750'],
                ['092019','0','9198750'],
                ['102019','0','9198750'],
                ['112019','0','9198750'],
                ['122019','0','9198750'],
                ['012020','0','9198750'],
                ['022020','0','9198750'],
                ['032020','0','9198750'],
                ['042020','0','9198750'],
                ['052020','0','9198750'],
                ['062020','0','9198750'],
                ['072020','0','9198750'],
                ['082020','0','9198750'],
                ['092020','0','9198750'],
                ['102020','0','9198750'],
                ['112020','0','9198750'],
                ['122020','0','9198750'],
                ['012021','0','9198750'],
                ['022021','0','9198750'],
                ['032021','0','9198750'],
                ['042021','0','9198750'],
                ['052021','391','9198750'],
                ['062021','434','9198750'],
                ['072021','477','9198750'],
                ['082021','-19','9198750'],
                ['092021','3035','9198750'],
                ['102021','-1071','9198750'],
                ['112021','-14','9198750'],
                ['122021','-1491','9198750'],
                ['012022','-381','9198750'],
                ['022022','-331','9198750'],
                ['032022','0','9198750'],
                ['042022','-21','9198750'],
                ['052022','-434','9198750'],
                ['062022','4055','9198750'],
                ['072022','1732','9198750'],
                ['082022','452','9198750'],
                ['092022','-563','9198750'],
                ['102022','0','9198750'],
                ['112022','1474','9198750'],
                ['122022','-177','9198750'],
                ['012023','0','9198750'],
                ['022023','-126','9198750'],
                ['032023','-340','9198750'],
                ['042023','0','9198750'],
                ['052023','-7082','9198750'],
                ['072019','0','11151617'],
                ['082019','0','11151617'],
                ['092019','0','11151617'],
                ['102019','0','11151617'],
                ['112019','0','11151617'],
                ['122019','0','11151617'],
                ['012020','0','11151617'],
                ['022020','0','11151617'],
                ['032020','0','11151617'],
                ['042020','182','11151617'],
                ['052020','-21','11151617'],
                ['062020','562','11151617'],
                ['072020','2551','11151617'],
                ['082020','1083','11151617'],
                ['092020','-1403','11151617'],
                ['102020','-736','11151617'],
                ['112020','-1188','11151617'],
                ['122020','634','11151617'],
                ['012021','593','11151617'],
                ['022021','-731','11151617'],
                ['032021','-412','11151617'],
                ['042021','85','11151617'],
                ['052021','6969','11151617'],
                ['062021','4573','11151617'],
                ['072021','7787','11151617'],
                ['082021','-293','11151617'],
                ['092021','545','11151617'],
                ['102021','-5152','11151617'],
                ['112021','-67','11151617'],
                ['122021','-7174','11151617'],
                ['012022','-1833','11151617'],
                ['022022','-1591','11151617'],
                ['032022','509','11151617'],
                ['042022','-114','11151617'],
                ['052022','-2303','11151617'],
                ['062022','3388','11151617'],
                ['072022','2537','11151617'],
                ['082022','460','11151617'],
                ['092022','-780','11151617'],
                ['102022','1482','11151617'],
                ['112022','626','11151617'],
                ['122022','-246','11151617'],
                ['012023','934','11151617'],
                ['022023','-192','11151617'],
                ['032023','-516','11151617'],
                ['042023','281','11151617'],
                ['052023','-11027','11151617'],
                ['072019','0','96070900'],
                ['082019','0','96070900'],
                ['092019','0','96070900'],
                ['102019','0','96070900'],
                ['112019','0','96070900'],
                ['122019','0','96070900'],
                ['012020','0','96070900'],
                ['022020','0','96070900'],
                ['032020','0','96070900'],
                ['042020','0','96070900'],
                ['052020','0','96070900'],
                ['062020','1523','96070900'],
                ['072020','3283','96070900'],
                ['082020','1703','96070900'],
                ['092020','-2096','96070900'],
                ['102020','-1099','96070900'],
                ['112020','-1775','96070900'],
                ['122020','883','96070900'],
                ['012021','769','96070900'],
                ['022021','-1034','96070900'],
                ['032021','-583','96070900'],
                ['042021','135','96070900'],
                ['052021','9827','96070900'],
                ['062021','8949','96070900'],
                ['072021','10352','96070900'],
                ['082021','-440','96070900'],
                ['092021','1896','96070900'],
                ['102021','-8007','96070900'],
                ['112021','-105','96070900'],
                ['122021','-11148','96070900'],
                ['012022','-2849','96070900'],
                ['022022','-2472','96070900'],
                ['032022','192','96070900'],
                ['042022','-164','96070900'],
                ['052022','-3327','96070900'],
                ['062022','10974','96070900'],
                ['072022','5686','96070900'],
                ['082022','396','96070900'],
                ['092022','-1775','96070900'],
                ['102022','3565','96070900'],
                ['112022','5390','96070900'],
                ['122022','-656','96070900'],
                ['012023','2389','96070900'],
                ['022023','-509','96070900'],
                ['032023','-1368','96070900'],
                ['042023','940','96070900'],
                ['052023','-29444','96070900'],
                ['072019','0','9057617'],
                ['082019','0','9057617'],
                ['092019','0','9057617'],
                ['102019','0','9057617'],
                ['112019','0','9057617'],
                ['122019','0','9057617'],
                ['012020','0','9057617'],
                ['022020','0','9057617'],
                ['032020','0','9057617'],
                ['042020','0','9057617'],
                ['052020','0','9057617'],
                ['062020','1047','9057617'],
                ['072020','3303','9057617'],
                ['082020','1433','9057617'],
                ['092020','-1863','9057617'],
                ['102020','-977','9057617'],
                ['112020','-1577','9057617'],
                ['122020','537','9057617'],
                ['012021','758','9057617'],
                ['022021','-863','9057617'],
                ['032021','-487','9057617'],
                ['042021','82','9057617'],
                ['052021','4758','9057617'],
                ['062021','5862','9057617'],
                ['072021','6205','9057617'],
                ['082021','-260','9057617'],
                ['092021','442','9057617'],
                ['102021','-4563','9057617'],
                ['112021','-60','9057617'],
                ['122021','-6353','9057617'],
                ['012022','-1623','9057617'],
                ['022022','-1409','9057617'],
                ['032022','4','9057617'],
                ['042022','-91','9057617'],
                ['052022','-1852','9057617'],
                ['062022','3335','9057617'],
                ['072022','1872','9057617'],
                ['082022','412','9057617'],
                ['092022','-668','9057617'],
                ['102022','1850','9057617'],
                ['112022','3593','9057617'],
                ['122022','-294','9057617'],
                ['012023','934','9057617'],
                ['022023','-226','9057617'],
                ['032023','-608','9057617'],
                ['042023','1165','9057617'],
                ['052023','-13823','9057617'],
                ['072019','0','9791329'],
                ['082019','0','9791329'],
                ['092019','0','9791329'],
                ['102019','0','9791329'],
                ['112019','0','9791329'],
                ['122019','0','9791329'],
                ['012020','0','9791329'],
                ['022020','0','9791329'],
                ['032020','0','9791329'],
                ['042020','0','9791329'],
                ['052020','0','9791329'],
                ['062020','641','9791329'],
                ['072020','1784','9791329'],
                ['082020','829','9791329'],
                ['092020','-1048','9791329'],
                ['102020','-550','9791329'],
                ['112020','-888','9791329'],
                ['122020','325','9791329'],
                ['012021','846','9791329'],
                ['022021','-629','9791329'],
                ['032021','-355','9791329'],
                ['042021','69','9791329'],
                ['052021','3634','9791329'],
                ['062021','4242','9791329'],
                ['072021','4386','9791329'],
                ['082021','-190','9791329'],
                ['092021','565','9791329'],
                ['102021','-3388','9791329'],
                ['112021','-44','9791329'],
                ['122021','-4717','9791329'],
                ['012022','-1205','9791329'],
                ['022022','-1046','9791329'],
                ['032022','408','9791329'],
                ['042022','-76','9791329'],
                ['052022','-1545','9791329'],
                ['062022','4251','9791329'],
                ['072022','717','9791329'],
                ['082022','292','9791329'],
                ['092022','-604','9791329'],
                ['102022','4116','9791329'],
                ['112022','3957','9791329'],
                ['122022','-338','9791329'],
                ['012023','866','9791329'],
                ['022023','-256','9791329'],
                ['032023','-689','9791329'],
                ['042023','392','9791329'],
                ['052023','-14753','9791329'],
                ['072019','0','11677058'],
                ['082019','0','11677058'],
                ['092019','0','11677058'],
                ['102019','0','11677058'],
                ['112019','0','11677058'],
                ['122019','0','11677058'],
                ['012020','0','11677058'],
                ['022020','0','11677058'],
                ['032020','0','11677058'],
                ['042020','0','11677058'],
                ['052020','0','11677058'],
                ['062020','0','11677058'],
                ['072020','0','11677058'],
                ['082020','0','11677058'],
                ['092020','0','11677058'],
                ['102020','0','11677058'],
                ['112020','0','11677058'],
                ['122020','0','11677058'],
                ['012021','0','11677058'],
                ['022021','0','11677058'],
                ['032021','0','11677058'],
                ['042021','0','11677058'],
                ['052021','0','11677058'],
                ['062021','0','11677058'],
                ['072021','0','11677058'],
                ['082021','0','11677058'],
                ['092021','0','11677058'],
                ['102021','0','11677058'],
                ['112021','0','11677058'],
                ['122021','0','11677058'],
                ['012022','0','11677058'],
                ['022022','0','11677058'],
                ['032022','0','11677058'],
                ['042022','0','11677058'],
                ['052022','0','11677058'],
                ['062022','0','11677058'],
                ['072022','0','11677058'],
                ['082022','0','11677058'],
                ['092022','0','11677058'],
                ['102022','4042','11677058'],
                ['112022','3330','11677058'],
                ['122022','-169','11677058'],
                ['012023','763','11677058'],
                ['022023','-133','11677058'],
                ['032023','-359','11677058'],
                ['042023','281','11677058'],
                ['052023','-7756','11677058'],
                ['072019','0','99884771'],
                ['082019','0','99884771'],
                ['092019','0','99884771'],
                ['102019','0','99884771'],
                ['112019','0','99884771'],
                ['122019','0','99884771'],
                ['012020','0','99884771'],
                ['022020','0','99884771'],
                ['032020','0','99884771'],
                ['042020','0','99884771'],
                ['052020','0','99884771'],
                ['062020','0','99884771'],
                ['072020','0','99884771'],
                ['082020','0','99884771'],
                ['092020','0','99884771'],
                ['102020','0','99884771'],
                ['112020','0','99884771'],
                ['122020','402','99884771'],
                ['012021','716','99884771'],
                ['022021','-362','99884771'],
                ['032021','-204','99884771'],
                ['042021','87','99884771'],
                ['052021','4013','99884771'],
                ['062021','5033','99884771'],
                ['072021','5803','99884771'],
                ['082021','-221','99884771'],
                ['092021','663','99884771'],
                ['102021','-3949','99884771'],
                ['112021','-52','99884771'],
                ['122021','-5499','99884771'],
                ['012022','-1405','99884771'],
                ['022022','-1219','99884771'],
                ['032022','446','99884771'],
                ['042022','-88','99884771'],
                ['052022','-1789','99884771'],
                ['062022','4002','99884771'],
                ['072022','2904','99884771'],
                ['082022','1048','99884771'],
                ['092022','-854','99884771'],
                ['102022','1311','99884771'],
                ['112022','1776','99884771'],
                ['122022','-287','99884771'],
                ['012023','871','99884771'],
                ['022023','-220','99884771'],
                ['032023','-592','99884771'],
                ['042023','275','99884771'],
                ['052023','-12607','99884771'],
                ['072019','0','80299296'],
                ['082019','0','80299296'],
                ['092019','0','80299296'],
                ['102019','0','80299296'],
                ['112019','0','80299296'],
                ['122019','0','80299296'],
                ['012020','0','80299296'],
                ['022020','0','80299296'],
                ['032020','0','80299296'],
                ['042020','0','80299296'],
                ['052020','0','80299296'],
                ['062020','0','80299296'],
                ['072020','0','80299296'],
                ['082020','0','80299296'],
                ['092020','0','80299296'],
                ['102020','0','80299296'],
                ['112020','0','80299296'],
                ['122020','0','80299296'],
                ['012021','0','80299296'],
                ['022021','0','80299296'],
                ['032021','0','80299296'],
                ['042021','0','80299296'],
                ['052021','0','80299296'],
                ['062021','0','80299296'],
                ['072021','1238','80299296'],
                ['082021','-18','80299296'],
                ['092021','0','80299296'],
                ['102021','-303','80299296'],
                ['112021','-4','80299296'],
                ['122021','-421','80299296'],
                ['012022','-108','80299296'],
                ['022022','-93','80299296'],
                ['032022','428','80299296'],
                ['042022','-15','80299296'],
                ['052022','-303','80299296'],
                ['062022','4002','80299296'],
                ['072022','1907','80299296'],
                ['082022','1138','80299296'],
                ['092022','-616','80299296'],
                ['102022','1139','80299296'],
                ['112022','1223','80299296'],
                ['122022','-210','80299296'],
                ['012023','0','80299296'],
                ['022023','-150','80299296'],
                ['032023','-405','80299296'],
                ['042023','284','80299296'],
                ['052023','-8714','80299296'],
                ['072019','0','9790799'],
                ['082019','0','9790799'],
                ['092019','0','9790799'],
                ['102019','0','9790799'],
                ['112019','0','9790799'],
                ['122019','0','9790799'],
                ['012020','0','9790799'],
                ['022020','0','9790799'],
                ['032020','0','9790799'],
                ['042020','0','9790799'],
                ['052020','0','9790799'],
                ['062020','0','9790799'],
                ['072020','0','9790799'],
                ['082020','0','9790799'],
                ['092020','0','9790799'],
                ['102020','0','9790799'],
                ['112020','0','9790799'],
                ['122020','0','9790799'],
                ['012021','0','9790799'],
                ['022021','0','9790799'],
                ['032021','0','9790799'],
                ['042021','0','9790799'],
                ['052021','0','9790799'],
                ['062021','0','9790799'],
                ['072021','0','9790799'],
                ['082021','0','9790799'],
                ['092021','0','9790799'],
                ['102021','0','9790799'],
                ['112021','0','9790799'],
                ['122021','0','9790799'],
                ['012022','0','9790799'],
                ['022022','0','9790799'],
                ['032022','0','9790799'],
                ['042022','0','9790799'],
                ['052022','0','9790799'],
                ['062022','0','9790799'],
                ['072022','0','9790799'],
                ['082022','0','9790799'],
                ['092022','0','9790799'],
                ['102022','815','9790799'],
                ['112022','1574','9790799'],
                ['122022','-55','9790799'],
                ['012023','1799','9790799'],
                ['022023','-69','9790799'],
                ['032023','-186','9790799'],
                ['042023','355','9790799'],
                ['052023','-4234','9790799'],
                ['072019','0','108983536'],
                ['082019','0','108983536'],
                ['092019','0','108983536'],
                ['102019','0','108983536'],
                ['112019','0','108983536'],
                ['122019','0','108983536'],
                ['012020','0','108983536'],
                ['022020','0','108983536'],
                ['032020','0','108983536'],
                ['042020','0','108983536'],
                ['052020','0','108983536'],
                ['062020','0','108983536'],
                ['072020','0','108983536'],
                ['082020','0','108983536'],
                ['092020','0','108983536'],
                ['102020','0','108983536'],
                ['112020','0','108983536'],
                ['122020','0','108983536'],
                ['012021','0','108983536'],
                ['022021','0','108983536'],
                ['032021','0','108983536'],
                ['042021','0','108983536'],
                ['052021','0','108983536'],
                ['062021','0','108983536'],
                ['072021','0','108983536'],
                ['082021','0','108983536'],
                ['092021','0','108983536'],
                ['102021','0','108983536'],
                ['112021','0','108983536'],
                ['122021','0','108983536'],
                ['012022','0','108983536'],
                ['022022','0','108983536'],
                ['032022','0','108983536'],
                ['042022','0','108983536'],
                ['052022','0','108983536'],
                ['062022','3803','108983536'],
                ['072022','2835','108983536'],
                ['082022','918','108983536'],
                ['092022','-625','108983536'],
                ['102022','3756','108983536'],
                ['112022','3088','108983536'],
                ['122022','-315','108983536'],
                ['012023','1494','108983536'],
                ['022023','-250','108983536'],
                ['032023','-674','108983536'],
                ['042023','553','108983536'],
                ['052023','-14585','108983536'],
                ['072019','0','106473085'],
                ['082019','0','106473085'],
                ['092019','0','106473085'],
                ['102019','0','106473085'],
                ['112019','0','106473085'],
                ['122019','0','106473085'],
                ['012020','0','106473085'],
                ['022020','0','106473085'],
                ['032020','0','106473085'],
                ['042020','0','106473085'],
                ['052020','0','106473085'],
                ['062020','0','106473085'],
                ['072020','0','106473085'],
                ['082020','0','106473085'],
                ['092020','0','106473085'],
                ['102020','0','106473085'],
                ['112020','0','106473085'],
                ['122020','0','106473085'],
                ['012021','0','106473085'],
                ['022021','0','106473085'],
                ['032021','0','106473085'],
                ['042021','0','106473085'],
                ['052021','0','106473085'],
                ['062021','0','106473085'],
                ['072021','0','106473085'],
                ['082021','0','106473085'],
                ['092021','0','106473085'],
                ['102021','0','106473085'],
                ['112021','0','106473085'],
                ['122021','0','106473085'],
                ['012022','0','106473085'],
                ['022022','0','106473085'],
                ['032022','0','106473085'],
                ['042022','0','106473085'],
                ['052022','0','106473085'],
                ['062022','0','106473085'],
                ['072022','0','106473085'],
                ['082022','0','106473085'],
                ['092022','0','106473085'],
                ['102022','2181','106473085'],
                ['112022','3311','106473085'],
                ['122022','-126','106473085'],
                ['012023','3406','106473085'],
                ['022023','-147','106473085'],
                ['032023','-395','106473085'],
                ['042023','0','106473085'],
                ['052023','-8230','106473085'],
                ['072019','0','108570010'],
                ['082019','0','108570010'],
                ['092019','0','108570010'],
                ['102019','0','108570010'],
                ['112019','0','108570010'],
                ['122019','0','108570010'],
                ['012020','0','108570010'],
                ['022020','0','108570010'],
                ['032020','0','108570010'],
                ['042020','0','108570010'],
                ['052020','0','108570010'],
                ['062020','0','108570010'],
                ['072020','0','108570010'],
                ['082020','0','108570010'],
                ['092020','0','108570010'],
                ['102020','0','108570010'],
                ['112020','0','108570010'],
                ['122020','0','108570010'],
                ['012021','0','108570010'],
                ['022021','0','108570010'],
                ['032021','0','108570010'],
                ['042021','0','108570010'],
                ['052021','0','108570010'],
                ['062021','0','108570010'],
                ['072021','0','108570010'],
                ['082021','0','108570010'],
                ['092021','0','108570010'],
                ['102021','0','108570010'],
                ['112021','0','108570010'],
                ['122021','0','108570010'],
                ['012022','0','108570010'],
                ['022022','0','108570010'],
                ['032022','0','108570010'],
                ['042022','0','108570010'],
                ['052022','0','108570010'],
                ['062022','0','108570010'],
                ['072022','0','108570010'],
                ['082022','0','108570010'],
                ['092022','0','108570010'],
                ['102022','14581','108570010'],
                ['112022','10930','108570010'],
                ['122022','-584','108570010'],
                ['012023','5803','108570010'],
                ['022023','-515','108570010'],
                ['032023','-1384','108570010'],
                ['042023','2024','108570010'],
                ['052023','-30856','108570010'],
                ['072019','0','109869079'],
                ['082019','0','109869079'],
                ['092019','0','109869079'],
                ['102019','0','109869079'],
                ['112019','0','109869079'],
                ['122019','0','109869079'],
                ['012020','0','109869079'],
                ['022020','0','109869079'],
                ['032020','0','109869079'],
                ['042020','0','109869079'],
                ['052020','0','109869079'],
                ['062020','0','109869079'],
                ['072020','0','109869079'],
                ['082020','0','109869079'],
                ['092020','0','109869079'],
                ['102020','0','109869079'],
                ['112020','0','109869079'],
                ['122020','0','109869079'],
                ['012021','0','109869079'],
                ['022021','0','109869079'],
                ['032021','0','109869079'],
                ['042021','0','109869079'],
                ['052021','0','109869079'],
                ['062021','0','109869079'],
                ['072021','0','109869079'],
                ['082021','0','109869079'],
                ['092021','0','109869079'],
                ['102021','0','109869079'],
                ['112021','0','109869079'],
                ['122021','0','109869079'],
                ['012022','0','109869079'],
                ['022022','0','109869079'],
                ['032022','0','109869079'],
                ['042022','0','109869079'],
                ['052022','0','109869079'],
                ['062022','0','109869079'],
                ['072022','0','109869079'],
                ['082022','0','109869079'],
                ['092022','0','109869079'],
                ['102022','0','109869079'],
                ['112022','0','109869079'],
                ['122022','0','109869079'],
                ['012023','1995','109869079'],
                ['022023','-33','109869079'],
                ['032023','-90','109869079'],
                ['042023','451','109869079'],
                ['052023','-2323','109869079'],
                ['072019','0','109869630'],
                ['082019','0','109869630'],
                ['092019','0','109869630'],
                ['102019','0','109869630'],
                ['112019','0','109869630'],
                ['122019','0','109869630'],
                ['012020','0','109869630'],
                ['022020','0','109869630'],
                ['032020','0','109869630'],
                ['042020','0','109869630'],
                ['052020','0','109869630'],
                ['062020','0','109869630'],
                ['072020','0','109869630'],
                ['082020','0','109869630'],
                ['092020','0','109869630'],
                ['102020','0','109869630'],
                ['112020','0','109869630'],
                ['122020','0','109869630'],
                ['012021','0','109869630'],
                ['022021','0','109869630'],
                ['032021','0','109869630'],
                ['042021','0','109869630'],
                ['052021','0','109869630'],
                ['062021','0','109869630'],
                ['072021','0','109869630'],
                ['082021','0','109869630'],
                ['092021','0','109869630'],
                ['102021','0','109869630'],
                ['112021','0','109869630'],
                ['122021','0','109869630'],
                ['012022','0','109869630'],
                ['022022','0','109869630'],
                ['032022','0','109869630'],
                ['042022','0','109869630'],
                ['052022','0','109869630'],
                ['062022','0','109869630'],
                ['072022','0','109869630'],
                ['082022','0','109869630'],
                ['092022','0','109869630'],
                ['102022','0','109869630'],
                ['112022','0','109869630'],
                ['122022','0','109869630'],
                ['012023','4458','109869630'],
                ['022023','-75','109869630'],
                ['032023','-201','109869630'],
                ['042023','462','109869630'],
                ['052023','-4645','109869630'],
                ['072019','0','109876830'],
                ['082019','0','109876830'],
                ['092019','0','109876830'],
                ['102019','0','109876830'],
                ['112019','0','109876830'],
                ['122019','0','109876830'],
                ['012020','0','109876830'],
                ['022020','0','109876830'],
                ['032020','0','109876830'],
                ['042020','0','109876830'],
                ['052020','0','109876830'],
                ['062020','0','109876830'],
                ['072020','0','109876830'],
                ['082020','0','109876830'],
                ['092020','0','109876830'],
                ['102020','0','109876830'],
                ['112020','0','109876830'],
                ['122020','0','109876830'],
                ['012021','0','109876830'],
                ['022021','0','109876830'],
                ['032021','0','109876830'],
                ['042021','0','109876830'],
                ['052021','0','109876830'],
                ['062021','0','109876830'],
                ['072021','0','109876830'],
                ['082021','0','109876830'],
                ['092021','0','109876830'],
                ['102021','0','109876830'],
                ['112021','0','109876830'],
                ['122021','0','109876830'],
                ['012022','0','109876830'],
                ['022022','0','109876830'],
                ['032022','0','109876830'],
                ['042022','0','109876830'],
                ['052022','0','109876830'],
                ['062022','0','109876830'],
                ['072022','0','109876830'],
                ['082022','0','109876830'],
                ['092022','0','109876830'],
                ['102022','0','109876830'],
                ['112022','0','109876830'],
                ['122022','0','109876830'],
                ['012023','0','109876830'],
                ['022023','0','109876830'],
                ['032023','0','109876830'],
                ['042023','534','109876830'],
                ['052023','-534','109876830'],
                ['072019','0','109852621'],
                ['082019','0','109852621'],
                ['092019','0','109852621'],
                ['102019','0','109852621'],
                ['112019','0','109852621'],
                ['122019','0','109852621'],
                ['012020','0','109852621'],
                ['022020','0','109852621'],
                ['032020','0','109852621'],
                ['042020','0','109852621'],
                ['052020','0','109852621'],
                ['062020','0','109852621'],
                ['072020','0','109852621'],
                ['082020','0','109852621'],
                ['092020','0','109852621'],
                ['102020','0','109852621'],
                ['112020','0','109852621'],
                ['122020','0','109852621'],
                ['012021','0','109852621'],
                ['022021','0','109852621'],
                ['032021','0','109852621'],
                ['042021','0','109852621'],
                ['052021','0','109852621'],
                ['062021','0','109852621'],
                ['072021','0','109852621'],
                ['082021','0','109852621'],
                ['092021','0','109852621'],
                ['102021','0','109852621'],
                ['112021','0','109852621'],
                ['122021','0','109852621'],
                ['012022','0','109852621'],
                ['022022','0','109852621'],
                ['032022','0','109852621'],
                ['042022','0','109852621'],
                ['052022','0','109852621'],
                ['062022','0','109852621'],
                ['072022','0','109852621'],
                ['082022','0','109852621'],
                ['092022','0','109852621'],
                ['102022','0','109852621'],
                ['112022','4582','109852621'],
                ['122022','-105','109852621'],
                ['012023','2175','109852621'],
                ['022023','-111','109852621'],
                ['032023','-300','109852621'],
                ['042023','650','109852621'],
                ['052023','-6892','109852621']]

        for i in mensal:
            self.inserirAmarzenadoM(i[2],i[0],i[1],1,dist,cli)

    def insere_total_anteriorCopel(self,cli,dist):
      
      total = [['072019','0','103710124'],
            ['082019','0','103710124'],
            ['092019','0','103710124'],
            ['102019','0','103710124'],
            ['112019','0','103710124'],
            ['122019','2283','103710124'],
            ['012020','1038','103710124'],
            ['022020','0','103710124'],
            ['032020','613','103710124'],
            ['042020','1488','103710124'],
            ['052020','1312','103710124'],
            ['062020','4165','103710124'],
            ['072020','12144','103710124'],
            ['082020','15751','103710124'],
            ['092020','10677','103710124'],
            ['102020','8017','103710124'],
            ['112020','3721','103710124'],
            ['122020','4908','103710124'],
            ['012021','6252','103710124'],
            ['022021','4225','103710124'],
            ['032021','3082','103710124'],
            ['042021','3193','103710124'],
            ['052021','16224','103710124'],
            ['062021','28554','103710124'],
            ['072021','39771','103710124'],
            ['082021','39204','103710124'],
            ['092021','39204','103710124'],
            ['102021','29483','103710124'],
            ['112021','29355','103710124'],
            ['122021','15821','103710124'],
            ['012022','12362','103710124'],
            ['022022','9361','103710124'],
            ['032022','9979','103710124'],
            ['042022','9772','103710124'],
            ['052022','5571','103710124'],
            ['062022','12359','103710124'],
            ['072022','20293','103710124'],
            ['082022','22216','103710124'],
            ['092022','20379','103710124'],
            ['102022','28134','103710124'],
            ['112022','34624','103710124'],
            ['122022','33832','103710124'],
            ['012023','36323','103710124'],
            ['022023','35715','103710124'],
            ['032023','34079','103710124'],
            ['042023','35052','103710124'],
            ['072019','0','9198750'],
            ['082019','0','9198750'],
            ['092019','0','9198750'],
            ['102019','0','9198750'],
            ['112019','0','9198750'],
            ['122019','0','9198750'],
            ['012020','0','9198750'],
            ['022020','0','9198750'],
            ['032020','0','9198750'],
            ['042020','0','9198750'],
            ['052020','0','9198750'],
            ['062020','0','9198750'],
            ['072020','0','9198750'],
            ['082020','0','9198750'],
            ['092020','0','9198750'],
            ['102020','0','9198750'],
            ['112020','0','9198750'],
            ['122020','0','9198750'],
            ['012021','0','9198750'],
            ['022021','0','9198750'],
            ['032021','0','9198750'],
            ['042021','0','9198750'],
            ['052021','391','9198750'],
            ['062021','825','9198750'],
            ['072021','1302','9198750'],
            ['082021','1284','9198750'],
            ['092021','4319','9198750'],
            ['102021','3248','9198750'],
            ['112021','3234','9198750'],
            ['122021','1743','9198750'],
            ['012022','1362','9198750'],
            ['022022','1031','9198750'],
            ['032022','1031','9198750'],
            ['042022','1010','9198750'],
            ['052022','576','9198750'],
            ['062022','4630','9198750'],
            ['072022','6362','9198750'],
            ['082022','6814','9198750'],
            ['092022','6251','9198750'],
            ['102022','6251','9198750'],
            ['112022','7725','9198750'],
            ['122022','7548','9198750'],
            ['012023','7548','9198750'],
            ['022023','7421','9198750'],
            ['032023','7082','9198750'],
            ['042023','7082','9198750'],
            ['072019','0','11151617'],
            ['082019','0','11151617'],
            ['092019','0','11151617'],
            ['102019','0','11151617'],
            ['112019','0','11151617'],
            ['122019','0','11151617'],
            ['012020','0','11151617'],
            ['022020','0','11151617'],
            ['032020','0','11151617'],
            ['042020','182','11151617'],
            ['052020','161','11151617'],
            ['062020','723','11151617'],
            ['072020','3274','11151617'],
            ['082020','4357','11151617'],
            ['092020','2954','11151617'],
            ['102020','2218','11151617'],
            ['112020','1029','11151617'],
            ['122020','1663','11151617'],
            ['012021','2256','11151617'],
            ['022021','1525','11151617'],
            ['032021','1112','11151617'],
            ['042021','1197','11151617'],
            ['052021','8167','11151617'],
            ['062021','12740','11151617'],
            ['072021','20527','11151617'],
            ['082021','20234','11151617'],
            ['092021','20779','11151617'],
            ['102021','15626','11151617'],
            ['112021','15559','11151617'],
            ['122021','8385','11151617'],
            ['012022','6552','11151617'],
            ['022022','4962','11151617'],
            ['032022','5471','11151617'],
            ['042022','5357','11151617'],
            ['052022','3054','11151617'],
            ['062022','6442','11151617'],
            ['072022','8979','11151617'],
            ['082022','9439','11151617'],
            ['092022','8658','11151617'],
            ['102022','10141','11151617'],
            ['112022','10767','11151617'],
            ['122022','10520','11151617'],
            ['012023','11454','11151617'],
            ['022023','11263','11151617'],
            ['032023','10747','11151617'],
            ['042023','11027','11151617'],
            ['072019','0','96070900'],
            ['082019','0','96070900'],
            ['092019','0','96070900'],
            ['102019','0','96070900'],
            ['112019','0','96070900'],
            ['122019','0','96070900'],
            ['012020','0','96070900'],
            ['022020','0','96070900'],
            ['032020','0','96070900'],
            ['042020','0','96070900'],
            ['052020','0','96070900'],
            ['062020','1523','96070900'],
            ['072020','4806','96070900'],
            ['082020','6508','96070900'],
            ['092020','4412','96070900'],
            ['102020','3313','96070900'],
            ['112020','1538','96070900'],
            ['122020','2420','96070900'],
            ['012021','3189','96070900'],
            ['022021','2155','96070900'],
            ['032021','1572','96070900'],
            ['042021','1707','96070900'],
            ['052021','11533','96070900'],
            ['062021','20482','96070900'],
            ['072021','30835','96070900'],
            ['082021','30395','96070900'],
            ['092021','32290','96070900'],
            ['102021','24283','96070900'],
            ['112021','24179','96070900'],
            ['122021','13031','96070900'],
            ['012022','10182','96070900'],
            ['022022','7710','96070900'],
            ['032022','7902','96070900'],
            ['042022','7738','96070900'],
            ['052022','4412','96070900'],
            ['062022','15385','96070900'],
            ['072022','21071','96070900'],
            ['082022','21467','96070900'],
            ['092022','19693','96070900'],
            ['102022','23258','96070900'],
            ['112022','28648','96070900'],
            ['122022','27992','96070900'],
            ['012023','30381','96070900'],
            ['022023','29873','96070900'],
            ['032023','28504','96070900'],
            ['042023','29444','96070900'],
            ['072019','0','9057617'],
            ['082019','0','9057617'],
            ['092019','0','9057617'],
            ['102019','0','9057617'],
            ['112019','0','9057617'],
            ['122019','0','9057617'],
            ['012020','0','9057617'],
            ['022020','0','9057617'],
            ['032020','0','9057617'],
            ['042020','0','9057617'],
            ['052020','0','9057617'],
            ['062020','1047','9057617'],
            ['072020','4350','9057617'],
            ['082020','5784','9057617'],
            ['092020','3921','9057617'],
            ['102020','2944','9057617'],
            ['112020','1366','9057617'],
            ['122020','1904','9057617'],
            ['012021','2661','9057617'],
            ['022021','1799','9057617'],
            ['032021','1312','9057617'],
            ['042021','1394','9057617'],
            ['052021','6152','9057617'],
            ['062021','12014','9057617'],
            ['072021','18219','9057617'],
            ['082021','17959','9057617'],
            ['092021','18401','9057617'],
            ['102021','13839','9057617'],
            ['112021','13779','9057617'],
            ['122021','7426','9057617'],
            ['012022','5803','9057617'],
            ['022022','4394','9057617'],
            ['032022','4398','9057617'],
            ['042022','4307','9057617'],
            ['052022','2455','9057617'],
            ['062022','5791','9057617'],
            ['072022','7663','9057617'],
            ['082022','8075','9057617'],
            ['092022','7407','9057617'],
            ['102022','9257','9057617'],
            ['112022','12850','9057617'],
            ['122022','12556','9057617'],
            ['012023','13491','9057617'],
            ['022023','13265','9057617'],
            ['032023','12657','9057617'],
            ['042023','13823','9057617'],
            ['072019','0','9791329'],
            ['082019','0','9791329'],
            ['092019','0','9791329'],
            ['102019','0','9791329'],
            ['112019','0','9791329'],
            ['122019','0','9791329'],
            ['012020','0','9791329'],
            ['022020','0','9791329'],
            ['032020','0','9791329'],
            ['042020','0','9791329'],
            ['052020','0','9791329'],
            ['062020','641','9791329'],
            ['072020','2425','9791329'],
            ['082020','3254','9791329'],
            ['092020','2206','9791329'],
            ['102020','1656','9791329'],
            ['112020','769','9791329'],
            ['122020','1094','9791329'],
            ['012021','1941','9791329'],
            ['022021','1311','9791329'],
            ['032021','957','9791329'],
            ['042021','1026','9791329'],
            ['052021','4660','9791329'],
            ['062021','8901','9791329'],
            ['072021','13287','9791329'],
            ['082021','13097','9791329'],
            ['092021','13662','9791329'],
            ['102021','10274','9791329'],
            ['112021','10230','9791329'],
            ['122021','5513','9791329'],
            ['012022','4308','9791329'],
            ['022022','3262','9791329'],
            ['032022','3670','9791329'],
            ['042022','3594','9791329'],
            ['052022','2049','9791329'],
            ['062022','6300','9791329'],
            ['072022','7017','9791329'],
            ['082022','7309','9791329'],
            ['092022','6705','9791329'],
            ['102022','10822','9791329'],
            ['112022','14778','9791329'],
            ['122022','14440','9791329'],
            ['012023','15306','9791329'],
            ['022023','15050','9791329'],
            ['032023','14361','9791329'],
            ['042023','14753','9791329'],
            ['072019','0','11677058'],
            ['082019','0','11677058'],
            ['092019','0','11677058'],
            ['102019','0','11677058'],
            ['112019','0','11677058'],
            ['122019','0','11677058'],
            ['012020','0','11677058'],
            ['022020','0','11677058'],
            ['032020','0','11677058'],
            ['042020','0','11677058'],
            ['052020','0','11677058'],
            ['062020','0','11677058'],
            ['072020','0','11677058'],
            ['082020','0','11677058'],
            ['092020','0','11677058'],
            ['102020','0','11677058'],
            ['112020','0','11677058'],
            ['122020','0','11677058'],
            ['012021','0','11677058'],
            ['022021','0','11677058'],
            ['032021','0','11677058'],
            ['042021','0','11677058'],
            ['052021','0','11677058'],
            ['062021','0','11677058'],
            ['072021','0','11677058'],
            ['082021','0','11677058'],
            ['092021','0','11677058'],
            ['102021','0','11677058'],
            ['112021','0','11677058'],
            ['122021','0','11677058'],
            ['012022','0','11677058'],
            ['022022','0','11677058'],
            ['032022','0','11677058'],
            ['042022','0','11677058'],
            ['052022','0','11677058'],
            ['062022','0','11677058'],
            ['072022','0','11677058'],
            ['082022','0','11677058'],
            ['092022','0','11677058'],
            ['102022','4042','11677058'],
            ['112022','7372','11677058'],
            ['122022','7203','11677058'],
            ['012023','7967','11677058'],
            ['022023','7833','11677058'],
            ['032023','7475','11677058'],
            ['042023','7756','11677058'],
            ['072019','0','99884771'],
            ['082019','0','99884771'],
            ['092019','0','99884771'],
            ['102019','0','99884771'],
            ['112019','0','99884771'],
            ['122019','0','99884771'],
            ['012020','0','99884771'],
            ['022020','0','99884771'],
            ['032020','0','99884771'],
            ['042020','0','99884771'],
            ['052020','0','99884771'],
            ['062020','0','99884771'],
            ['072020','0','99884771'],
            ['082020','0','99884771'],
            ['092020','0','99884771'],
            ['102020','0','99884771'],
            ['112020','0','99884771'],
            ['122020','402','99884771'],
            ['012021','1118','99884771'],
            ['022021','755','99884771'],
            ['032021','551','99884771'],
            ['042021','638','99884771'],
            ['052021','4650','99884771'],
            ['062021','9683','99884771'],
            ['072021','15485','99884771'],
            ['082021','15265','99884771'],
            ['092021','15927','99884771'],
            ['102021','11978','99884771'],
            ['112021','11926','99884771'],
            ['122021','6428','99884771'],
            ['012022','5022','99884771'],
            ['022022','3803','99884771'],
            ['032022','4249','99884771'],
            ['042022','4161','99884771'],
            ['052022','2372','99884771'],
            ['062022','6374','99884771'],
            ['072022','9278','99884771'],
            ['082022','10326','99884771'],
            ['092022','9472','99884771'],
            ['102022','10783','99884771'],
            ['112022','12560','99884771'],
            ['122022','12272','99884771'],
            ['012023','13143','99884771'],
            ['022023','12923','99884771'],
            ['032023','12331','99884771'],
            ['042023','12607','99884771'],
            ['072019','0','80299296'],
            ['082019','0','80299296'],
            ['092019','0','80299296'],
            ['102019','0','80299296'],
            ['112019','0','80299296'],
            ['122019','0','80299296'],
            ['012020','0','80299296'],
            ['022020','0','80299296'],
            ['032020','0','80299296'],
            ['042020','0','80299296'],
            ['052020','0','80299296'],
            ['062020','0','80299296'],
            ['072020','0','80299296'],
            ['082020','0','80299296'],
            ['092020','0','80299296'],
            ['102020','0','80299296'],
            ['112020','0','80299296'],
            ['122020','0','80299296'],
            ['012021','0','80299296'],
            ['022021','0','80299296'],
            ['032021','0','80299296'],
            ['042021','0','80299296'],
            ['052021','0','80299296'],
            ['062021','0','80299296'],
            ['072021','1238','80299296'],
            ['082021','1220','80299296'],
            ['092021','1220','80299296'],
            ['102021','918','80299296'],
            ['112021','914','80299296'],
            ['122021','493','80299296'],
            ['012022','385','80299296'],
            ['022022','291','80299296'],
            ['032022','719','80299296'],
            ['042022','704','80299296'],
            ['052022','402','80299296'],
            ['062022','4404','80299296'],
            ['072022','6311','80299296'],
            ['082022','7449','80299296'],
            ['092022','6833','80299296'],
            ['102022','7972','80299296'],
            ['112022','9196','80299296'],
            ['122022','8985','80299296'],
            ['012023','8985','80299296'],
            ['022023','8835','80299296'],
            ['032023','8430','80299296'],
            ['042023','8714','80299296'],
            ['072019','0','9790799'],
            ['082019','0','9790799'],
            ['092019','0','9790799'],
            ['102019','0','9790799'],
            ['112019','0','9790799'],
            ['122019','0','9790799'],
            ['012020','0','9790799'],
            ['022020','0','9790799'],
            ['032020','0','9790799'],
            ['042020','0','9790799'],
            ['052020','0','9790799'],
            ['062020','0','9790799'],
            ['072020','0','9790799'],
            ['082020','0','9790799'],
            ['092020','0','9790799'],
            ['102020','0','9790799'],
            ['112020','0','9790799'],
            ['122020','0','9790799'],
            ['012021','0','9790799'],
            ['022021','0','9790799'],
            ['032021','0','9790799'],
            ['042021','0','9790799'],
            ['052021','0','9790799'],
            ['062021','0','9790799'],
            ['072021','0','9790799'],
            ['082021','0','9790799'],
            ['092021','0','9790799'],
            ['102021','0','9790799'],
            ['112021','0','9790799'],
            ['122021','0','9790799'],
            ['012022','0','9790799'],
            ['022022','0','9790799'],
            ['032022','0','9790799'],
            ['042022','0','9790799'],
            ['052022','0','9790799'],
            ['062022','0','9790799'],
            ['072022','0','9790799'],
            ['082022','0','9790799'],
            ['092022','0','9790799'],
            ['102022','815','9790799'],
            ['112022','2390','9790799'],
            ['122022','2335','9790799'],
            ['012023','4134','9790799'],
            ['022023','4065','9790799'],
            ['032023','3879','9790799'],
            ['042023','4234','9790799'],
            ['072019','0','108983536'],
            ['082019','0','108983536'],
            ['092019','0','108983536'],
            ['102019','0','108983536'],
            ['112019','0','108983536'],
            ['122019','0','108983536'],
            ['012020','0','108983536'],
            ['022020','0','108983536'],
            ['032020','0','108983536'],
            ['042020','0','108983536'],
            ['052020','0','108983536'],
            ['062020','0','108983536'],
            ['072020','0','108983536'],
            ['082020','0','108983536'],
            ['092020','0','108983536'],
            ['102020','0','108983536'],
            ['112020','0','108983536'],
            ['122020','0','108983536'],
            ['012021','0','108983536'],
            ['022021','0','108983536'],
            ['032021','0','108983536'],
            ['042021','0','108983536'],
            ['052021','0','108983536'],
            ['062021','0','108983536'],
            ['072021','0','108983536'],
            ['082021','0','108983536'],
            ['092021','0','108983536'],
            ['102021','0','108983536'],
            ['112021','0','108983536'],
            ['122021','0','108983536'],
            ['012022','0','108983536'],
            ['022022','0','108983536'],
            ['032022','0','108983536'],
            ['042022','0','108983536'],
            ['052022','0','108983536'],
            ['062022','3803','108983536'],
            ['072022','6639','108983536'],
            ['082022','7557','108983536'],
            ['092022','6932','108983536'],
            ['102022','10688','108983536'],
            ['112022','13776','108983536'],
            ['122022','13461','108983536'],
            ['012023','14955','108983536'],
            ['022023','14705','108983536'],
            ['032023','14032','108983536'],
            ['042023','14585','108983536'],
            ['072019','0','106473085'],
            ['082019','0','106473085'],
            ['092019','0','106473085'],
            ['102019','0','106473085'],
            ['112019','0','106473085'],
            ['122019','0','106473085'],
            ['012020','0','106473085'],
            ['022020','0','106473085'],
            ['032020','0','106473085'],
            ['042020','0','106473085'],
            ['052020','0','106473085'],
            ['062020','0','106473085'],
            ['072020','0','106473085'],
            ['082020','0','106473085'],
            ['092020','0','106473085'],
            ['102020','0','106473085'],
            ['112020','0','106473085'],
            ['122020','0','106473085'],
            ['012021','0','106473085'],
            ['022021','0','106473085'],
            ['032021','0','106473085'],
            ['042021','0','106473085'],
            ['052021','0','106473085'],
            ['062021','0','106473085'],
            ['072021','0','106473085'],
            ['082021','0','106473085'],
            ['092021','0','106473085'],
            ['102021','0','106473085'],
            ['112021','0','106473085'],
            ['122021','0','106473085'],
            ['012022','0','106473085'],
            ['022022','0','106473085'],
            ['032022','0','106473085'],
            ['042022','0','106473085'],
            ['052022','0','106473085'],
            ['062022','0','106473085'],
            ['072022','0','106473085'],
            ['082022','0','106473085'],
            ['092022','0','106473085'],
            ['102022','2181','106473085'],
            ['112022','5491','106473085'],
            ['122022','5366','106473085'],
            ['012023','8772','106473085'],
            ['022023','8625','106473085'],
            ['032023','8230','106473085'],
            ['042023','8230','106473085'],
            ['072019','0','108570010'],
            ['082019','0','108570010'],
            ['092019','0','108570010'],
            ['102019','0','108570010'],
            ['112019','0','108570010'],
            ['122019','0','108570010'],
            ['012020','0','108570010'],
            ['022020','0','108570010'],
            ['032020','0','108570010'],
            ['042020','0','108570010'],
            ['052020','0','108570010'],
            ['062020','0','108570010'],
            ['072020','0','108570010'],
            ['082020','0','108570010'],
            ['092020','0','108570010'],
            ['102020','0','108570010'],
            ['112020','0','108570010'],
            ['122020','0','108570010'],
            ['012021','0','108570010'],
            ['022021','0','108570010'],
            ['032021','0','108570010'],
            ['042021','0','108570010'],
            ['052021','0','108570010'],
            ['062021','0','108570010'],
            ['072021','0','108570010'],
            ['082021','0','108570010'],
            ['092021','0','108570010'],
            ['102021','0','108570010'],
            ['112021','0','108570010'],
            ['122021','0','108570010'],
            ['012022','0','108570010'],
            ['022022','0','108570010'],
            ['032022','0','108570010'],
            ['042022','0','108570010'],
            ['052022','0','108570010'],
            ['062022','0','108570010'],
            ['072022','0','108570010'],
            ['082022','0','108570010'],
            ['092022','0','108570010'],
            ['102022','14581','108570010'],
            ['112022','25512','108570010'],
            ['122022','24928','108570010'],
            ['012023','30730','108570010'],
            ['022023','30216','108570010'],
            ['032023','28832','108570010'],
            ['042023','30856','108570010'],
            ['072019','0','109869079'],
            ['082019','0','109869079'],
            ['092019','0','109869079'],
            ['102019','0','109869079'],
            ['112019','0','109869079'],
            ['122019','0','109869079'],
            ['012020','0','109869079'],
            ['022020','0','109869079'],
            ['032020','0','109869079'],
            ['042020','0','109869079'],
            ['052020','0','109869079'],
            ['062020','0','109869079'],
            ['072020','0','109869079'],
            ['082020','0','109869079'],
            ['092020','0','109869079'],
            ['102020','0','109869079'],
            ['112020','0','109869079'],
            ['122020','0','109869079'],
            ['012021','0','109869079'],
            ['022021','0','109869079'],
            ['032021','0','109869079'],
            ['042021','0','109869079'],
            ['052021','0','109869079'],
            ['062021','0','109869079'],
            ['072021','0','109869079'],
            ['082021','0','109869079'],
            ['092021','0','109869079'],
            ['102021','0','109869079'],
            ['112021','0','109869079'],
            ['122021','0','109869079'],
            ['012022','0','109869079'],
            ['022022','0','109869079'],
            ['032022','0','109869079'],
            ['042022','0','109869079'],
            ['052022','0','109869079'],
            ['062022','0','109869079'],
            ['072022','0','109869079'],
            ['082022','0','109869079'],
            ['092022','0','109869079'],
            ['102022','0','109869079'],
            ['112022','0','109869079'],
            ['122022','0','109869079'],
            ['012023','1995','109869079'],
            ['022023','1962','109869079'],
            ['032023','1872','109869079'],
            ['042023','2323','109869079'],
            ['072019','0','109869630'],
            ['082019','0','109869630'],
            ['092019','0','109869630'],
            ['102019','0','109869630'],
            ['112019','0','109869630'],
            ['122019','0','109869630'],
            ['012020','0','109869630'],
            ['022020','0','109869630'],
            ['032020','0','109869630'],
            ['042020','0','109869630'],
            ['052020','0','109869630'],
            ['062020','0','109869630'],
            ['072020','0','109869630'],
            ['082020','0','109869630'],
            ['092020','0','109869630'],
            ['102020','0','109869630'],
            ['112020','0','109869630'],
            ['122020','0','109869630'],
            ['012021','0','109869630'],
            ['022021','0','109869630'],
            ['032021','0','109869630'],
            ['042021','0','109869630'],
            ['052021','0','109869630'],
            ['062021','0','109869630'],
            ['072021','0','109869630'],
            ['082021','0','109869630'],
            ['092021','0','109869630'],
            ['102021','0','109869630'],
            ['112021','0','109869630'],
            ['122021','0','109869630'],
            ['012022','0','109869630'],
            ['022022','0','109869630'],
            ['032022','0','109869630'],
            ['042022','0','109869630'],
            ['052022','0','109869630'],
            ['062022','0','109869630'],
            ['072022','0','109869630'],
            ['082022','0','109869630'],
            ['092022','0','109869630'],
            ['102022','0','109869630'],
            ['112022','0','109869630'],
            ['122022','0','109869630'],
            ['012023','4458','109869630'],
            ['022023','4384','109869630'],
            ['032023','4183','109869630'],
            ['042023','4645','109869630'],
            ['072019','0','109876830'],
            ['082019','0','109876830'],
            ['092019','0','109876830'],
            ['102019','0','109876830'],
            ['112019','0','109876830'],
            ['122019','0','109876830'],
            ['012020','0','109876830'],
            ['022020','0','109876830'],
            ['032020','0','109876830'],
            ['042020','0','109876830'],
            ['052020','0','109876830'],
            ['062020','0','109876830'],
            ['072020','0','109876830'],
            ['082020','0','109876830'],
            ['092020','0','109876830'],
            ['102020','0','109876830'],
            ['112020','0','109876830'],
            ['122020','0','109876830'],
            ['012021','0','109876830'],
            ['022021','0','109876830'],
            ['032021','0','109876830'],
            ['042021','0','109876830'],
            ['052021','0','109876830'],
            ['062021','0','109876830'],
            ['072021','0','109876830'],
            ['082021','0','109876830'],
            ['092021','0','109876830'],
            ['102021','0','109876830'],
            ['112021','0','109876830'],
            ['122021','0','109876830'],
            ['012022','0','109876830'],
            ['022022','0','109876830'],
            ['032022','0','109876830'],
            ['042022','0','109876830'],
            ['052022','0','109876830'],
            ['062022','0','109876830'],
            ['072022','0','109876830'],
            ['082022','0','109876830'],
            ['092022','0','109876830'],
            ['102022','0','109876830'],
            ['112022','0','109876830'],
            ['122022','0','109876830'],
            ['012023','0','109876830'],
            ['022023','0','109876830'],
            ['032023','0','109876830'],
            ['042023','534','109876830'],
            ['072019','0','109852621'],
            ['082019','0','109852621'],
            ['092019','0','109852621'],
            ['102019','0','109852621'],
            ['112019','0','109852621'],
            ['122019','0','109852621'],
            ['012020','0','109852621'],
            ['022020','0','109852621'],
            ['032020','0','109852621'],
            ['042020','0','109852621'],
            ['052020','0','109852621'],
            ['062020','0','109852621'],
            ['072020','0','109852621'],
            ['082020','0','109852621'],
            ['092020','0','109852621'],
            ['102020','0','109852621'],
            ['112020','0','109852621'],
            ['122020','0','109852621'],
            ['012021','0','109852621'],
            ['022021','0','109852621'],
            ['032021','0','109852621'],
            ['042021','0','109852621'],
            ['052021','0','109852621'],
            ['062021','0','109852621'],
            ['072021','0','109852621'],
            ['082021','0','109852621'],
            ['092021','0','109852621'],
            ['102021','0','109852621'],
            ['112021','0','109852621'],
            ['122021','0','109852621'],
            ['012022','0','109852621'],
            ['022022','0','109852621'],
            ['032022','0','109852621'],
            ['042022','0','109852621'],
            ['052022','0','109852621'],
            ['062022','0','109852621'],
            ['072022','0','109852621'],
            ['082022','0','109852621'],
            ['092022','0','109852621'],
            ['102022','0','109852621'],
            ['112022','4582','109852621'],
            ['122022','4478','109852621'],
            ['012023','6653','109852621'],
            ['022023','6541','109852621'],
            ['032023','6242','109852621'],
            ['042023','6892','109852621']]


      for i in total:
            self.inserirAmarzenadoT(i[2],i[0],i[1],1,dist,cli)


    def Conta_gerados_copel(self):

        query = f' SELECT COUNT(DISTINCT(Referencia)) FROM `relatorios_gerador`'

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()[0][0]
        
        return resultado

    def Conta_ArmazenadosMCopel(self):

        query = f' SELECT COUNT(DISTINCT(Referencia)) FROM `relatorios_ArmazenamentoMensal` WHERE distribuidora_id=1 '

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()[0][0]
        
        return resultado
#-----------------------------------Celesc-------------------------------------------------#
    
    def Conta_gerados_celesc(self):

        query = f' SELECT COUNT(DISTINCT(Referencia)) FROM `relatorios_gerador_celesc`'

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()[0][0]
        
        return resultado
    
    def Lista_ref(self,valor):
        
        refBase = '042023'
        
        lista = []
        for i in range(valor):

            refBase = self.ReferenciaPosterior(refBase)
            lista.append(refBase)

        return lista
            
    def Conta_ArmazenadosM(self):

        query = f' SELECT COUNT(DISTINCT(Referencia)) FROM `relatorios_ArmazenamentoMensal` WHERE distribuidora_id=2 '

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()[0][0]
        
        return resultado

    def insere_mensal_anterior(self,cli,dist):

        mensal = [[' 48966365 ',' 0 ',' 072018 '],
                [' 48966365 ',' 0 ',' 082018 '],
                [' 48966365 ',' 0 ',' 092018 '],
                [' 48966365 ',' 0 ',' 102018 '],
                [' 48966365 ',' 0 ',' 112018 '],
                [' 48966365 ',' 0 ',' 122018 '],
                [' 48966365 ',' 0 ',' 012019 '],
                [' 48966365 ',' 0 ',' 022019 '],
                [' 48966365 ',' 0 ',' 032019 '],
                [' 48966365 ',' 0 ',' 042019 '],
                [' 48966365 ',' 0 ',' 052019 '],
                [' 48966365 ',' 0 ',' 062019 '],
                [' 48966365 ',' 0 ',' 072019 '],
                [' 48966365 ',' 0 ',' 082019 '],
                [' 48966365 ',' 0 ',' 092019 '],
                [' 48966365 ',' 0 ',' 102019 '],
                [' 48966365 ',' 0 ',' 112019 '],
                [' 48966365 ',' 0 ',' 122019 '],
                [' 48966365 ',' 0 ',' 012020 '],
                [' 48966365 ',' 0 ',' 022020 '],
                [' 48966365 ',' 0 ',' 032020 '],
                [' 48966365 ',' 0 ',' 042020 '],
                [' 48966365 ',' 0 ',' 052020 '],
                [' 48966365 ',' 0 ',' 062020 '],
                [' 48966365 ',' 0 ',' 072020 '],
                [' 48966365 ',' 0 ',' 082020 '],
                [' 48966365 ',' 0 ',' 092020 '],
                [' 48966365 ',' 0 ',' 102020 '],
                [' 48966365 ',' 0 ',' 112020 '],
                [' 48966365 ',' 0 ',' 122020 '],
                [' 48966365 ',' 2163 ',' 012021 '],
                [' 48966365 ',' 9 ',' 022021 '],
                [' 48966365 ',' 31 ',' 032021 '],
                [' 48966365 ',' 62 ',' 042021 '],
                [' 48966365 ',' 104 ',' 052021 '],
                [' 48966365 ',' -555 ',' 062021 '],
                [' 48966365 ',' 963 ',' 072021 '],
                [' 48966365 ',' 2445 ',' 082021 '],
                [' 48966365 ',' 722 ',' 092021 '],
                [' 48966365 ',' 775 ',' 102021 '],
                [' 48966365 ',' -3477 ',' 112021 '],
                [' 48966365 ',' 702 ',' 122021 '],
                [' 48966365 ',' -582 ',' 012022 '],
                [' 48966365 ',' 865 ',' 022022 '],
                [' 48966365 ',' 675 ',' 032022 '],
                [' 48966365 ',' 1302 ',' 042022 '],
                [' 48966365 ',' 2012 ',' 052022 '],
                [' 48966365 ',' 336 ',' 062022 '],
                [' 48966365 ',' 3021 ',' 072022 '],
                [' 48966365 ',' -237 ',' 082022 '],
                [' 48966365 ',' 3313 ',' 092022 '],
                [' 48966365 ',' 1449 ',' 102022 '],
                [' 48966365 ',' -3762 ',' 112022 '],
                [' 48966365 ',' -1870 ',' 122022 '],
                [' 48966365 ',' -21 ',' 012023 '],
                [' 48966365 ',' 112266 ',' 022023 '],
                [' 48966365 ',' -120541 ',' 032023 '],
                [' 48966365 ',' 0 ',' 042023 '],
                [' 48966365 ',' 0 ',' 052023 '],
                [' 52537266 ',' 0 ',' 072018 '],
                [' 52537266 ',' 0 ',' 082018 '],
                [' 52537266 ',' 0 ',' 092018 '],
                [' 52537266 ',' 0 ',' 102018 '],
                [' 52537266 ',' 0 ',' 112018 '],
                [' 52537266 ',' 0 ',' 122018 '],
                [' 52537266 ',' 0 ',' 012019 '],
                [' 52537266 ',' 0 ',' 022019 '],
                [' 52537266 ',' 0 ',' 032019 '],
                [' 52537266 ',' 0 ',' 042019 '],
                [' 52537266 ',' 0 ',' 052019 '],
                [' 52537266 ',' 0 ',' 062019 '],
                [' 52537266 ',' 0 ',' 072019 '],
                [' 52537266 ',' 0 ',' 082019 '],
                [' 52537266 ',' 0 ',' 092019 '],
                [' 52537266 ',' 0 ',' 102019 '],
                [' 52537266 ',' 0 ',' 112019 '],
                [' 52537266 ',' 0 ',' 122019 '],
                [' 52537266 ',' 0 ',' 012020 '],
                [' 52537266 ',' 0 ',' 022020 '],
                [' 52537266 ',' 0 ',' 032020 '],
                [' 52537266 ',' 0 ',' 042020 '],
                [' 52537266 ',' 0 ',' 052020 '],
                [' 52537266 ',' 0 ',' 062020 '],
                [' 52537266 ',' 0 ',' 072020 '],
                [' 52537266 ',' 0 ',' 082020 '],
                [' 52537266 ',' 0 ',' 092020 '],
                [' 52537266 ',' 0 ',' 102020 '],
                [' 52537266 ',' 0 ',' 112020 '],
                [' 52537266 ',' 0 ',' 122020 '],
                [' 52537266 ',' 9943 ',' 012021 '],
                [' 52537266 ',' 796 ',' 022021 '],
                [' 52537266 ',' 2673 ',' 032021 '],
                [' 52537266 ',' 6023 ',' 042021 '],
                [' 52537266 ',' 5376 ',' 052021 '],
                [' 52537266 ',' -5813 ',' 062021 '],
                [' 52537266 ',' 3977 ',' 072021 '],
                [' 52537266 ',' 19565 ',' 082021 '],
                [' 52537266 ',' 4719 ',' 092021 '],
                [' 52537266 ',' 29926 ',' 102021 '],
                [' 52537266 ',' -39946 ',' 112021 '],
                [' 52537266 ',' 12977 ',' 122021 '],
                [' 52537266 ',' -7414 ',' 012022 '],
                [' 52537266 ',' 6268 ',' 022022 '],
                [' 52537266 ',' 5755 ',' 032022 '],
                [' 52537266 ',' 8427 ',' 042022 '],
                [' 52537266 ',' 10188 ',' 052022 '],
                [' 52537266 ',' 1269 ',' 062022 '],
                [' 52537266 ',' 14879 ',' 072022 '],
                [' 52537266 ',' -1839 ',' 082022 '],
                [' 52537266 ',' 9670 ',' 092022 '],
                [' 52537266 ',' 5494 ',' 102022 '],
                [' 52537266 ',' -24054 ',' 112022 '],
                [' 52537266 ',' -11957 ',' 122022 '],
                [' 52537266 ',' -163 ',' 012023 '],
                [' 52537266 ',' 344188 ',' 022023 '],
                [' 52537266 ',' -403669 ',' 032023 '],
                [' 52537266 ',' 31503 ',' 042023 '],
                [' 52537266 ',' -19192 ',' 052023 '],
                [' 31172756 ',' 0 ',' 072018 '],
                [' 31172756 ',' 0 ',' 082018 '],
                [' 31172756 ',' 0 ',' 092018 '],
                [' 31172756 ',' 0 ',' 102018 '],
                [' 31172756 ',' 0 ',' 112018 '],
                [' 31172756 ',' 0 ',' 122018 '],
                [' 31172756 ',' 0 ',' 012019 '],
                [' 31172756 ',' 0 ',' 022019 '],
                [' 31172756 ',' 0 ',' 032019 '],
                [' 31172756 ',' 0 ',' 042019 '],
                [' 31172756 ',' 0 ',' 052019 '],
                [' 31172756 ',' 0 ',' 062019 '],
                [' 31172756 ',' 0 ',' 072019 '],
                [' 31172756 ',' 0 ',' 082019 '],
                [' 31172756 ',' 0 ',' 092019 '],
                [' 31172756 ',' 0 ',' 102019 '],
                [' 31172756 ',' 0 ',' 112019 '],
                [' 31172756 ',' 0 ',' 122019 '],
                [' 31172756 ',' 0 ',' 012020 '],
                [' 31172756 ',' 0 ',' 022020 '],
                [' 31172756 ',' 0 ',' 032020 '],
                [' 31172756 ',' 0 ',' 042020 '],
                [' 31172756 ',' 0 ',' 052020 '],
                [' 31172756 ',' 0 ',' 062020 '],
                [' 31172756 ',' 0 ',' 072020 '],
                [' 31172756 ',' 0 ',' 082020 '],
                [' 31172756 ',' 0 ',' 092020 '],
                [' 31172756 ',' 0 ',' 102020 '],
                [' 31172756 ',' 0 ',' 112020 '],
                [' 31172756 ',' 0 ',' 122020 '],
                [' 31172756 ',' 559 ',' 012021 '],
                [' 31172756 ',' 35 ',' 022021 '],
                [' 31172756 ',' 91 ',' 032021 '],
                [' 31172756 ',' 58 ',' 042021 '],
                [' 31172756 ',' 169 ',' 052021 '],
                [' 31172756 ',' -214 ',' 062021 '],
                [' 31172756 ',' 189 ',' 072021 '],
                [' 31172756 ',' 1116 ',' 082021 '],
                [' 31172756 ',' 176 ',' 092021 '],
                [' 31172756 ',' 1348 ',' 102021 '],
                [' 31172756 ',' -1826 ',' 112021 '],
                [' 31172756 ',' 625 ',' 122021 '],
                [' 31172756 ',' -344 ',' 012022 '],
                [' 31172756 ',' 71 ',' 022022 '],
                [' 31172756 ',' 261 ',' 032022 '],
                [' 31172756 ',' 312 ',' 042022 '],
                [' 31172756 ',' 204 ',' 052022 '],
                [' 31172756 ',' 20 ',' 062022 '],
                [' 31172756 ',' 339 ',' 072022 '],
                [' 31172756 ',' -65 ',' 082022 '],
                [' 31172756 ',' 597 ',' 092022 '],
                [' 31172756 ',' 208 ',' 102022 '],
                [' 31172756 ',' -919 ',' 112022 '],
                [' 31172756 ',' -457 ',' 122022 '],
                [' 31172756 ',' -6 ',' 012023 '],
                [' 31172756 ',' 24721 ',' 022023 '],
                [' 31172756 ',' -26788 ',' 032023 '],
                [' 31172756 ',' 2426 ',' 042023 '],
                [' 31172756 ',' -1440 ',' 052023 '],
                [' 42944114 ',' 0 ',' 072018 '],
                [' 42944114 ',' 0 ',' 082018 '],
                [' 42944114 ',' 0 ',' 092018 '],
                [' 42944114 ',' 0 ',' 102018 '],
                [' 42944114 ',' 0 ',' 112018 '],
                [' 42944114 ',' 0 ',' 122018 '],
                [' 42944114 ',' 0 ',' 012019 '],
                [' 42944114 ',' 0 ',' 022019 '],
                [' 42944114 ',' 0 ',' 032019 '],
                [' 42944114 ',' 0 ',' 042019 '],
                [' 42944114 ',' 0 ',' 052019 '],
                [' 42944114 ',' 0 ',' 062019 '],
                [' 42944114 ',' 0 ',' 072019 '],
                [' 42944114 ',' 0 ',' 082019 '],
                [' 42944114 ',' 0 ',' 092019 '],
                [' 42944114 ',' 0 ',' 102019 '],
                [' 42944114 ',' 0 ',' 112019 '],
                [' 42944114 ',' 0 ',' 122019 '],
                [' 42944114 ',' 0 ',' 012020 '],
                [' 42944114 ',' 0 ',' 022020 '],
                [' 42944114 ',' 0 ',' 032020 '],
                [' 42944114 ',' 0 ',' 042020 '],
                [' 42944114 ',' 0 ',' 052020 '],
                [' 42944114 ',' 0 ',' 062020 '],
                [' 42944114 ',' 0 ',' 072020 '],
                [' 42944114 ',' 0 ',' 082020 '],
                [' 42944114 ',' 0 ',' 092020 '],
                [' 42944114 ',' 0 ',' 102020 '],
                [' 42944114 ',' 0 ',' 112020 '],
                [' 42944114 ',' 0 ',' 122020 '],
                [' 42944114 ',' 0 ',' 012021 '],
                [' 42944114 ',' 0 ',' 022021 '],
                [' 42944114 ',' 0 ',' 032021 '],
                [' 42944114 ',' 198 ',' 042021 '],
                [' 42944114 ',' 227 ',' 052021 '],
                [' 42944114 ',' -100 ',' 062021 '],
                [' 42944114 ',' 212 ',' 072021 '],
                [' 42944114 ',' 1147 ',' 082021 '],
                [' 42944114 ',' 181 ',' 092021 '],
                [' 42944114 ',' 1570 ',' 102021 '],
                [' 42944114 ',' -1778 ',' 112021 '],
                [' 42944114 ',' 648 ',' 122021 '],
                [' 42944114 ',' -340 ',' 012022 '],
                [' 42944114 ',' 248 ',' 022022 '],
                [' 42944114 ',' 186 ',' 032022 '],
                [' 42944114 ',' 283 ',' 042022 '],
                [' 42944114 ',' 213 ',' 052022 '],
                [' 42944114 ',' 29 ',' 062022 '],
                [' 42944114 ',' 429 ',' 072022 '],
                [' 42944114 ',' -69 ',' 082022 '],
                [' 42944114 ',' 583 ',' 092022 '],
                [' 42944114 ',' 263 ',' 102022 '],
                [' 42944114 ',' -965 ',' 112022 '],
                [' 42944114 ',' -480 ',' 122022 '],
                [' 42944114 ',' -7 ',' 012023 '],
                [' 42944114 ',' 24602 ',' 022023 '],
                [' 42944114 ',' -26798 ',' 032023 '],
                [' 42944114 ',' 2360 ',' 042023 '],
                [' 42944114 ',' -1407 ',' 052023 '],
                [' 21909386 ',' 0 ',' 072018 '],
                [' 21909386 ',' 0 ',' 082018 '],
                [' 21909386 ',' 0 ',' 092018 '],
                [' 21909386 ',' 0 ',' 102018 '],
                [' 21909386 ',' 0 ',' 112018 '],
                [' 21909386 ',' 0 ',' 122018 '],
                [' 21909386 ',' 0 ',' 012019 '],
                [' 21909386 ',' 0 ',' 022019 '],
                [' 21909386 ',' 0 ',' 032019 '],
                [' 21909386 ',' 0 ',' 042019 '],
                [' 21909386 ',' 0 ',' 052019 '],
                [' 21909386 ',' 0 ',' 062019 '],
                [' 21909386 ',' 0 ',' 072019 '],
                [' 21909386 ',' 0 ',' 082019 '],
                [' 21909386 ',' 0 ',' 092019 '],
                [' 21909386 ',' 0 ',' 102019 '],
                [' 21909386 ',' 0 ',' 112019 '],
                [' 21909386 ',' 0 ',' 122019 '],
                [' 21909386 ',' 0 ',' 012020 '],
                [' 21909386 ',' 0 ',' 022020 '],
                [' 21909386 ',' 0 ',' 032020 '],
                [' 21909386 ',' 0 ',' 042020 '],
                [' 21909386 ',' 0 ',' 052020 '],
                [' 21909386 ',' 0 ',' 062020 '],
                [' 21909386 ',' 0 ',' 072020 '],
                [' 21909386 ',' 0 ',' 082020 '],
                [' 21909386 ',' 0 ',' 092020 '],
                [' 21909386 ',' 0 ',' 102020 '],
                [' 21909386 ',' 0 ',' 112020 '],
                [' 21909386 ',' 0 ',' 122020 '],
                [' 21909386 ',' 0 ',' 012021 '],
                [' 21909386 ',' 0 ',' 022021 '],
                [' 21909386 ',' 0 ',' 032021 '],
                [' 21909386 ',' 0 ',' 042021 '],
                [' 21909386 ',' 0 ',' 052021 '],
                [' 21909386 ',' 0 ',' 062021 '],
                [' 21909386 ',' 0 ',' 072021 '],
                [' 21909386 ',' 0 ',' 082021 '],
                [' 21909386 ',' 0 ',' 092021 '],
                [' 21909386 ',' 0 ',' 102021 '],
                [' 21909386 ',' 0 ',' 112021 '],
                [' 21909386 ',' 689 ',' 122021 '],
                [' 21909386 ',' -102 ',' 012022 '],
                [' 21909386 ',' 266 ',' 022022 '],
                [' 21909386 ',' 215 ',' 032022 '],
                [' 21909386 ',' 304 ',' 042022 '],
                [' 21909386 ',' 229 ',' 052022 '],
                [' 21909386 ',' 22 ',' 062022 '],
                [' 21909386 ',' 315 ',' 072022 '],
                [' 21909386 ',' -40 ',' 082022 '],
                [' 21909386 ',' 501 ',' 092022 '],
                [' 21909386 ',' 189 ',' 102022 '],
                [' 21909386 ',' -605 ',' 112022 '],
                [' 21909386 ',' -301 ',' 122022 '],
                [' 21909386 ',' -4 ',' 012023 '],
                [' 21909386 ',' 23665 ',' 022023 '],
                [' 21909386 ',' -24896 ',' 032023 '],
                [' 21909386 ',' 2236 ',' 042023 '],
                [' 21909386 ',' -1329 ',' 052023 '],
                [' 53903541 ',' 0 ',' 072018 '],
                [' 53903541 ',' 0 ',' 082018 '],
                [' 53903541 ',' 0 ',' 092018 '],
                [' 53903541 ',' 0 ',' 102018 '],
                [' 53903541 ',' 0 ',' 112018 '],
                [' 53903541 ',' 0 ',' 122018 '],
                [' 53903541 ',' 0 ',' 012019 '],
                [' 53903541 ',' 0 ',' 022019 '],
                [' 53903541 ',' 0 ',' 032019 '],
                [' 53903541 ',' 0 ',' 042019 '],
                [' 53903541 ',' 0 ',' 052019 '],
                [' 53903541 ',' 0 ',' 062019 '],
                [' 53903541 ',' 0 ',' 072019 '],
                [' 53903541 ',' 0 ',' 082019 '],
                [' 53903541 ',' 0 ',' 092019 '],
                [' 53903541 ',' 0 ',' 102019 '],
                [' 53903541 ',' 0 ',' 112019 '],
                [' 53903541 ',' 0 ',' 122019 '],
                [' 53903541 ',' 0 ',' 012020 '],
                [' 53903541 ',' 0 ',' 022020 '],
                [' 53903541 ',' 0 ',' 032020 '],
                [' 53903541 ',' 0 ',' 042020 '],
                [' 53903541 ',' 0 ',' 052020 '],
                [' 53903541 ',' 0 ',' 062020 '],
                [' 53903541 ',' 0 ',' 072020 '],
                [' 53903541 ',' 0 ',' 082020 '],
                [' 53903541 ',' 0 ',' 092020 '],
                [' 53903541 ',' 0 ',' 102020 '],
                [' 53903541 ',' 0 ',' 112020 '],
                [' 53903541 ',' 0 ',' 122020 '],
                [' 53903541 ',' 0 ',' 012021 '],
                [' 53903541 ',' 0 ',' 022021 '],
                [' 53903541 ',' 0 ',' 032021 '],
                [' 53903541 ',' 0 ',' 042021 '],
                [' 53903541 ',' 0 ',' 052021 '],
                [' 53903541 ',' 0 ',' 062021 '],
                [' 53903541 ',' 0 ',' 072021 '],
                [' 53903541 ',' 0 ',' 082021 '],
                [' 53903541 ',' 0 ',' 092021 '],
                [' 53903541 ',' 0 ',' 102021 '],
                [' 53903541 ',' 0 ',' 112021 '],
                [' 53903541 ',' 618 ',' 122021 '],
                [' 53903541 ',' -91 ',' 012022 '],
                [' 53903541 ',' 178 ',' 022022 '],
                [' 53903541 ',' 385 ',' 032022 '],
                [' 53903541 ',' 731 ',' 042022 '],
                [' 53903541 ',' 975 ',' 052022 '],
                [' 53903541 ',' 93 ',' 062022 '],
                [' 53903541 ',' 727 ',' 072022 '],
                [' 53903541 ',' -74 ',' 082022 '],
                [' 53903541 ',' 882 ',' 092022 '],
                [' 53903541 ',' 394 ',' 102022 '],
                [' 53903541 ',' -1126 ',' 112022 '],
                [' 53903541 ',' -560 ',' 122022 '],
                [' 53903541 ',' -8 ',' 012023 '],
                [' 53903541 ',' 66686 ',' 022023 '],
                [' 53903541 ',' -68577 ',' 032023 '],
                [' 53903541 ',' 5803 ',' 042023 '],
                [' 53903541 ',' -3484 ',' 052023 '],
                [' 41973722 ',' 0 ',' 072018 '],
                [' 41973722 ',' 0 ',' 082018 '],
                [' 41973722 ',' 0 ',' 092018 '],
                [' 41973722 ',' 0 ',' 102018 '],
                [' 41973722 ',' 0 ',' 112018 '],
                [' 41973722 ',' 0 ',' 122018 '],
                [' 41973722 ',' 0 ',' 012019 '],
                [' 41973722 ',' 0 ',' 022019 '],
                [' 41973722 ',' 0 ',' 032019 '],
                [' 41973722 ',' 0 ',' 042019 '],
                [' 41973722 ',' 0 ',' 052019 '],
                [' 41973722 ',' 0 ',' 062019 '],
                [' 41973722 ',' 0 ',' 072019 '],
                [' 41973722 ',' 0 ',' 082019 '],
                [' 41973722 ',' 0 ',' 092019 '],
                [' 41973722 ',' 0 ',' 102019 '],
                [' 41973722 ',' 0 ',' 112019 '],
                [' 41973722 ',' 0 ',' 122019 '],
                [' 41973722 ',' 0 ',' 012020 '],
                [' 41973722 ',' 0 ',' 022020 '],
                [' 41973722 ',' 0 ',' 032020 '],
                [' 41973722 ',' 0 ',' 042020 '],
                [' 41973722 ',' 0 ',' 052020 '],
                [' 41973722 ',' 0 ',' 062020 '],
                [' 41973722 ',' 0 ',' 072020 '],
                [' 41973722 ',' 0 ',' 082020 '],
                [' 41973722 ',' 0 ',' 092020 '],
                [' 41973722 ',' 0 ',' 102020 '],
                [' 41973722 ',' 0 ',' 112020 '],
                [' 41973722 ',' 0 ',' 122020 '],
                [' 41973722 ',' 0 ',' 012021 '],
                [' 41973722 ',' 0 ',' 022021 '],
                [' 41973722 ',' 0 ',' 032021 '],
                [' 41973722 ',' 0 ',' 042021 '],
                [' 41973722 ',' 0 ',' 052021 '],
                [' 41973722 ',' 0 ',' 062021 '],
                [' 41973722 ',' 0 ',' 072021 '],
                [' 41973722 ',' 0 ',' 082021 '],
                [' 41973722 ',' 0 ',' 092021 '],
                [' 41973722 ',' 0 ',' 102021 '],
                [' 41973722 ',' 0 ',' 112021 '],
                [' 41973722 ',' 0 ',' 122021 '],
                [' 41973722 ',' 0 ',' 012022 '],
                [' 41973722 ',' 1833 ',' 022022 '],
                [' 41973722 ',' 990 ',' 032022 '],
                [' 41973722 ',' 2150 ',' 042022 '],
                [' 41973722 ',' 3025 ',' 052022 '],
                [' 41973722 ',' 378 ',' 062022 '],
                [' 41973722 ',' 3052 ',' 072022 '],
                [' 41973722 ',' -235 ',' 082022 '],
                [' 41973722 ',' 6035 ',' 092022 '],
                [' 41973722 ',' 2230 ',' 102022 '],
                [' 41973722 ',' -4548 ',' 112022 '],
                [' 41973722 ',' -2261 ',' 122022 '],
                [' 41973722 ',' -31 ',' 012023 '],
                [' 41973722 ',' 92179 ',' 022023 '],
                [' 41973722 ',' -102947 ',' 032023 '],
                [' 41973722 ',' 17105 ',' 042023 '],
                [' 41973722 ',' -9386 ',' 052023 '],
                [' 52496373 ',' 0 ',' 072018 '],
                [' 52496373 ',' 0 ',' 082018 '],
                [' 52496373 ',' 0 ',' 092018 '],
                [' 52496373 ',' 0 ',' 102018 '],
                [' 52496373 ',' 0 ',' 112018 '],
                [' 52496373 ',' 0 ',' 122018 '],
                [' 52496373 ',' 0 ',' 012019 '],
                [' 52496373 ',' 0 ',' 022019 '],
                [' 52496373 ',' 0 ',' 032019 '],
                [' 52496373 ',' 0 ',' 042019 '],
                [' 52496373 ',' 0 ',' 052019 '],
                [' 52496373 ',' 0 ',' 062019 '],
                [' 52496373 ',' 0 ',' 072019 '],
                [' 52496373 ',' 0 ',' 082019 '],
                [' 52496373 ',' 0 ',' 092019 '],
                [' 52496373 ',' 0 ',' 102019 '],
                [' 52496373 ',' 0 ',' 112019 '],
                [' 52496373 ',' 0 ',' 122019 '],
                [' 52496373 ',' 0 ',' 012020 '],
                [' 52496373 ',' 0 ',' 022020 '],
                [' 52496373 ',' 0 ',' 032020 '],
                [' 52496373 ',' 0 ',' 042020 '],
                [' 52496373 ',' 0 ',' 052020 '],
                [' 52496373 ',' 0 ',' 062020 '],
                [' 52496373 ',' 0 ',' 072020 '],
                [' 52496373 ',' 0 ',' 082020 '],
                [' 52496373 ',' 0 ',' 092020 '],
                [' 52496373 ',' 0 ',' 102020 '],
                [' 52496373 ',' 0 ',' 112020 '],
                [' 52496373 ',' 0 ',' 122020 '],
                [' 52496373 ',' 0 ',' 012021 '],
                [' 52496373 ',' 0 ',' 022021 '],
                [' 52496373 ',' 0 ',' 032021 '],
                [' 52496373 ',' 0 ',' 042021 '],
                [' 52496373 ',' 0 ',' 052021 '],
                [' 52496373 ',' 0 ',' 062021 '],
                [' 52496373 ',' 0 ',' 072021 '],
                [' 52496373 ',' 0 ',' 082021 '],
                [' 52496373 ',' 0 ',' 092021 '],
                [' 52496373 ',' 0 ',' 102021 '],
                [' 52496373 ',' 0 ',' 112021 '],
                [' 52496373 ',' 0 ',' 122021 '],
                [' 52496373 ',' 0 ',' 012022 '],
                [' 52496373 ',' 0 ',' 022022 '],
                [' 52496373 ',' 0 ',' 032022 '],
                [' 52496373 ',' 0 ',' 042022 '],
                [' 52496373 ',' 0 ',' 052022 '],
                [' 52496373 ',' 0 ',' 062022 '],
                [' 52496373 ',' 0 ',' 072022 '],
                [' 52496373 ',' 0 ',' 082022 '],
                [' 52496373 ',' 710 ',' 092022 '],
                [' 52496373 ',' 0 ',' 102022 '],
                [' 52496373 ',' 0 ',' 112022 '],
                [' 52496373 ',' 0 ',' 122022 '],
                [' 52496373 ',' 0 ',' 012023 '],
                [' 52496373 ',' 0 ',' 022023 '],
                [' 52496373 ',' 0 ',' 032023 '],
                [' 52496373 ',' 0 ',' 042023 '],
                [' 52496373 ',' 0 ',' 052023 '],
                [' 32205151 ',' 0 ',' 072018 '],
                [' 32205151 ',' 0 ',' 082018 '],
                [' 32205151 ',' 0 ',' 092018 '],
                [' 32205151 ',' 0 ',' 102018 '],
                [' 32205151 ',' 0 ',' 112018 '],
                [' 32205151 ',' 0 ',' 122018 '],
                [' 32205151 ',' 0 ',' 012019 '],
                [' 32205151 ',' 0 ',' 022019 '],
                [' 32205151 ',' 0 ',' 032019 '],
                [' 32205151 ',' 0 ',' 042019 '],
                [' 32205151 ',' 0 ',' 052019 '],
                [' 32205151 ',' 0 ',' 062019 '],
                [' 32205151 ',' 0 ',' 072019 '],
                [' 32205151 ',' 0 ',' 082019 '],
                [' 32205151 ',' 0 ',' 092019 '],
                [' 32205151 ',' 0 ',' 102019 '],
                [' 32205151 ',' 0 ',' 112019 '],
                [' 32205151 ',' 0 ',' 122019 '],
                [' 32205151 ',' 0 ',' 012020 '],
                [' 32205151 ',' 0 ',' 022020 '],
                [' 32205151 ',' 0 ',' 032020 '],
                [' 32205151 ',' 0 ',' 042020 '],
                [' 32205151 ',' 0 ',' 052020 '],
                [' 32205151 ',' 0 ',' 062020 '],
                [' 32205151 ',' 0 ',' 072020 '],
                [' 32205151 ',' 0 ',' 082020 '],
                [' 32205151 ',' 0 ',' 092020 '],
                [' 32205151 ',' 0 ',' 102020 '],
                [' 32205151 ',' 0 ',' 112020 '],
                [' 32205151 ',' 0 ',' 122020 '],
                [' 32205151 ',' 0 ',' 012021 '],
                [' 32205151 ',' 0 ',' 022021 '],
                [' 32205151 ',' 0 ',' 032021 '],
                [' 32205151 ',' 0 ',' 042021 '],
                [' 32205151 ',' 0 ',' 052021 '],
                [' 32205151 ',' 0 ',' 062021 '],
                [' 32205151 ',' 0 ',' 072021 '],
                [' 32205151 ',' 0 ',' 082021 '],
                [' 32205151 ',' 0 ',' 092021 '],
                [' 32205151 ',' 0 ',' 102021 '],
                [' 32205151 ',' 0 ',' 112021 '],
                [' 32205151 ',' 0 ',' 122021 '],
                [' 32205151 ',' 0 ',' 012022 '],
                [' 32205151 ',' 0 ',' 022022 '],
                [' 32205151 ',' 0 ',' 032022 '],
                [' 32205151 ',' 0 ',' 042022 '],
                [' 32205151 ',' 0 ',' 052022 '],
                [' 32205151 ',' 0 ',' 062022 '],
                [' 32205151 ',' 0 ',' 072022 '],
                [' 32205151 ',' 0 ',' 082022 '],
                [' 32205151 ',' 0 ',' 092022 '],
                [' 32205151 ',' 0 ',' 102022 '],
                [' 32205151 ',' 0 ',' 112022 '],
                [' 32205151 ',' 0 ',' 122022 '],
                [' 32205151 ',' 0 ',' 012023 '],
                [' 32205151 ',' 43995 ',' 022023 '],
                [' 32205151 ',' -43218 ',' 032023 '],
                [' 32205151 ',' 3845 ',' 042023 '],
                [' 32205151 ',' -2289 ',' 052023 ']]
        for i in mensal:
            self.inserirAmarzenadoM(i[0],i[2],i[1],1,dist,cli)
    def insere_total_anterior(self,cli,dist):

        total = [[' 48966365 ',' 0 ',' 072018 '],
                [' 48966365 ',' 0 ',' 082018 '],
                [' 48966365 ',' 0 ',' 092018 '],
                [' 48966365 ',' 0 ',' 102018 '],
                [' 48966365 ',' 0 ',' 112018 '],
                [' 48966365 ',' 0 ',' 122018 '],
                [' 48966365 ',' 0 ',' 012019 '],
                [' 48966365 ',' 0 ',' 022019 '],
                [' 48966365 ',' 0 ',' 032019 '],
                [' 48966365 ',' 0 ',' 042019 '],
                [' 48966365 ',' 0 ',' 052019 '],
                [' 48966365 ',' 0 ',' 062019 '],
                [' 48966365 ',' 0 ',' 072019 '],
                [' 48966365 ',' 0 ',' 082019 '],
                [' 48966365 ',' 0 ',' 092019 '],
                [' 48966365 ',' 0 ',' 102019 '],
                [' 48966365 ',' 0 ',' 112019 '],
                [' 48966365 ',' 0 ',' 122019 '],
                [' 48966365 ',' 0 ',' 012020 '],
                [' 48966365 ',' 0 ',' 022020 '],
                [' 48966365 ',' 0 ',' 032020 '],
                [' 48966365 ',' 0 ',' 042020 '],
                [' 48966365 ',' 0 ',' 052020 '],
                [' 48966365 ',' 0 ',' 062020 '],
                [' 48966365 ',' 0 ',' 072020 '],
                [' 48966365 ',' 0 ',' 082020 '],
                [' 48966365 ',' 0 ',' 092020 '],
                [' 48966365 ',' 0 ',' 102020 '],
                [' 48966365 ',' 0 ',' 112020 '],
                [' 48966365 ',' 0 ',' 122020 '],
                [' 48966365 ',' 2163 ',' 012021 '],
                [' 48966365 ',' 2172 ',' 022021 '],
                [' 48966365 ',' 2203 ',' 032021 '],
                [' 48966365 ',' 2265 ',' 042021 '],
                [' 48966365 ',' 2369 ',' 052021 '],
                [' 48966365 ',' 1814 ',' 062021 '],
                [' 48966365 ',' 2777 ',' 072021 '],
                [' 48966365 ',' 5222 ',' 082021 '],
                [' 48966365 ',' 5944 ',' 092021 '],
                [' 48966365 ',' 6719 ',' 102021 '],
                [' 48966365 ',' 3242 ',' 112021 '],
                [' 48966365 ',' 3943 ',' 122021 '],
                [' 48966365 ',' 3361 ',' 012022 '],
                [' 48966365 ',' 4226 ',' 022022 '],
                [' 48966365 ',' 4901 ',' 032022 '],
                [' 48966365 ',' 6202 ',' 042022 '],
                [' 48966365 ',' 8214 ',' 052022 '],
                [' 48966365 ',' 8550 ',' 062022 '],
                [' 48966365 ',' 11570 ',' 072022 '],
                [' 48966365 ',' 11333 ',' 082022 '],
                [' 48966365 ',' 14646 ',' 092022 '],
                [' 48966365 ',' 16095 ',' 102022 '],
                [' 48966365 ',' 12333 ',' 112022 '],
                [' 48966365 ',' 10463 ',' 122022 '],
                [' 48966365 ',' 10442 ',' 012023 '],
                [' 48966365 ',' 122708 ',' 022023 '],
                [' 48966365 ',' 2167 ',' 032023 '],
                [' 48966365 ',' 0 ',' 042023 '],
                [' 48966365 ',' 0 ',' 052023 '],
                [' 52537266 ',' 0 ',' 072018 '],
                [' 52537266 ',' 0 ',' 082018 '],
                [' 52537266 ',' 0 ',' 092018 '],
                [' 52537266 ',' 0 ',' 102018 '],
                [' 52537266 ',' 0 ',' 112018 '],
                [' 52537266 ',' 0 ',' 122018 '],
                [' 52537266 ',' 0 ',' 012019 '],
                [' 52537266 ',' 0 ',' 022019 '],
                [' 52537266 ',' 0 ',' 032019 '],
                [' 52537266 ',' 0 ',' 042019 '],
                [' 52537266 ',' 0 ',' 052019 '],
                [' 52537266 ',' 0 ',' 062019 '],
                [' 52537266 ',' 0 ',' 072019 '],
                [' 52537266 ',' 0 ',' 082019 '],
                [' 52537266 ',' 0 ',' 092019 '],
                [' 52537266 ',' 0 ',' 102019 '],
                [' 52537266 ',' 0 ',' 112019 '],
                [' 52537266 ',' 0 ',' 122019 '],
                [' 52537266 ',' 0 ',' 012020 '],
                [' 52537266 ',' 0 ',' 022020 '],
                [' 52537266 ',' 0 ',' 032020 '],
                [' 52537266 ',' 0 ',' 042020 '],
                [' 52537266 ',' 0 ',' 052020 '],
                [' 52537266 ',' 0 ',' 062020 '],
                [' 52537266 ',' 0 ',' 072020 '],
                [' 52537266 ',' 0 ',' 082020 '],
                [' 52537266 ',' 0 ',' 092020 '],
                [' 52537266 ',' 0 ',' 102020 '],
                [' 52537266 ',' 0 ',' 112020 '],
                [' 52537266 ',' 0 ',' 122020 '],
                [' 52537266 ',' 9943 ',' 012021 '],
                [' 52537266 ',' 10739 ',' 022021 '],
                [' 52537266 ',' 13412 ',' 032021 '],
                [' 52537266 ',' 19435 ',' 042021 '],
                [' 52537266 ',' 24811 ',' 052021 '],
                [' 52537266 ',' 18997 ',' 062021 '],
                [' 52537266 ',' 22975 ',' 072021 '],
                [' 52537266 ',' 42539 ',' 082021 '],
                [' 52537266 ',' 47258 ',' 092021 '],
                [' 52537266 ',' 77183 ',' 102021 '],
                [' 52537266 ',' 37237 ',' 112021 '],
                [' 52537266 ',' 50214 ',' 122021 '],
                [' 52537266 ',' 42800 ',' 012022 '],
                [' 52537266 ',' 49069 ',' 022022 '],
                [' 52537266 ',' 54824 ',' 032022 '],
                [' 52537266 ',' 63251 ',' 042022 '],
                [' 52537266 ',' 73439 ',' 052022 '],
                [' 52537266 ',' 74708 ',' 062022 '],
                [' 52537266 ',' 89587 ',' 072022 '],
                [' 52537266 ',' 87748 ',' 082022 '],
                [' 52537266 ',' 97418 ',' 092022 '],
                [' 52537266 ',' 102912 ',' 102022 '],
                [' 52537266 ',' 78857 ',' 112022 '],
                [' 52537266 ',' 66900 ',' 122022 '],
                [' 52537266 ',' 66737 ',' 012023 '],
                [' 52537266 ',' 410925 ',' 022023 '],
                [' 52537266 ',' 7257 ',' 032023 '],
                [' 52537266 ',' 38760 ',' 042023 '],
                [' 52537266 ',' 19568 ',' 052023 '],
                [' 31172756 ',' 0 ',' 072018 '],
                [' 31172756 ',' 0 ',' 082018 '],
                [' 31172756 ',' 0 ',' 092018 '],
                [' 31172756 ',' 0 ',' 102018 '],
                [' 31172756 ',' 0 ',' 112018 '],
                [' 31172756 ',' 0 ',' 122018 '],
                [' 31172756 ',' 0 ',' 012019 '],
                [' 31172756 ',' 0 ',' 022019 '],
                [' 31172756 ',' 0 ',' 032019 '],
                [' 31172756 ',' 0 ',' 042019 '],
                [' 31172756 ',' 0 ',' 052019 '],
                [' 31172756 ',' 0 ',' 062019 '],
                [' 31172756 ',' 0 ',' 072019 '],
                [' 31172756 ',' 0 ',' 082019 '],
                [' 31172756 ',' 0 ',' 092019 '],
                [' 31172756 ',' 0 ',' 102019 '],
                [' 31172756 ',' 0 ',' 112019 '],
                [' 31172756 ',' 0 ',' 122019 '],
                [' 31172756 ',' 0 ',' 012020 '],
                [' 31172756 ',' 0 ',' 022020 '],
                [' 31172756 ',' 0 ',' 032020 '],
                [' 31172756 ',' 0 ',' 042020 '],
                [' 31172756 ',' 0 ',' 052020 '],
                [' 31172756 ',' 0 ',' 062020 '],
                [' 31172756 ',' 0 ',' 072020 '],
                [' 31172756 ',' 0 ',' 082020 '],
                [' 31172756 ',' 0 ',' 092020 '],
                [' 31172756 ',' 0 ',' 102020 '],
                [' 31172756 ',' 0 ',' 112020 '],
                [' 31172756 ',' 0 ',' 122020 '],
                [' 31172756 ',' 559 ',' 012021 '],
                [' 31172756 ',' 594 ',' 022021 '],
                [' 31172756 ',' 685 ',' 032021 '],
                [' 31172756 ',' 744 ',' 042021 '],
                [' 31172756 ',' 912 ',' 052021 '],
                [' 31172756 ',' 699 ',' 062021 '],
                [' 31172756 ',' 887 ',' 072021 '],
                [' 31172756 ',' 2003 ',' 082021 '],
                [' 31172756 ',' 2180 ',' 092021 '],
                [' 31172756 ',' 3528 ',' 102021 '],
                [' 31172756 ',' 1702 ',' 112021 '],
                [' 31172756 ',' 2327 ',' 122021 '],
                [' 31172756 ',' 1984 ',' 012022 '],
                [' 31172756 ',' 2055 ',' 022022 '],
                [' 31172756 ',' 2316 ',' 032022 '],
                [' 31172756 ',' 2628 ',' 042022 '],
                [' 31172756 ',' 2832 ',' 052022 '],
                [' 31172756 ',' 2852 ',' 062022 '],
                [' 31172756 ',' 3190 ',' 072022 '],
                [' 31172756 ',' 3125 ',' 082022 '],
                [' 31172756 ',' 3722 ',' 092022 '],
                [' 31172756 ',' 3930 ',' 102022 '],
                [' 31172756 ',' 3012 ',' 112022 '],
                [' 31172756 ',' 2555 ',' 122022 '],
                [' 31172756 ',' 2549 ',' 012023 '],
                [' 31172756 ',' 27270 ',' 022023 '],
                [' 31172756 ',' 482 ',' 032023 '],
                [' 31172756 ',' 2908 ',' 042023 '],
                [' 31172756 ',' 1468 ',' 052023 '],
                [' 42944114 ',' 0 ',' 072018 '],
                [' 42944114 ',' 0 ',' 082018 '],
                [' 42944114 ',' 0 ',' 092018 '],
                [' 42944114 ',' 0 ',' 102018 '],
                [' 42944114 ',' 0 ',' 112018 '],
                [' 42944114 ',' 0 ',' 122018 '],
                [' 42944114 ',' 0 ',' 012019 '],
                [' 42944114 ',' 0 ',' 022019 '],
                [' 42944114 ',' 0 ',' 032019 '],
                [' 42944114 ',' 0 ',' 042019 '],
                [' 42944114 ',' 0 ',' 052019 '],
                [' 42944114 ',' 0 ',' 062019 '],
                [' 42944114 ',' 0 ',' 072019 '],
                [' 42944114 ',' 0 ',' 082019 '],
                [' 42944114 ',' 0 ',' 092019 '],
                [' 42944114 ',' 0 ',' 102019 '],
                [' 42944114 ',' 0 ',' 112019 '],
                [' 42944114 ',' 0 ',' 122019 '],
                [' 42944114 ',' 0 ',' 012020 '],
                [' 42944114 ',' 0 ',' 022020 '],
                [' 42944114 ',' 0 ',' 032020 '],
                [' 42944114 ',' 0 ',' 042020 '],
                [' 42944114 ',' 0 ',' 052020 '],
                [' 42944114 ',' 0 ',' 062020 '],
                [' 42944114 ',' 0 ',' 072020 '],
                [' 42944114 ',' 0 ',' 082020 '],
                [' 42944114 ',' 0 ',' 092020 '],
                [' 42944114 ',' 0 ',' 102020 '],
                [' 42944114 ',' 0 ',' 112020 '],
                [' 42944114 ',' 0 ',' 122020 '],
                [' 42944114 ',' 0 ',' 012021 '],
                [' 42944114 ',' 0 ',' 022021 '],
                [' 42944114 ',' 0 ',' 032021 '],
                [' 42944114 ',' 198 ',' 042021 '],
                [' 42944114 ',' 425 ',' 052021 '],
                [' 42944114 ',' 326 ',' 062021 '],
                [' 42944114 ',' 538 ',' 072021 '],
                [' 42944114 ',' 1684 ',' 082021 '],
                [' 42944114 ',' 1865 ',' 092021 '],
                [' 42944114 ',' 3435 ',' 102021 '],
                [' 42944114 ',' 1657 ',' 112021 '],
                [' 42944114 ',' 2306 ',' 122021 '],
                [' 42944114 ',' 1965 ',' 012022 '],
                [' 42944114 ',' 2213 ',' 022022 '],
                [' 42944114 ',' 2399 ',' 032022 '],
                [' 42944114 ',' 2682 ',' 042022 '],
                [' 42944114 ',' 2895 ',' 052022 '],
                [' 42944114 ',' 2924 ',' 062022 '],
                [' 42944114 ',' 3353 ',' 072022 '],
                [' 42944114 ',' 3284 ',' 082022 '],
                [' 42944114 ',' 3867 ',' 092022 '],
                [' 42944114 ',' 4130 ',' 102022 '],
                [' 42944114 ',' 3165 ',' 112022 '],
                [' 42944114 ',' 2685 ',' 122022 '],
                [' 42944114 ',' 2678 ',' 012023 '],
                [' 42944114 ',' 27280 ',' 022023 '],
                [' 42944114 ',' 482 ',' 032023 '],
                [' 42944114 ',' 2841 ',' 042023 '],
                [' 42944114 ',' 1434 ',' 052023 '],
                [' 21909386 ',' 0 ',' 072018 '],
                [' 21909386 ',' 0 ',' 082018 '],
                [' 21909386 ',' 0 ',' 092018 '],
                [' 21909386 ',' 0 ',' 102018 '],
                [' 21909386 ',' 0 ',' 112018 '],
                [' 21909386 ',' 0 ',' 122018 '],
                [' 21909386 ',' 0 ',' 012019 '],
                [' 21909386 ',' 0 ',' 022019 '],
                [' 21909386 ',' 0 ',' 032019 '],
                [' 21909386 ',' 0 ',' 042019 '],
                [' 21909386 ',' 0 ',' 052019 '],
                [' 21909386 ',' 0 ',' 062019 '],
                [' 21909386 ',' 0 ',' 072019 '],
                [' 21909386 ',' 0 ',' 082019 '],
                [' 21909386 ',' 0 ',' 092019 '],
                [' 21909386 ',' 0 ',' 102019 '],
                [' 21909386 ',' 0 ',' 112019 '],
                [' 21909386 ',' 0 ',' 122019 '],
                [' 21909386 ',' 0 ',' 012020 '],
                [' 21909386 ',' 0 ',' 022020 '],
                [' 21909386 ',' 0 ',' 032020 '],
                [' 21909386 ',' 0 ',' 042020 '],
                [' 21909386 ',' 0 ',' 052020 '],
                [' 21909386 ',' 0 ',' 062020 '],
                [' 21909386 ',' 0 ',' 072020 '],
                [' 21909386 ',' 0 ',' 082020 '],
                [' 21909386 ',' 0 ',' 092020 '],
                [' 21909386 ',' 0 ',' 102020 '],
                [' 21909386 ',' 0 ',' 112020 '],
                [' 21909386 ',' 0 ',' 122020 '],
                [' 21909386 ',' 0 ',' 012021 '],
                [' 21909386 ',' 0 ',' 022021 '],
                [' 21909386 ',' 0 ',' 032021 '],
                [' 21909386 ',' 0 ',' 042021 '],
                [' 21909386 ',' 0 ',' 052021 '],
                [' 21909386 ',' 0 ',' 062021 '],
                [' 21909386 ',' 0 ',' 072021 '],
                [' 21909386 ',' 0 ',' 082021 '],
                [' 21909386 ',' 0 ',' 092021 '],
                [' 21909386 ',' 0 ',' 102021 '],
                [' 21909386 ',' 0 ',' 112021 '],
                [' 21909386 ',' 689 ',' 122021 '],
                [' 21909386 ',' 588 ',' 012022 '],
                [' 21909386 ',' 853 ',' 022022 '],
                [' 21909386 ',' 1068 ',' 032022 '],
                [' 21909386 ',' 1373 ',' 042022 '],
                [' 21909386 ',' 1602 ',' 052022 '],
                [' 21909386 ',' 1624 ',' 062022 '],
                [' 21909386 ',' 1939 ',' 072022 '],
                [' 21909386 ',' 1899 ',' 082022 '],
                [' 21909386 ',' 2400 ',' 092022 '],
                [' 21909386 ',' 2589 ',' 102022 '],
                [' 21909386 ',' 1984 ',' 112022 '],
                [' 21909386 ',' 1683 ',' 122022 '],
                [' 21909386 ',' 1679 ',' 012023 '],
                [' 21909386 ',' 25344 ',' 022023 '],
                [' 21909386 ',' 448 ',' 032023 '],
                [' 21909386 ',' 2684 ',' 042023 '],
                [' 21909386 ',' 1355 ',' 052023 '],
                [' 53903541 ',' 0 ',' 072018 '],
                [' 53903541 ',' 0 ',' 082018 '],
                [' 53903541 ',' 0 ',' 092018 '],
                [' 53903541 ',' 0 ',' 102018 '],
                [' 53903541 ',' 0 ',' 112018 '],
                [' 53903541 ',' 0 ',' 122018 '],
                [' 53903541 ',' 0 ',' 012019 '],
                [' 53903541 ',' 0 ',' 022019 '],
                [' 53903541 ',' 0 ',' 032019 '],
                [' 53903541 ',' 0 ',' 042019 '],
                [' 53903541 ',' 0 ',' 052019 '],
                [' 53903541 ',' 0 ',' 062019 '],
                [' 53903541 ',' 0 ',' 072019 '],
                [' 53903541 ',' 0 ',' 082019 '],
                [' 53903541 ',' 0 ',' 092019 '],
                [' 53903541 ',' 0 ',' 102019 '],
                [' 53903541 ',' 0 ',' 112019 '],
                [' 53903541 ',' 0 ',' 122019 '],
                [' 53903541 ',' 0 ',' 012020 '],
                [' 53903541 ',' 0 ',' 022020 '],
                [' 53903541 ',' 0 ',' 032020 '],
                [' 53903541 ',' 0 ',' 042020 '],
                [' 53903541 ',' 0 ',' 052020 '],
                [' 53903541 ',' 0 ',' 062020 '],
                [' 53903541 ',' 0 ',' 072020 '],
                [' 53903541 ',' 0 ',' 082020 '],
                [' 53903541 ',' 0 ',' 092020 '],
                [' 53903541 ',' 0 ',' 102020 '],
                [' 53903541 ',' 0 ',' 112020 '],
                [' 53903541 ',' 0 ',' 122020 '],
                [' 53903541 ',' 0 ',' 012021 '],
                [' 53903541 ',' 0 ',' 022021 '],
                [' 53903541 ',' 0 ',' 032021 '],
                [' 53903541 ',' 0 ',' 042021 '],
                [' 53903541 ',' 0 ',' 052021 '],
                [' 53903541 ',' 0 ',' 062021 '],
                [' 53903541 ',' 0 ',' 072021 '],
                [' 53903541 ',' 0 ',' 082021 '],
                [' 53903541 ',' 0 ',' 092021 '],
                [' 53903541 ',' 0 ',' 102021 '],
                [' 53903541 ',' 0 ',' 112021 '],
                [' 53903541 ',' 618 ',' 122021 '],
                [' 53903541 ',' 527 ',' 012022 '],
                [' 53903541 ',' 705 ',' 022022 '],
                [' 53903541 ',' 1090 ',' 032022 '],
                [' 53903541 ',' 1820 ',' 042022 '],
                [' 53903541 ',' 2796 ',' 052022 '],
                [' 53903541 ',' 2889 ',' 062022 '],
                [' 53903541 ',' 3616 ',' 072022 '],
                [' 53903541 ',' 3542 ',' 082022 '],
                [' 53903541 ',' 4423 ',' 092022 '],
                [' 53903541 ',' 4817 ',' 102022 '],
                [' 53903541 ',' 3691 ',' 112022 '],
                [' 53903541 ',' 3132 ',' 122022 '],
                [' 53903541 ',' 3124 ',' 012023 '],
                [' 53903541 ',' 69809 ',' 022023 '],
                [' 53903541 ',' 1233 ',' 032023 '],
                [' 53903541 ',' 7036 ',' 042023 '],
                [' 53903541 ',' 3552 ',' 052023 '],
                [' 41973722 ',' 0 ',' 072018 '],
                [' 41973722 ',' 0 ',' 082018 '],
                [' 41973722 ',' 0 ',' 092018 '],
                [' 41973722 ',' 0 ',' 102018 '],
                [' 41973722 ',' 0 ',' 112018 '],
                [' 41973722 ',' 0 ',' 122018 '],
                [' 41973722 ',' 0 ',' 012019 '],
                [' 41973722 ',' 0 ',' 022019 '],
                [' 41973722 ',' 0 ',' 032019 '],
                [' 41973722 ',' 0 ',' 042019 '],
                [' 41973722 ',' 0 ',' 052019 '],
                [' 41973722 ',' 0 ',' 062019 '],
                [' 41973722 ',' 0 ',' 072019 '],
                [' 41973722 ',' 0 ',' 082019 '],
                [' 41973722 ',' 0 ',' 092019 '],
                [' 41973722 ',' 0 ',' 102019 '],
                [' 41973722 ',' 0 ',' 112019 '],
                [' 41973722 ',' 0 ',' 122019 '],
                [' 41973722 ',' 0 ',' 012020 '],
                [' 41973722 ',' 0 ',' 022020 '],
                [' 41973722 ',' 0 ',' 032020 '],
                [' 41973722 ',' 0 ',' 042020 '],
                [' 41973722 ',' 0 ',' 052020 '],
                [' 41973722 ',' 0 ',' 062020 '],
                [' 41973722 ',' 0 ',' 072020 '],
                [' 41973722 ',' 0 ',' 082020 '],
                [' 41973722 ',' 0 ',' 092020 '],
                [' 41973722 ',' 0 ',' 102020 '],
                [' 41973722 ',' 0 ',' 112020 '],
                [' 41973722 ',' 0 ',' 122020 '],
                [' 41973722 ',' 0 ',' 012021 '],
                [' 41973722 ',' 0 ',' 022021 '],
                [' 41973722 ',' 0 ',' 032021 '],
                [' 41973722 ',' 0 ',' 042021 '],
                [' 41973722 ',' 0 ',' 052021 '],
                [' 41973722 ',' 0 ',' 062021 '],
                [' 41973722 ',' 0 ',' 072021 '],
                [' 41973722 ',' 0 ',' 082021 '],
                [' 41973722 ',' 0 ',' 092021 '],
                [' 41973722 ',' 0 ',' 102021 '],
                [' 41973722 ',' 0 ',' 112021 '],
                [' 41973722 ',' 0 ',' 122021 '],
                [' 41973722 ',' 0 ',' 012022 '],
                [' 41973722 ',' 1833 ',' 022022 '],
                [' 41973722 ',' 2823 ',' 032022 '],
                [' 41973722 ',' 4973 ',' 042022 '],
                [' 41973722 ',' 7998 ',' 052022 '],
                [' 41973722 ',' 8375 ',' 062022 '],
                [' 41973722 ',' 11427 ',' 072022 '],
                [' 41973722 ',' 11193 ',' 082022 '],
                [' 41973722 ',' 17227 ',' 092022 '],
                [' 41973722 ',' 19457 ',' 102022 '],
                [' 41973722 ',' 14909 ',' 112022 '],
                [' 41973722 ',' 12649 ',' 122022 '],
                [' 41973722 ',' 12618 ',' 012023 '],
                [' 41973722 ',' 104797 ',' 022023 '],
                [' 41973722 ',' 1851 ',' 032023 '],
                [' 41973722 ',' 18956 ',' 042023 '],
                [' 41973722 ',' 9570 ',' 052023 '],
                [' 52496373 ',' 0 ',' 072018 '],
                [' 52496373 ',' 0 ',' 082018 '],
                [' 52496373 ',' 0 ',' 092018 '],
                [' 52496373 ',' 0 ',' 102018 '],
                [' 52496373 ',' 0 ',' 112018 '],
                [' 52496373 ',' 0 ',' 122018 '],
                [' 52496373 ',' 0 ',' 012019 '],
                [' 52496373 ',' 0 ',' 022019 '],
                [' 52496373 ',' 0 ',' 032019 '],
                [' 52496373 ',' 0 ',' 042019 '],
                [' 52496373 ',' 0 ',' 052019 '],
                [' 52496373 ',' 0 ',' 062019 '],
                [' 52496373 ',' 0 ',' 072019 '],
                [' 52496373 ',' 0 ',' 082019 '],
                [' 52496373 ',' 0 ',' 092019 '],
                [' 52496373 ',' 0 ',' 102019 '],
                [' 52496373 ',' 0 ',' 112019 '],
                [' 52496373 ',' 0 ',' 122019 '],
                [' 52496373 ',' 0 ',' 012020 '],
                [' 52496373 ',' 0 ',' 022020 '],
                [' 52496373 ',' 0 ',' 032020 '],
                [' 52496373 ',' 0 ',' 042020 '],
                [' 52496373 ',' 0 ',' 052020 '],
                [' 52496373 ',' 0 ',' 062020 '],
                [' 52496373 ',' 0 ',' 072020 '],
                [' 52496373 ',' 0 ',' 082020 '],
                [' 52496373 ',' 0 ',' 092020 '],
                [' 52496373 ',' 0 ',' 102020 '],
                [' 52496373 ',' 0 ',' 112020 '],
                [' 52496373 ',' 0 ',' 122020 '],
                [' 52496373 ',' 0 ',' 012021 '],
                [' 52496373 ',' 0 ',' 022021 '],
                [' 52496373 ',' 0 ',' 032021 '],
                [' 52496373 ',' 0 ',' 042021 '],
                [' 52496373 ',' 0 ',' 052021 '],
                [' 52496373 ',' 0 ',' 062021 '],
                [' 52496373 ',' 0 ',' 072021 '],
                [' 52496373 ',' 0 ',' 082021 '],
                [' 52496373 ',' 0 ',' 092021 '],
                [' 52496373 ',' 0 ',' 102021 '],
                [' 52496373 ',' 0 ',' 112021 '],
                [' 52496373 ',' 0 ',' 122021 '],
                [' 52496373 ',' 0 ',' 012022 '],
                [' 52496373 ',' 0 ',' 022022 '],
                [' 52496373 ',' 0 ',' 032022 '],
                [' 52496373 ',' 0 ',' 042022 '],
                [' 52496373 ',' 0 ',' 052022 '],
                [' 52496373 ',' 0 ',' 062022 '],
                [' 52496373 ',' 0 ',' 072022 '],
                [' 52496373 ',' 0 ',' 082022 '],
                [' 52496373 ',' 710 ',' 092022 '],
                [' 52496373 ',' 0 ',' 102022 '],
                [' 52496373 ',' 0 ',' 112022 '],
                [' 52496373 ',' 0 ',' 122022 '],
                [' 52496373 ',' 0 ',' 012023 '],
                [' 52496373 ',' 0 ',' 022023 '],
                [' 52496373 ',' 0 ',' 032023 '],
                [' 52496373 ',' 0 ',' 042023 '],
                [' 52496373 ',' 0 ',' 052023 '],
                [' 32205151 ',' 0 ',' 072018 '],
                [' 32205151 ',' 0 ',' 082018 '],
                [' 32205151 ',' 0 ',' 092018 '],
                [' 32205151 ',' 0 ',' 102018 '],
                [' 32205151 ',' 0 ',' 112018 '],
                [' 32205151 ',' 0 ',' 122018 '],
                [' 32205151 ',' 0 ',' 012019 '],
                [' 32205151 ',' 0 ',' 022019 '],
                [' 32205151 ',' 0 ',' 032019 '],
                [' 32205151 ',' 0 ',' 042019 '],
                [' 32205151 ',' 0 ',' 052019 '],
                [' 32205151 ',' 0 ',' 062019 '],
                [' 32205151 ',' 0 ',' 072019 '],
                [' 32205151 ',' 0 ',' 082019 '],
                [' 32205151 ',' 0 ',' 092019 '],
                [' 32205151 ',' 0 ',' 102019 '],
                [' 32205151 ',' 0 ',' 112019 '],
                [' 32205151 ',' 0 ',' 122019 '],
                [' 32205151 ',' 0 ',' 012020 '],
                [' 32205151 ',' 0 ',' 022020 '],
                [' 32205151 ',' 0 ',' 032020 '],
                [' 32205151 ',' 0 ',' 042020 '],
                [' 32205151 ',' 0 ',' 052020 '],
                [' 32205151 ',' 0 ',' 062020 '],
                [' 32205151 ',' 0 ',' 072020 '],
                [' 32205151 ',' 0 ',' 082020 '],
                [' 32205151 ',' 0 ',' 092020 '],
                [' 32205151 ',' 0 ',' 102020 '],
                [' 32205151 ',' 0 ',' 112020 '],
                [' 32205151 ',' 0 ',' 122020 '],
                [' 32205151 ',' 0 ',' 012021 '],
                [' 32205151 ',' 0 ',' 022021 '],
                [' 32205151 ',' 0 ',' 032021 '],
                [' 32205151 ',' 0 ',' 042021 '],
                [' 32205151 ',' 0 ',' 052021 '],
                [' 32205151 ',' 0 ',' 062021 '],
                [' 32205151 ',' 0 ',' 072021 '],
                [' 32205151 ',' 0 ',' 082021 '],
                [' 32205151 ',' 0 ',' 092021 '],
                [' 32205151 ',' 0 ',' 102021 '],
                [' 32205151 ',' 0 ',' 112021 '],
                [' 32205151 ',' 0 ',' 122021 '],
                [' 32205151 ',' 0 ',' 012022 '],
                [' 32205151 ',' 0 ',' 022022 '],
                [' 32205151 ',' 0 ',' 032022 '],
                [' 32205151 ',' 0 ',' 042022 '],
                [' 32205151 ',' 0 ',' 052022 '],
                [' 32205151 ',' 0 ',' 062022 '],
                [' 32205151 ',' 0 ',' 072022 '],
                [' 32205151 ',' 0 ',' 082022 '],
                [' 32205151 ',' 0 ',' 092022 '],
                [' 32205151 ',' 0 ',' 102022 '],
                [' 32205151 ',' 0 ',' 112022 '],
                [' 32205151 ',' 0 ',' 122022 '],
                [' 32205151 ',' 0 ',' 012023 '],
                [' 32205151 ',' 43995 ',' 022023 '],
                [' 32205151 ',' 777 ',' 032023 '],
                [' 32205151 ',' 4622 ',' 042023 '],
                [' 32205151 ',' 2334 ',' 052023 ']]

        for i in total:
            self.inserirAmarzenadoT(i[0],i[2],i[1],1,dist,cli)

    def valorGerador_Celesc(self,referencia, cli, uc=None):
        dic = {} 

        query = 'SELECT * FROM relatorios_gerador_celesc as r JOIN Geradores_geradores AS g   ON r.uc = g.uc'
        query += f' WHERE r.Referencia= {referencia}'
        query += f' AND r.cliente_id= {cli}'

        if uc != None: 
            query += f' AND r.uc= {uc}'

        cursor = connection.cursor()
        cursor.execute(query)
        r = cursor.fetchall()[0]


        dic['uc'] = r[1]
        dic['nome'] = r[24]
        dic['referencia'] = r[3]
        dic['fatura'] = r[2]
        dic['geracaoPT'] = r[6]
        dic['geracaoFP'] = r[7]
        dic['consumoPT'] = r[8]
        dic['consumoFP'] = r[9]
        dic['acumulado'] = r[13]

        if r[20] != 0:
            dic['imposto'] = 100-int(str(r[20]).replace('.',''))
        else:
            dic['imposto'] = 1

        if r[21] != 0:
            dic['descontoCli'] = 100-r[21]
        else:
            dic['descontoCli'] = 1
        
        if r[22] != 0:
            dic['descontoGest'] = 100-r[22]
        else:
            dic['descontoGest'] = 1

        injetada = int(r[6])-int(r[8])
        if injetada <0:
            injetada=0

        if int(r[7]) > 0 :

            acrescimo = int(r[7])-int(r[9])
            if acrescimo <0:
                acrescimo=0

            injetada = (injetada*1.62)+acrescimo
        
        dic['injetada'] = injetada

        return dic

    def Armazenamento_Celesc(self,cli,dist):

        self.insere_mensal_anterior(cli,dist)
        self.insere_total_anterior(cli,dist)

        tamanho_gerado = self.Conta_gerados_celesc()
        tamanho = self.Conta_ArmazenadosM()

        dif = tamanho_gerado-tamanho

        Ref = self.Lista_ref(dif)
        und= self.ucs_Celesc(cli)

        mensal = self.ArmMensalTodos(dist,'042023')
        total = self.ArmTotalTodos(dist,'042023')

        t=[]
        m=[]
        for me,to in zip(mensal,total):
            t.append(int(to[2]))
            m.append(int(me[2]))

        for i in range(len(und)-len(m)):
            t.append(0)
            m.append(0)

        mensal = [m]
        total = [t]
        for ref in Ref:
            valor = []
            x=0
            for uc in und:

                RefAn = self.ReferenciaAnterior(ref)

                try:
                    SaldoFinalAn = int(self.SaldoFinalCli_Celesc(RefAn,cli))#GJ48
                except:
                    SaldoFinalAn = 0

                try:
                    SaldoFinal = int(self.SaldoFinalCli_Celesc(ref,cli))#GJ49
                except:
                    SaldoFinal = 0

                try:
                    injetada = int(self.InjetadaInd_Celesc(uc,cli, ref))#BF49
                except:
                    injetada = 0
                try:
                    injetadatotal = int(self.InjecaoTotal_Celesc(ref,cli))#SOMA INJ
                except:
                    injetadatotal = 0
                

                if SaldoFinal > SaldoFinalAn:
                    
                    arm = int((SaldoFinal-SaldoFinalAn)*(injetada/injetadatotal))
                    valor.append(arm)
                    
                else:
                    try:
                        totalAnt = total[-1]
                    except:
                        totalAnt = total

                    try:
                        arm = int((SaldoFinal-SaldoFinalAn)*(totalAnt[x]/sum(total[-1])))
                    except:
                        arm = 0
                
                    valor.append(arm)
                x+=1
            mensal.append(valor)

            repo = []
            for v,t in zip(mensal[-1],total[-1]):
                repo.append(int(v)+int(t))
            total.append(repo)

        repo = []
        for r,p in zip(Ref[::-1],total[::-1]):
            v=[]
            v.append(r)
            for valor in p:
                v.append(valor)
            repo.append(tuple(v))
        total = tuple(repo)

        repo = []
        for r,p in zip(Ref[::-1],mensal[::-1]):
            v=[]
            v.append(r)
            for valor in p:
                v.append(valor)
            repo.append(tuple(v))
        mensal = tuple(repo)

        for valor in mensal:
            for uc,v in zip(und,valor[1:]):
                self.inserirAmarzenadoM(uc,valor[0],v,1,dist,cli)
        
        for valor in total:
            for uc,v in zip(und,valor[1:]):
                self.inserirAmarzenadoT(uc,valor[0],v,1,dist,cli)

        return mensal,total
 
    def trata_lista(self,lista,dist):

        if dist =='1':
            und = self.ucs()
        elif dist =='2':
            und = self.ucs_Celesc()


        for i in range(len(und)-(len(lista)-1)):
            lista.append(0)

        return lista

    def agrega_lista(self,tupla,dist):
        
        lista = []

        if dist =='1':
            ref = self.Referencias()
        elif dist =='2':
            ref = self.Referencias_Celesc()

        repositorio = []
        for i in ref:
            repo = []
            repo.append(i)
            for valor in tupla:
                if i == valor[1] and valor not in repositorio:
                    repo.append(int(valor[2]))
                    repositorio.append(valor)
                
            repo = self.trata_lista(repo,dist)
            lista.append(repo)

        return lista

    def InjetadaInd_Celesc(self,uc,cli,ref=None):
        query = f' SELECT Energia_Injetada,Energia_Ativa,Energia_InjetadaFP,Energia_AtivaFP FROM relatorios_gerador_celesc WHERE uc= {uc} ' 
        query += f' AND cliente_id= {cli} '

        if ref != None: 
            query += f' AND referencia= {ref} '

        cursor = connection.cursor()
        cursor.execute(query)

        r = cursor.fetchall()[0]

        injetada = int(r[0])-int(r[1])
        if injetada <0:
            injetada=0

        if int(r[2]) > 0 :

            acrescimo = int(r[2])-int(r[3])
            if acrescimo <0:
                acrescimo=0

            injetada = (injetada*1.62)+acrescimo

        return injetada

    def InjecaoTotal_Celesc(self,referencia,cli):

        query = ' SELECT Energia_Injetada, Energia_Ativa, Energia_InjetadaFP,Energia_AtivaFP '
        query += f' FROM relatorios_gerador_celesc  WHERE referencia= {referencia}'
        query += f' AND cliente_id= {cli} '

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        lista = []
        for i in resultado:

            injetada = int(i[0])-int(i[1])
            if injetada <0:
                injetada=0

            if int(i[2]) > 0 :
                acrescimo = int(i[2])-int(i[3])
                if acrescimo <0:
                    acrescimo=0

                injetada = (injetada*1.62)+acrescimo

            if injetada > 0:

                lista.append(injetada)
        
        resultado =sum(lista)

        return resultado

    def Injecao_Celesc(self,cli):

        query = ' SELECT Energia_Injetada, Energia_Ativa, Energia_InjetadaFP,Energia_AtivaFP,uc,Referencia '
        query += f' FROM relatorios_gerador_celesc '
        query += f' WHERE cliente_id= {cli} '

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        lista = []
        for i in resultado:
            repo = []
            injetada = int(i[0])-int(i[1])
            if injetada <0:
                injetada=0

            if int(i[2]) > 0 :
                acrescimo = int(i[2])-int(i[3])
                if acrescimo <0:
                    acrescimo=0

                injetada = (injetada*1.62)+acrescimo

            if injetada > 0:

                repo.append(i[4])
                repo.append(i[5])
                repo.append(injetada)
            else:
                repo.append(i[4])
                repo.append(i[5])
                repo.append(0)
        
            lista.append(tuple(repo))

        r = tuple(lista)

        

        return r

    def SaldoFinalCli_Celesc(self,referencia,cli):

        query = f'SELECT SUM(Saldo_Final) FROM relatorios_azul_celesc a WHERE Referencia= {referencia}'
        query += f' AND cliente_id= {cli}'
        query += f' AND admin_id= 1'

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()[0][0]

        return resultado

    def Geracao_Celesc(self,referencia=None):
        query = ' SELECT uc,Referencia,Energia_Injetada FROM relatorios_gerador_celesc '

        if referencia != None: 
            query += f' WHERE referencia= {referencia}'

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        return resultado

    def consumoGd_Celesc(self,referencia=None):
        query = ' SELECT uc,Referencia,Energia_Ativa FROM relatorios_gerador_celesc '

        if referencia != None: 
            query += f' WHERE referencia= {referencia}'

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        return resultado

    def CredCompensado_Celesc(self,referencia,cli):

        query = f'SELECT '
        query += f'  SUM(MptTEQtd) + SUM(MptQtd) + SUM(OptTEQtd) + SUM(OptQtd) + SUM(PtMptTEQtd) + SUM(PtMptTUSDQtd) '
        query += f' FROM '
        query += f' relatorios_consumidor_celesc ' 
        query += f' WHERE '
        query += f' referencia = {referencia} '
        query += f' AND cliente_id= {cli}'
        query += f' AND admin_id=2'
        cursor = connection.cursor()
        cursor.execute(query)
        resultado = cursor.fetchall()[0][0]

        if resultado == None:
            resultado = 0

        query = f'SELECT '
        query += f'  SUM(MptTEQtd) + SUM(MptQtd) + SUM(OptTEQtd) + SUM(OptQtd) + SUM(PtMptTEQtd) + SUM(PtMptTUSDQtd) '
        query += f' FROM '
        query += f' relatorios_consumidor_celesc ' 
        query += f' WHERE '
        query += f' referencia = {referencia} '
        query += f' AND cliente_id= {cli}'
        cursor = connection.cursor()
        cursor.execute(query)
        total = cursor.fetchall()[0][0]

        resultado = total-resultado

        return resultado

    def CredBruto_Celesc(self,referencia,cli):
 
        query = f'SELECT '
        query += f'  SUM(MptTEValor) + SUM(MptTUSDValor) + SUM(MptValor) + SUM(OptTEValor) + SUM(OptTUSDValor) + SUM(OptValor) + SUM(PtMptTUSDValor) + SUM(PtMptValor) + SUM(FpMptTEValor) + SUM(FpMptTUSDValor) + SUM(FpMptValor) '
        query += f' FROM '
        query += f' relatorios_consumidor_celesc ' 
        query += f' WHERE '
        query += f' referencia = {referencia} '
        query += f' AND cliente_id= {cli}'
        query += f' AND status=1'
        query += f' AND admin_id=2'
        cursor = connection.cursor()
        cursor.execute(query)
        resultado = cursor.fetchall()[0][0]

        if resultado == None:
            resultado = 0
        #90428.02 encanto
        #208834.77 total
        #13.724,85  geradores
        #

        query = f'SELECT '
        query += f'  SUM(MptTEValor) + SUM(MptTUSDValor) + SUM(MptValor) + SUM(OptTEValor) + SUM(OptTUSDValor) + SUM(OptValor) + SUM(PtMptTUSDValor) + SUM(PtMptValor) + SUM(FpMptTEValor) + SUM(FpMptTUSDValor) + SUM(FpMptValor) '
        query += f' FROM '
        query += f' relatorios_consumidor_celesc ' 
        query += f' WHERE '
        query += f' referencia = {referencia} '
        query += f' AND cliente_id= {cli}'
        query += f' AND status=1'
        cursor = connection.cursor()
        cursor.execute(query)
        total = cursor.fetchall()[0][0]

        return total-resultado
    
    def SomaArm(self,tupla):
        lista = []
        for i in tupla:
            valor = self.TrasformaemvalorUnit(i[2])
            lista.append(valor)
        
        resultado = sum(lista)

        return resultado

    def splitConsumo_Celesc(self,referencia,uc,cli,dist):
        
        injTotal = self.InjecaoTotal_Celesc(referencia,cli)
        injTotal = self.TrasformaemvalorUnit(injTotal)

        credComp = self.CredCompensado_Celesc(referencia,cli)
        credComp = self.TrasformaemvalorUnit(credComp)

        injetado = self.InjetadaInd_Celesc(uc,cli,referencia)

        armT = self.ArmTotal(referencia,uc,cli,dist)
        armT = self.TrasformaemvalorUnit(armT)

        armTtdos = self.SomaArm(self.ArmTotalTodos(dist, referencia))
        armTtdos = self.TrasformaemvalorUnit(armTtdos)

        """ print()
        print(uc)
        print('injTotal ------',injTotal)
        print('credComp ------',credComp)
        print('injetado ------',injetado)
        print('armT -------',armT)
        print('armTtdos --------',armTtdos)
        print()
        print() """

        split = (injTotal/credComp)*(credComp*(injetado/injTotal))

        if credComp > injTotal:
            adicional = (credComp-injTotal)*(armT/armTtdos)
            split = split+adicional

        return split
    
    def SomaSplit_Celesc(self,referencia,cli,dist):

        lista = []
        unds = self.ucs_Celesc(cli)
        for i in unds:
            lista.append(self.splitConsumo_Celesc(referencia,i,cli,dist))
        
        return sum(lista)
    


# ------------RELATORIO GERADOR COPEL-------------------

    def RelatorioGerador(self,uc=None):
        
        query = ' SELECT Referencia,Energia_Ativa,Energia_Injetada,Energia_Injetada-Energia_Ativa,Saldo_Final FROM relatorios_gerador '

        if uc != None: 
            query += f' WHERE uc= {uc}'

        cursor = connection.cursor()
        cursor.execute(query)
        resultado = cursor.fetchall()

        lista = []
        for i in resultado:
            if i[3] < 0:
                valor = 0
            else:
                valor = i[3]
            lista.append([i[0],i[1],i[2],int(valor),i[4]])

        return lista

    def RelatorioGerador_Celesc(self,uc=None):
        
        query = ' SELECT Referencia,Energia_Ativa,Energia_Injetada,Energia_AtivaFp,Energia_InjetadaFP,Saldo_Final FROM relatorios_gerador_celesc '

        if uc != None: 
            query += f' WHERE uc= {uc}'

        cursor = connection.cursor()
        cursor.execute(query)
        resultado = cursor.fetchall()


        lista = []
        for r in resultado:

            injetada = int(r[2])-int(r[1])
            if injetada <0:
                injetada=0

            if int(r[3]) > 0 :

                acrescimo = int(r[4])-int(r[3])
                if acrescimo <0:
                    acrescimo=0

                injetada = (injetada*1.62)+acrescimo
                
            lista.append([r[0],r[1],r[2],r[3],r[4],injetada,r[5]])

        return lista
    
    def RelatorioGerador_mensal(self,uc,dist):
        
        query = ' SELECT valor FROM relatorios_ArmazenamentoMensal '
        query += f' WHERE distribuidora_id= {dist}'
        if uc != None: 
            query += f' AND uc= {uc}'

        cursor = connection.cursor()
        cursor.execute(query)
        resultado = cursor.fetchall()

        lista = []
        for i in resultado:
            lista.append(i[0])

        return lista

    def RelatorioGerador_total(self,uc,dist):
        
        query = ' SELECT valor FROM relatorios_armazenamentototal '
        query += f' WHERE distribuidora_id= {dist}'

        if uc != None: 
            query += f' AND uc= {uc}'

        cursor = connection.cursor()
        cursor.execute(query)
        resultado = cursor.fetchall()

        lista = []
        for i in resultado:
            lista.append(i[0])

        return lista
    
    def Atualiza_liberado_copel(self,ref,status):
        
        query = f'UPDATE relatorios_gerador SET liberado ={status} '
        query += f' WHERE Referencia= {ref}'

        cursor = connection.cursor()
        cursor.execute(query)
        cursor.fetchone()
    
    def Atualiza_liberado_celesc(self,ref,status):
        
        query = f'UPDATE relatorios_gerador_celesc SET liberado ={status} '
        query += f' WHERE Referencia= {ref}'

        cursor = connection.cursor()
        cursor.execute(query)
        cursor.fetchone()
    
    def SelecionaHistorico(self,ref, uc=None):
        dic = {} 
        query = ' SELECT * FROM relatorios_historico '

        if uc != None: 
            query += f' WHERE Referencia= {ref}'
            query += f' AND uc= {uc}'

        cursor = connection.cursor()
        cursor.execute(query)
        r = cursor.fetchall()[0]

        print(r)

        dic['valorBruto'] = r[3]
        dic['CompensadoMes'] = r[4]
        dic['UnitBruto'] = r[11]
        dic['faturaGerador'] = r[5]
        dic['UnitFatura'] = r[12]    
        dic['descontoCliente'] = r[6]
        dic['UnitCliente'] = r[7]
        dic['descontoGestao'] = r[8]
        dic['UnitGestao'] = r[9]
        dic['descontoImposto']= r[10]
        dic['ValorFinal'] = dic['descontoImposto']
        
        return dic
