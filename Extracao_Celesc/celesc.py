from django.db import connection
from collections import defaultdict

 
class Celesc:

    def PegaPosicao(self,texto):
        repositorio = []

        for i in range(len(texto)):

            if texto[i]['text'] == 'CONSUMO':
            
                nome = texto[i]['text']+texto[i+1]['text']
                nome = self.TrataNome(nome)
                
                repositorio.append(self.passaNome(texto, i, nome))

            if texto[i]['text'] == 'MPT':
                
                nome = texto[i-3]['text']+texto[i-2]['text']+texto[i-1]['text']+texto[i]['text']
                nome = self.TrataNome(nome)
                
                repositorio.append(self.passaNome(texto, i, nome))

            if texto[i]['text'] == 'OPT':
                
                nome = texto[i-3]['text']+texto[i-2]['text']+texto[i-1]['text']+texto[i]['text']
                nome = self.TrataNome(nome)

                repositorio.append(self.passaNome(texto, i, nome))
            
            if texto[i]['text'] == 'MUNICIPAL':

                nome = texto[i-1]['text']+texto[i]['text']
                nome = self.TrataNome(nome)

                repositorio.append(self.passaNome(texto, i, nome))
            
            if texto[i]['text'] == 'AJUSTE':

                nome = texto[i]['text']+texto[i+1]['text']
                nome = self.TrataNome(nome)
        
                repositorio.append(self.passaNome(texto, i, nome))

            if texto[i]['text'] == 'DEMANDA':
                nome = texto[i]['text']+texto[i+1]['text']
                nome = self.TrataNome(nome)

                repositorio.append(self.passaNome(texto, i, nome))
            
            if texto[i]['text'] == 'ENERGIA':

                nome = texto[i]['text']+texto[i+1]['text']
                nome = self.TrataNome(nome)
                
                repositorio.append(self.passaNome(texto, i, nome))

            if texto[i]['text'] == 'DEV.':

                nome = texto[i]['text']+texto[i+1]['text']+texto[i+2]['text']+texto[i+3]['text']
                nome = self.TrataNome(nome)

                repositorio.append(self.passaNome(texto, i, nome))

            if texto[i]['text'] == 'JUROS':

                nome = texto[i]['text']+texto[i+2]['text']
                nome = self.TrataNome(nome)
                repositorio.append(self.passaNome(texto, i, nome))
            
            if texto[i]['text'] == 'MULTA':

                nome = texto[i]['text']+texto[i+2]['text']
                nome = self.TrataNome(nome)

                repositorio.append(self.passaNome(texto, i, nome))

            if texto[i]['text'] == 'SISTEMA':

                nome = texto[i-2]['text']+texto[i-1]['text']+texto[i]['text']
                nome = self.TrataNome(nome)
                repositorio.append(self.passaNome(texto, i, nome))

            if texto[i]['text'] == 'CONTINUIDADE':

                nome = texto[i-3]['text']+texto[i-2]['text']+texto[i-1]['text']+texto[i]['text']
                nome = self.TrataNome(nome)
                
                repositorio.append(self.passaNome(texto, i, nome))

            if texto[i]['text'] == 'ANTERIOR':

                nome = texto[i-2]['text']+texto[i-1]['text']+texto[i]['text']
                nome = self.TrataNome(nome)

                repositorio.append(self.passaNome(texto, i, nome))

            if texto[i]['text'] == 'DUPLICIDADE.':

                nome = texto[i-1]['text']+texto[i]['text']
                nome = self.TrataNome(nome)

                repositorio.append(self.passaNome(texto, i, nome))

            if texto[i]['text'] == 'DEVOLUCAO':

                nome = texto[i]['text']+texto[i+1]['text']+texto[i+2]['text']+texto[i+3]['text']+texto[i+4]['text']
                nome = self.TrataNome(nome)

                repositorio.append(self.passaNome(texto, i, nome))
            
            #------------------ TRIBUTOS --------------------#

            if texto[i]['text'] == 'ICMS':
                
                nome = texto[i]['text']+texto[i-1]['text']
                nome = self.TrataNome(nome)
                
                
                repositorio.append(self.passaNome(texto, i, nome))
            
            if texto[i]['text'] == 'COFINS':
            
                nome = texto[i]['text']+texto[i+1]['text']
                nome = self.TrataNome(nome)
                
                repositorio.append(self.passaNome(texto, i, nome))
            
            if texto[i]['text'] == 'PIS':
            
                nome = texto[i]['text']+texto[i+1]['text']
                nome = self.TrataNome(nome)
                
                repositorio.append(self.passaNome(texto, i, nome))
        
        return repositorio

    def CorrigeDic(self, lista):

        todos = []
        nenhum = []
        te = []
        tusd = []

        for dicionario in lista:
            try:
            
                if not 'te' in dicionario and  not 'tusd' in dicionario:
                    nenhum.append(dicionario)
                
                if 'te' in dicionario and  'tusd' in dicionario:
                    todos.append(dicionario)
                
                if 'te' in dicionario and  not 'tusd' in dicionario:
                    te.append(dicionario)
                
                if 'tusd' in dicionario and  not 'te' in dicionario:
                    tusd.append(dicionario)
            
            except:
                pass
        
        repositoriotusd = []
        for i in tusd:
            repositoriotusd.append(i['nome'])
        
        repositoriote = []
        for i in te:
            repositoriote.append(i['nome'])
        
        repositorionenhum = []
        for i in nenhum:
            repositorionenhum.append(i['nome'])
        
        repositoriotodos = []
        for i in todos:
            repositoriotodos.append(i['nome'])
        
        
        tusd = self.SomaListas(repositoriotusd,tusd)
        te = self.SomaListas(repositoriote,te)
        nenhum = self.SomaListas(repositorionenhum,nenhum)
        todos = self.SomaListas(repositoriotodos,todos)

        return [todos, tusd, te, nenhum]
    
    def SomaListas(self,tipo,lista):

        repositorio = []
        repositorio_unico = []
        valores = []

        keys = defaultdict(list)
        for key, value in enumerate(tipo):

            keys[value].append(key)

        for value in keys:
            if len(keys[value]) > 1:
                repositorio.append([value, keys[value]])

        for i in repositorio:
            gaveta = []
            for valor in i[1]:
                gaveta.append(lista[valor])
        
            valores.append(self.SomaDicionario(i[0], gaveta))        
        
        for value in keys:
            if len(keys[value]) == 1:
                repositorio_unico.append([value, keys[value]])

        for i in repositorio_unico:
            gaveta = []
            for valor in i[1]:
                gaveta.append(lista[valor])
            
        
            valores.append(self.SomaDicionario(i[0], gaveta))

        return valores

    def SomaDicionario(self,nome, lista):

        dic = {}
        nome = nome
        
        tamanho = len(lista)
        
        if 'qtd' in lista[0]:
            qtd = sum(sub['qtd'] for sub in lista)

        if 'te' in lista[0]:
            te = sum(sub['te'] for sub in lista)/ tamanho 
        
        if 'tusd' in lista[0]:
            tusd = sum(sub['tusd'] for sub in lista)/ tamanho 

        if 'valor' in lista[0]:
            valor = sum(sub['valor'] for sub in lista)

        if 'baseCalc' in lista[0]:
            baseCalc = sum(sub['baseCalc'] for sub in lista)

        if 'aliquota' in lista[0]:
            aliquota = sum(sub['aliquota'] for sub in lista)

        if 'valorTributo' in lista[0]:
            valorTributo = sum(sub['valorTributo'] for sub in lista) 


        dic['nome'] = nome

        if 'baseCalc' in lista[0]:
            dic['baseCalc'] = baseCalc
        
        if 'aliquota' in lista[0]:
            dic['aliquota'] = round(aliquota,2)
        
        if 'valorTributo' in lista[0]:
            dic['valorTributo'] = round(valorTributo,2)

        if 'te' in lista[0]:
            dic['te'] = round(te,6)

        if 'tusd' in lista[0]:
            dic['tusd'] = round(tusd,6)
        
        if 'qtd' in lista[0]:
            dic['qtd'] = qtd

        if 'valor' in lista[0]:
            dic['valor'] = round(valor,2)

        return dic
 
    def Tratalista(self,lista):
        repositorio = []

        for i in lista:
            for valor in i: 
                repositorio.append(valor)
        
        return repositorio

    def distribuiDic(self, dicionario):

        dic = {}
        for tipo in dicionario:
            
            if tipo['nome'] == 'CONSUMO':
                
                dic['ConsumoQtd'] = tipo['qtd']
                dic['ConsumoTe'] = tipo['te']
                dic['ConsumoTusd'] = tipo['tusd']
                dic['ConsumoValor'] = tipo['valor']

            if tipo['nome'] == 'CONSUMOPONTA':

                dic['ConsumoPontaQtd'] = tipo['qtd']
                dic['ConsumoPontaTe'] = tipo['te']
                dic['ConsumoPontaTusd'] = tipo['tusd']
                dic['ConsumoPontaValor'] = tipo['valor']

            if tipo['nome'] == 'CONSUMOFORA':
                
                dic['ConsumoForaPontaQtd'] = tipo['qtd']
                dic['ConsumoForaPontaTe'] = tipo['te']
                dic['ConsumoForaPontaTusd'] = tipo['tusd']
                dic['ConsumoForaPontaValor'] = tipo['valor']

            if tipo['nome'] == 'ENERINJOUCMPT':

                if 'te' in tipo and not 'tusd' in tipo:
                    
                    dic['MptTEQtd'] = tipo['qtd']
                    dic['MptTETe'] = tipo['te']
                    dic['MptTEValor'] = tipo['valor']

                elif 'tusd' in tipo and not 'te' in tipo:
                    
                    dic['MptTUSDQtd'] = tipo['qtd']
                    dic['MptTUSDTusd'] = tipo['tusd']
                    dic['MptTUSDValor'] = tipo['valor']

                elif 'tusd' in tipo and 'te' in tipo:
                    
                    dic['MptQtd'] = tipo['qtd']
                    dic['MptTe'] = tipo['te']
                    dic['MptTusd'] = tipo['tusd']
                    dic['MptValor'] = tipo['valor']

            if tipo['nome'] == 'ENERINJOUCOPT':
                
                if 'te' in tipo and not 'tusd' in tipo:
                    
                    dic['OptTEQtd'] = tipo['qtd']
                    dic['OptTETe'] = tipo['te']
                    dic['OptTEValor'] = tipo['valor']

                elif 'tusd' in tipo and not 'te' in tipo:
                    
                    dic['OptTUSDQtd'] = tipo['qtd']
                    dic['OptTUSDTusd'] = tipo['tusd']
                    dic['OptTUSDValor'] = tipo['valor']

                elif 'tusd' in tipo and 'te' in tipo:
                    
                    dic['OptQtd'] = tipo['qtd']
                    dic['OptTe'] = tipo['te']
                    dic['OptTusd'] = tipo['tusd']
                    dic['OptValor'] = tipo['valor']

            if tipo['nome'] == 'INJPTOUCMPT':
                
                if 'te' in tipo and not 'tusd' in tipo:
                    
                    dic['PtMptTEQtd'] = tipo['qtd']
                    dic['PtMptTETe'] = tipo['te']
                    dic['PtMptTEValor'] = tipo['valor']

                elif 'tusd' in tipo and not 'te' in tipo:
                    
                    dic['PtMptTUSDQtd'] = tipo['qtd']
                    dic['PtMptTUSDTusd'] = tipo['tusd']
                    dic['PtMptTUSDValor'] = tipo['valor']

                elif 'tusd' in tipo and 'te' in tipo:
                    
                    dic['PtMptQtd'] = tipo['qtd']
                    dic['PtMptTe'] = tipo['te']
                    dic['PtMptTusd'] = tipo['tusd']
                    dic['PtMptValor'] = tipo['valor']

            if tipo['nome'] == 'INJFPOUCMPT':
                
                if 'te' in tipo and not 'tusd' in tipo:
                    
                    dic['FpMptTEQtd'] = tipo['qtd']
                    dic['FpMptTETe'] = tipo['te']
                    dic['FpMptTEValor'] = tipo['valor']

                elif 'tusd' in tipo and not 'te' in tipo:
                    
                    dic['FpMptTUSDQtd'] = tipo['qtd']
                    dic['FpMptTUSDTusd'] = tipo['tusd']
                    dic['FpMptTUSDValor'] = tipo['valor']

                elif 'tusd' in tipo and 'te' in tipo:
                    
                    dic['FpMptQtd'] = tipo['qtd']
                    dic['FpMptTe'] = tipo['te']
                    dic['FpMptTusd'] = tipo['tusd']
                    dic['FpMptValor'] = tipo['valor']

            if tipo['nome'] == 'COSIPMUNICIPAL':
                
                dic['CosipValor'] = tipo['valor']

            if tipo['nome'] == 'DEMANDA':

                if 'te' in tipo and not 'tusd' in tipo:
                    
                    dic['DemandaTEQtd'] = tipo['qtd']
                    dic['DemandaTETe'] = tipo['te']
                    dic['DemandaTEValor'] = tipo['valor']

                elif 'tusd' in tipo and not 'te' in tipo:
                    
                    dic['DemandaTUSDQtd'] = tipo['qtd']
                    dic['DemandaTUSDTusd'] = tipo['tusd']
                    dic['DemandaTUSDValor'] = tipo['valor']

                elif 'tusd' in tipo and 'te' in tipo:
                    
                    dic['DemandaQtd'] = tipo['qtd']
                    dic['DemandaTe'] = tipo['te']
                    dic['DemandaTusd'] = tipo['tusd']
                    dic['DemandaValor'] = tipo['valor']

            if tipo['nome'] == 'DEMANDAISENTA':
                
                if 'te' in tipo and not 'tusd' in tipo:
                    
                    dic['DemandaIsentTEQtd'] = tipo['qtd']
                    dic['DemandaIsentTETe'] = tipo['te']
                    dic['DemandaIsentTEValor'] = tipo['valor']

                elif 'tusd' in tipo and not 'te' in tipo:
                    
                    dic['DemandaIsentTUSDQtd'] = tipo['qtd']
                    dic['DemandaIsentTUSDTusd'] = tipo['tusd']
                    dic['DemandaIsentTUSDValor'] = tipo['valor']

                elif 'tusd' in tipo and 'te' in tipo:
                    
                    dic['DemandaIsentQtd'] = tipo['qtd']
                    dic['DemandaIsentTe'] = tipo['te']
                    dic['DemandaIsentTusd'] = tipo['tusd']
                    dic['DemandaIsentValor'] = tipo['valor']

            if tipo['nome'] == 'ENERGIAREAT':
                
                if 'te' in tipo and not 'tusd' in tipo:
                    
                    dic['EnergiaReatTEQtd'] = tipo['qtd']
                    dic['EnergiaReatTETe'] = tipo['te']
                    dic['EnergiaReatTEValor'] = tipo['valor']

                elif 'tusd' in tipo and not 'te' in tipo:
                    
                    dic['EnergiaReatTUSDQtd'] = tipo['qtd']
                    dic['EnergiaReatTUSDTusd'] = tipo['tusd']
                    dic['EnergiaReatTUSDValor'] = tipo['valor']

                elif 'tusd' in tipo and 'te' in tipo:
                    
                    dic['EnergiaReatQtd'] = tipo['qtd']
                    dic['EnergiaReatTe'] = tipo['te']
                    dic['EnergiaReatTusd'] = tipo['tusd']
                    dic['EnergiaReatValor'] = tipo['valor']

            if tipo['nome'] == 'AJUSTECONSUANTERIOR':
                
                dic['AjusteConsuAnteriorValor'] = tipo['valor']
                
            if tipo['nome'] == 'DEVOLUCAODEAJUSTEDEFATURAMENTO':
                
                dic['DevolucaoAjusteFaturamentoValor'] = tipo['valor']

            if tipo['nome'] == 'JUROSANTERIOR':
                
                dic['JurosAnteriorValor'] = tipo['valor']

            if tipo['nome'] == 'DEVJUROSAJUSTEFATURAMENTO':
                
                dic['DevJurosFaturamentoValor'] = tipo['valor']

            if tipo['nome'] == 'MULTAANTERIOR':
                
                dic['MultaContaAnteriorValor'] = tipo['valor']

            if tipo['nome'] == 'CUSTODISPSISTEMA':
                
                if 'te' in tipo and not 'tusd' in tipo:
                    
                    dic['DispSistemaTEQtd'] = tipo['qtd']
                    dic['DispSistemaTETe'] = tipo['te']
                    dic['DispSistemaTEValor'] = tipo['valor']

                elif 'tusd' in tipo and not 'te' in tipo:
                    
                    dic['DispSistemaTUSDQtd'] = tipo['qtd']
                    dic['DispSistemaTUSDTusd'] = tipo['tusd']
                    dic['DispSistemaTUSDValor'] = tipo['valor']

                elif 'tusd' in tipo and 'te' in tipo:
                    
                    dic['DispSistemaQtd'] = tipo['qtd']
                    dic['DispSistemaTe'] = tipo['te']
                    dic['DispSistemaTusd'] = tipo['tusd']
                    dic['DispSistemaValor'] = tipo['valor']

            if tipo['nome'] == 'DEVOLPAGADUPLICIDADE':
                
                dic['DevPagaDuplicidadeValor'] = tipo['valor']

            if tipo['nome'] == 'COMPVIOLMETACONTINUIDADE':
                
                dic['ViolMetaContinuidadeValor'] = tipo['valor']

            if tipo['nome'] == 'DEVCREDITOMESANTERIOR':
                
                dic['DevCreditoMesAnteriorValor'] = tipo['valor']
            
            if tipo['nome'] == 'ICMSV':
                
                dic['IcmsBaseCalc'] = tipo['baseCalc']
                dic['IcmsAliquota'] = tipo['aliquota']
                dic['IcmsValorTributo'] = tipo['valorTributo']

            if tipo['nome'] == 'COFINS':
                
                dic['CofinsBaseCalc'] = tipo['baseCalc']
                dic['CofinsAliquota'] = tipo['aliquota']
                dic['CofinsValorTributo'] = tipo['valorTributo']

            if tipo['nome'] == 'PIS':
                
                dic['PisBaseCalc'] = tipo['baseCalc']
                dic['PisAliquota'] = tipo['aliquota']
                dic['PisValorTributo'] = tipo['valorTributo']


        dic = self.completaDic(dic)

        return dic

    def PegaUC(self, texto):

        repositorio = {}

        for i in range(len(texto)):

            if texto[i]['text'] == 'UC:':
            
                nome = texto[i+1]['text']
                
                repositorio['uc'] = nome
            
            if 'Fatura:' in texto[i]['text']:
            
                nome = texto[i]['text']
                nome = str(nome).split(':')
                nome = nome[1]

                repositorio['fatura'] = nome

        return repositorio

    def passaNome(self, texto, i, nome):

        if nome == 'CONSUMO':
            retorno = self.distribuiColunasValores(texto, i, nome)
            return retorno
        
        elif nome == 'CONSUMOPONTA':
            retorno = self.distribuiColunasValores(texto, i, nome)
            return retorno
        
        elif nome == 'CONSUMOFORA':
            retorno = self.distribuiColunasValores(texto, i, nome)
            return retorno

        elif nome == 'ENERINJOUCMPT':
            retorno = self.distribuiColunasValores(texto, i, nome)
            return retorno
        
        elif nome == 'ENERINJOUCOPT':
            retorno = self.distribuiColunasValores(texto, i, nome)
            return retorno
        
        elif nome == 'INJPTOUCMPT':
            retorno = self.distribuiColunasValores(texto, i, nome)
            return retorno
        
        elif nome == 'INJFPOUCMPT':
            retorno = self.distribuiColunasValores(texto, i, nome)
            return retorno
        
        elif nome == 'COSIPMUNICIPAL':
            retorno = self.distribuiColunasValores(texto, i, nome)
            return retorno
        
        elif nome == 'DEMANDA':
            retorno = self.distribuiColunasValores(texto, i, nome)
            return retorno

        elif nome == 'DEMANDAISENTA':
            retorno = self.distribuiColunasValores(texto, i, nome)
            return retorno
        
        elif nome == 'ENERGIAREAT':
            retorno = self.distribuiColunasValores(texto, i, nome)
            return retorno
        
        elif nome == 'AJUSTECONSUANTERIOR':
            retorno = self.distribuiColunasValores(texto, i, nome)
            return retorno

        elif nome == 'DEVOLUCAODEAJUSTEDEFATURAMENTO':
            retorno = self.distribuiColunasValores(texto, i, nome)
            return retorno
        
        elif nome == 'JUROSANTERIOR':
            retorno = self.distribuiColunasValores(texto, i, nome)
            return retorno
        
        elif nome == 'MULTAANTERIOR':
            retorno = self.distribuiColunasValores(texto, i, nome)
            return retorno
        
        elif nome == 'CUSTODISPSISTEMA':
            retorno = self.distribuiColunasValores(texto, i, nome)
            return retorno
        
        elif nome == 'DEVOLPAGADUPLICIDADE':
            retorno = self.distribuiColunasValores(texto, i, nome)
            return retorno
        
        elif nome == 'COMPVIOLMETACONTINUIDADE':
            retorno = self.distribuiColunasValores(texto, i, nome)
            return retorno
        
        elif nome == 'DEVCREDITOMESANTERIOR':
            retorno = self.distribuiColunasValores(texto, i, nome)
            return retorno
        
        elif nome == 'DEVJUROSAJUSTEFATURAMENTO':
            retorno = self.distribuiColunasValores(texto, i, nome)
            return retorno
        
        #------------------- TRIBUTOS --------------------------#

        elif nome == 'ICMSV':
            retorno = self.distribuiColunasTributos(texto, i, nome)
            return retorno
        
        elif nome == 'COFINS':
            retorno = self.distribuiColunasTributos(texto, i, nome)
            return retorno
        
        elif nome == 'PIS':
            retorno = self.distribuiColunasTributos(texto, i, nome)
            return retorno

    def  TrataNome(self, nome):
        
        for char in "abcdefghijklmnoprstuvwyxz?/-êí%1234567890.,":
            nome = nome.replace(char, "")
        
        return  nome
  
    def distribuiColunasValores(self, texto, i, nome):
        
        valores = {}

        valores['nome'] = nome

        top = texto[i]['top']
            
        for valor in range(len(texto)):
            if (texto[valor]['x1']  > 588.00 and texto[valor]['x1'] < 610.00) and (texto[valor]['top'] >= top-5 and texto[valor]['top'] <= top+5):
                
                valorNovo = self.Trasformaemvalor(texto[valor]['text'])
                valores['qtd'] = valorNovo

            if (texto[valor]['x1']  > 640.00 and texto[valor]['x1'] < 660.00) and (texto[valor]['top'] >= top-5 and texto[valor]['top'] <= top+5):
                
                valorNovo = self.Trasformaemvalor(texto[valor]['text'])
                valores['te'] = valorNovo
            
            if (texto[valor]['x1']  > 700.00 and texto[valor]['x1'] < 730.00) and (texto[valor]['top'] >= top-5 and texto[valor]['top'] <= top+5):
                
                valorNovo = self.Trasformaemvalor(texto[valor]['text'])
                valores['tusd'] = valorNovo
                
            
            if (texto[valor]['x1']  > 730.52 and texto[valor]['x1'] < 800.00) and (texto[valor]['top'] >= top-5 and texto[valor]['top'] <= top+5):
                
                valorNovo = self.Trasformaemvalor(texto[valor]['text'])
                valores['valor'] = valorNovo
        

        return valores
                
    def distribuiColunasTributos(self, texto, i, nome):

        tributos = {}

        tributos['nome'] = nome

        top = texto[i]['top']

        for valor in range(len(texto)):
            if (texto[valor]['x1']  > 210.00 and texto[valor]['x1'] < 280.00) and (texto[valor]['top'] >= top-5 and texto[valor]['top'] <= top+5):
                
                tributosNovo = self.Trasformaemvalor(texto[valor]['text'])
                tributos['baseCalc'] = tributosNovo

            if (texto[valor]['x1']  > 285.00 and texto[valor]['x1'] < 370.00) and (texto[valor]['top'] >= top-5 and texto[valor]['top'] <= top+5):
                
                tributosNovo = self.Trasformaemvalor(texto[valor]['text'])
                tributos['aliquota'] = tributosNovo
            
            if (texto[valor]['x1']  > 375.00 and texto[valor]['x1'] < 400.00) and (texto[valor]['top'] >= top-5 and texto[valor]['top'] <= top+5):
                
                tributosNovo = self.Trasformaemvalor(texto[valor]['text'])
                tributos['valorTributo'] = tributosNovo
        
        return tributos

    def virgulaemponto(self, texto):

        texto = texto.replace('%', '')
        texto = texto.replace('.','')
        texto = texto.replace(',','.')

        return texto

    def Trasformaemvalor(self, valor):

        valor = self.virgulaemponto(str(valor))

        if '.' in valor:
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

    def completaDic(self, dic):

        lista = ['ConsumoQtd', 'ConsumoTe', 'ConsumoTusd', 'ConsumoValor', 'ConsumoPontaQtd', 'ConsumoPontaTe', 'ConsumoPontaTusd',
                'ConsumoPontaValor',  'ConsumoForaPontaQtd', 'ConsumoForaPontaTe', 'ConsumoForaPontaTusd', 'ConsumoForaPontaValor',
                'MptTEQtd', 'MptTETe', 'MptTEValor', 'MptTUSDQtd', 'MptTUSDTusd', 'MptTUSDValor','MptQtd', 'MptTe', 'MptTusd',
                'MptValor', 'OptTEQtd', 'OptTETe', 'OptTEValor', 'OptTUSDQtd', 'OptTUSDTusd', 'OptTUSDValor',  'OptQtd', 'OptTe', 
                'OptTusd',  'OptValor', 'PtMptTEQtd', 'PtMptTETe', 'PtMptTEValor', 'PtMptTUSDQtd', 'PtMptTUSDTusd', 'PtMptTUSDValor',
                'PtMptQtd',  'PtMptTe', 'PtMptTusd', 'PtMptValor',  'FpMptTEQtd', 'FpMptTETe',  'FpMptTEValor', 'FpMptTUSDQtd',
                'FpMptTUSDTusd', 'FpMptTUSDValor', 'FpMptQtd', 'FpMptTe', 'FpMptTusd', 'FpMptValor', 'CosipValor', 'DemandaTEQtd',
                'DemandaTETe', 'DemandaTEValor',  'DemandaTUSDQtd', 'DemandaTUSDTusd', 'DemandaTUSDValor', 'DemandaQtd', 'DemandaTe', 
                'DemandaTusd', 'DemandaValor', 'DemandaIsentTEQtd',  'DemandaIsentTETe', 'DemandaIsentTEValor', 'DemandaIsentTUSDQtd',
                'DemandaIsentTUSDTusd', 'DemandaIsentTUSDValor',  'DemandaIsentQtd', 'DemandaIsentTe', 'DemandaIsentTusd',
                'DemandaIsentValor',  'EnergiaReatTEQtd', 'EnergiaReatTETe', 'EnergiaReatTEValor',  'EnergiaReatTUSDQtd',
                'EnergiaReatTUSDTusd',  'EnergiaReatTUSDValor',  'EnergiaReatQtd',  'EnergiaReatTe', 'EnergiaReatTusd',
                'EnergiaReatValor', 'AjusteConsuAnteriorValor', 'DevolucaoAjusteFaturamentoValor', 'JurosAnteriorValor',
                'DevJurosFaturamentoValor', 'MultaContaAnteriorValor', 'DispSistemaTEQtd', 'DispSistemaTETe', 'DispSistemaTEValor',
                'DispSistemaTUSDQtd', 'DispSistemaTUSDTusd', 'DispSistemaTUSDValor',  'DispSistemaQtd', 'DispSistemaTe',
                'DispSistemaTusd', 'DispSistemaValor', 'DevPagaDuplicidadeValor', 'ViolMetaContinuidadeValor',  'DevCreditoMesAnteriorValor', 
                'IcmsBaseCalc', 'IcmsAliquota',  'IcmsValorTributo', 'CofinsBaseCalc',  'CofinsAliquota', 'CofinsValorTributo', 
                'PisAliquota', 'PisValorTributo']
        
        for i in lista:
            if i not in dic:
                dic[f'{i}'] = 0
        
        return dic
    
    def Insere_Consumidor_Celesc(self,uc,referencia,MptTEQtd,MptTEValor,MptTUSDValor,MptQtd,MptValor,OptTEQtd,OptTEValor,OptTUSDValor,OptQtd,OptValor,PtMptTEQtd,PtMptTEValor,PtMptTUSDValor,PtMptValor,FpMptTEValor,FpMptTUSDValor,FpMptValor,PtMptTUSDQtd,status,admin_id,cliente_id,distribuidora_id):
 
        query = ' INSERT INTO relatorios_consumidor_celesc (uc,referencia,MptTEQtd,MptTEValor,MptTUSDValor,MptQtd,MptValor,OptTEQtd,OptTEValor,OptTUSDValor,OptQtd,OptValor,PtMptTEQtd,PtMptTEValor,PtMptTUSDValor,PtMptValor,FpMptTEValor,FpMptTUSDValor,FpMptValor,PtMptTUSDQtd,status,admin_id,cliente_id,distribuidora_id) '
        query += f'  VALUES ("{uc}","{referencia}","{MptTEQtd}","{MptTEValor}","{MptTUSDValor}","{MptQtd}","{MptValor}","{OptTEQtd}","{OptTEValor}","{OptTUSDValor}","{OptQtd}","{OptValor}","{PtMptTEQtd}","{PtMptTEValor}","{PtMptTUSDValor}","{PtMptValor}","{FpMptTEValor}","{FpMptTUSDValor}","{FpMptValor}","{PtMptTUSDQtd}","{status}","{admin_id}","{cliente_id}","{distribuidora_id}") '
    	
        cursor = connection.cursor()
        cursor.execute(query)
        cursor.fetchone()

    """def inserirContaAgrupada(self, uc, referencia, numDoc, ConsumoQtd, ConsumoTe, ConsumoTusd, ConsumoValor, ConsumoPontaQtd,
        ConsumoPontaTe, ConsumoPontaTusd, ConsumoPontaValor,  ConsumoForaPontaQtd, ConsumoForaPontaTe, ConsumoForaPontaTusd, ConsumoForaPontaValor,
        MptTEQtd, MptTETe, MptTEValor, MptTUSDQtd, MptTUSDTusd, MptTUSDValor,MptQtd, MptTe, MptTusd, MptValor, OptTEQtd, OptTETe, OptTEValor, 
        OptTUSDQtd, OptTUSDTusd, OptTUSDValor,  OptQtd, OptTe, OptTusd,  OptValor, PtMptTEQtd, PtMptTETe, PtMptTEValor, PtMptTUSDQtd,
        PtMptTUSDTusd, PtMptTUSDValor, PtMptQtd,  PtMptTe, PtMptTusd, PtMptValor,  FpMptTEQtd, FpMptTETe,  FpMptTEValor, FpMptTUSDQtd,
        FpMptTUSDTusd, FpMptTUSDValor, FpMptQtd, FpMptTe, FpMptTusd, FpMptValor, CosipValor, DemandaTEQtd, DemandaTETe, DemandaTEValor,
        DemandaTUSDQtd, DemandaTUSDTusd, DemandaTUSDValor, DemandaQtd, DemandaTe, DemandaTusd, DemandaValor, DemandaIsentTEQtd, 
        DemandaIsentTETe, DemandaIsentTEValor, DemandaIsentTUSDQtd,DemandaIsentTUSDTusd, DemandaIsentTUSDValor,  DemandaIsentQtd, 
        DemandaIsentTe, DemandaIsentTusd, DemandaIsentValor,  EnergiaReatTEQtd, EnergiaReatTETe, EnergiaReatTEValor,  EnergiaReatTUSDQtd,
        EnergiaReatTUSDTusd,  EnergiaReatTUSDValor,  EnergiaReatQtd,  EnergiaReatTe, EnergiaReatTusd, EnergiaReatValor, AjusteConsuAnteriorValor, 
        DevolucaoAjusteFaturamentoValor, JurosAnteriorValor, DevJurosFaturamentoValor, MultaContaAnteriorValor, DispSistemaTEQtd, DispSistemaTETe, DispSistemaTEValor,
        DispSistemaTUSDQtd, DispSistemaTUSDTusd, DispSistemaTUSDValor,  DispSistemaQtd, DispSistemaTe,DispSistemaTusd, DispSistemaValor,
        DevPagaDuplicidadeValor, ViolMetaContinuidadeValor,  DevCreditoMesAnteriorValor, IcmsBaseCalc, IcmsAliquota,  IcmsValorTributo, 
        CofinsBaseCalc,  CofinsAliquota, CofinsValorTributo, PisAliquota, PisValorTributo):


        query = 'INSERT INTO relatorios_consumidor_celesc (uc, referencia, numDoc, ConsumoQtd, ConsumoTe, ConsumoTusd, ConsumoValor, ConsumoPontaQtd, '
        query+= ' ConsumoPontaTe, ConsumoPontaTusd, ConsumoPontaValor,  ConsumoForaPontaQtd, ConsumoForaPontaTe, ConsumoForaPontaTusd, ConsumoForaPontaValor, '
        query+= ' MptTEQtd, MptTETe, MptTEValor, MptTUSDQtd, MptTUSDTusd, MptTUSDValor,MptQtd, MptTe, MptTusd, MptValor, OptTEQtd, OptTETe, OptTEValor, '
        query+= ' OptTUSDQtd, OptTUSDTusd, OptTUSDValor,  OptQtd, OptTe, OptTusd,  OptValor, PtMptTEQtd, PtMptTETe, PtMptTEValor, PtMptTUSDQtd, '
        query+= ' PtMptTUSDTusd, PtMptTUSDValor, PtMptQtd,  PtMptTe, PtMptTusd, PtMptValor,  FpMptTEQtd, FpMptTETe,  FpMptTEValor, FpMptTUSDQtd, '
        query+= ' FpMptTUSDTusd, FpMptTUSDValor, FpMptQtd, FpMptTe, FpMptTusd, FpMptValor, CosipValor, DemandaTEQtd, DemandaTETe, DemandaTEValor, '
        query+= ' DemandaTUSDQtd, DemandaTUSDTusd, DemandaTUSDValor, DemandaQtd, DemandaTe, DemandaTusd, DemandaValor, DemandaIsentTEQtd, '
        query+= ' DemandaIsentTETe, DemandaIsentTEValor, DemandaIsentTUSDQtd,DemandaIsentTUSDTusd, DemandaIsentTUSDValor,  DemandaIsentQtd, '
        query+= ' DemandaIsentTe, DemandaIsentTusd, DemandaIsentValor,  EnergiaReatTEQtd, EnergiaReatTETe, EnergiaReatTEValor,  EnergiaReatTUSDQtd, '
        query+= ' EnergiaReatTUSDTusd,  EnergiaReatTUSDValor,  EnergiaReatQtd,  EnergiaReatTe, EnergiaReatTusd, EnergiaReatValor, AjusteConsuAnteriorValor, '
        query+= ' DevolucaoAjusteFaturamentoValor, JurosAnteriorValor, DevJurosFaturamentoValor, MultaContaAnteriorValor, DispSistemaTEQtd, DispSistemaTETe, DispSistemaTEValor, '
        query+= ' DispSistemaTUSDQtd, DispSistemaTUSDTusd, DispSistemaTUSDValor,  DispSistemaQtd, DispSistemaTe,DispSistemaTusd, DispSistemaValor, '
        query+= ' DevPagaDuplicidadeValor, ViolMetaContinuidadeValor,  DevCreditoMesAnteriorValor, IcmsBaseCalc, IcmsAliquota,  IcmsValorTributo, '
        query+= ' CofinsBaseCalc,  CofinsAliquota, CofinsValorTributo, PisAliquota, PisValorTributo) '

        query+= f' VALUES ("{uc}","{ referencia}","{ numDoc}","{ ConsumoQtd}","{ ConsumoTe}","{ ConsumoTusd}","{ ConsumoValor}","{ ConsumoPontaQtd}", '
        query+= f' "{ConsumoPontaTe}","{ ConsumoPontaTusd}","{ ConsumoPontaValor}","{  ConsumoForaPontaQtd}","{ ConsumoForaPontaTe}","{ ConsumoForaPontaTusd}","{ ConsumoForaPontaValor}", '
        query+= f' "{MptTEQtd}","{ MptTETe}","{ MptTEValor}","{ MptTUSDQtd}","{ MptTUSDTusd}","{ MptTUSDValor}","{MptQtd}","{ MptTe}","{ MptTusd}","{ MptValor}","{ OptTEQtd}","{ OptTETe}","{ OptTEValor}", '
        query+= f' "{OptTUSDQtd}","{ OptTUSDTusd}","{ OptTUSDValor}","{  OptQtd}","{ OptTe}","{ OptTusd}","{  OptValor}","{ PtMptTEQtd}","{ PtMptTETe}","{ PtMptTEValor}","{ PtMptTUSDQtd}", '
        query+= f' "{PtMptTUSDTusd}","{ PtMptTUSDValor}","{ PtMptQtd}","{  PtMptTe}","{ PtMptTusd}","{ PtMptValor}","{  FpMptTEQtd}","{ FpMptTETe}","{  FpMptTEValor}","{ FpMptTUSDQtd}", '
        query+= f' "{FpMptTUSDTusd}","{ FpMptTUSDValor}","{ FpMptQtd}","{ FpMptTe}","{ FpMptTusd}","{ FpMptValor}","{ CosipValor}","{ DemandaTEQtd}","{ DemandaTETe}","{ DemandaTEValor}", '
        query+= f' "{DemandaTUSDQtd}","{ DemandaTUSDTusd}","{ DemandaTUSDValor}","{ DemandaQtd}","{ DemandaTe}","{ DemandaTusd}","{ DemandaValor}","{ DemandaIsentTEQtd}", '
        query+= f' "{DemandaIsentTETe}","{ DemandaIsentTEValor}","{ DemandaIsentTUSDQtd}","{DemandaIsentTUSDTusd}","{ DemandaIsentTUSDValor}","{  DemandaIsentQtd}", '
        query+= f' "{DemandaIsentTe}","{ DemandaIsentTusd}","{ DemandaIsentValor}","{  EnergiaReatTEQtd}","{ EnergiaReatTETe}","{ EnergiaReatTEValor}","{  EnergiaReatTUSDQtd}", '
        query+= f' "{EnergiaReatTUSDTusd}","{  EnergiaReatTUSDValor}","{  EnergiaReatQtd}","{  EnergiaReatTe}","{ EnergiaReatTusd}","{ EnergiaReatValor}","{ AjusteConsuAnteriorValor}", '
        query+= f' "{DevolucaoAjusteFaturamentoValor}","{ JurosAnteriorValor}","{ DevJurosFaturamentoValor}","{ MultaContaAnteriorValor}","{ DispSistemaTEQtd}","{ DispSistemaTETe}","{ DispSistemaTEValor}", '
        query+= f' "{DispSistemaTUSDQtd}","{ DispSistemaTUSDTusd}","{ DispSistemaTUSDValor}","{  DispSistemaQtd}","{ DispSistemaTe}","{DispSistemaTusd}","{ DispSistemaValor}", '
        query+= f' "{DevPagaDuplicidadeValor}","{ ViolMetaContinuidadeValor}","{  DevCreditoMesAnteriorValor}","{ IcmsBaseCalc}","{ IcmsAliquota}","{  IcmsValorTributo}", '
        query+= f' "{CofinsBaseCalc}","{  CofinsAliquota}","{ CofinsValorTributo}","{ PisAliquota}","{ PisValorTributo}" ) '

        conect = Conexao()
        conect.inserir('celesc', query)"""
    
    def VerificaGerador(self, uc,referencia,cli): 
            
        query = 'SELECT * FROM relatorios_gerador_celesc'
        query += f' WHERE uc={uc}'
        query += f' AND Referencia={referencia}'
        query += f' AND cliente_id={cli}'

        cursor = connection.cursor()
        cursor.execute(query)
        resultado = cursor.fetchall()
        return resultado
    
    def AtualizarContaGerador(self, unid_consumidora, valor, referencia):
        
        query = f'UPDATE relatorios_gerador_celesc SET valor = "{valor}"'
        query+= f' WHERE uc = "{unid_consumidora}"' 
        query+= f' AND Referencia = "{referencia}"' 

        cursor = connection.cursor()
        cursor.execute(query)
        cursor.fetchone()
    
    def inserirContaGerador(self,uc,valor,Referencia,Saldo_Anterior,Cred_Receb,Energia_Injetada,Energia_InjetadaFP,Energia_Ativa,Energia_AtivaFP,Credito_Utilizado,Saldo_Mes,Saldo_Transferido,Saldo_Final,status,up,admin_id,cliente_id,distribuidora_id):
        query = 'INSERT INTO relatorios_gerador_celesc (uc,valor,Referencia,Saldo_Anterior,Cred_Receb,Energia_Injetada,Energia_InjetadaFP,Energia_Ativa,Energia_AtivaFP,Credito_Utilizado,Saldo_Mes,Saldo_Transferido,Saldo_Final,status,up,admin_id,cliente_id,distribuidora_id)'
        query+= f' VALUES ("{uc}","{valor}","{Referencia}","{Saldo_Anterior}","{Cred_Receb}","{Energia_Injetada}","{Energia_InjetadaFP}","{Energia_Ativa}","{Energia_AtivaFP}","{Credito_Utilizado}","{Saldo_Mes}","{Saldo_Transferido}","{Saldo_Final}","{status}","{up}","{admin_id}","{cliente_id}","{distribuidora_id}")'

        cursor = connection.cursor()
        cursor.execute(query)
        cursor.fetchone()

    def infoGerador(self, texto):

        texto = texto.replace('REF.:','REFERENCIA ')
        texto = texto.split('DADOS DA UNIDADE CONSUMIDORA') 
        texto = texto[0]
        texto = texto.replace('CONSUMO TOTAL FATURADO','UNIDADECONSS')
        texto = texto.replace('R$', "VALORCONTA")
        texto = texto.replace('\n',' ')
        texto = texto.split(' ')
        texto = list(filter(None, texto))
        
        return texto

    def VerificaAdmin(self): 
            
        query = 'SELECT * FROM relatorios_consumidor_celesc'
        query += f' WHERE admin_id=2'

        cursor = connection.cursor()
        cursor.execute(query)
        resultado = cursor.fetchall()
        return resultado
    
    def VerificaAdmin(self): 
            
        query = 'SELECT uc, status FROM relatorios_consumidor_celesc'
        query += f' WHERE admin_id=2'

        cursor = connection.cursor()
        cursor.execute(query)
        resultado = cursor.fetchall()

        return resultado

    def AtualizarSituacao(self, uc, status, referencia,cli):
        
        query = f'UPDATE relatorios_consumidor_celesc SET admin_id =2, status ={status} '
        query+= f' WHERE uc = "{uc}"' 
        query+= f' AND Referencia = "{referencia}"'
        query+= f' AND cliente_id = "{cli}"'  

        cursor = connection.cursor()
        cursor.execute(query)
        cursor.fetchone()