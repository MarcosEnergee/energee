from django.db import connection
from collections import defaultdict
import pdfplumber
import re

class Copel:

    def Tratatexto(self,caminho,arquivo, pagina):
        pdf = pdfplumber.open(f'{caminho}/{arquivo}')
        p = pdf.pages[pagina]
        texto = p.extract_text()
        texto = texto.replace('3 R$', ' REFERENCIA ')#procurar final do ano
        texto = texto.replace('ENERGIA ELET CONSUMO','ENERGIAELETCONSUMO')
        texto = texto.replace('CONT ILUMIN PUBLICA MUNICIPIO','CONTILUMINPUBLICAMICIPIO')
        texto = texto.replace('ENERGIA ELET USO SISTEMA','ENERGIAELETUSOSISTEMA')
        texto = texto.replace('ENERGIA INJ. OUC MPT TE','ENERGIAINJOUCMPTTE')
        texto = texto.replace('ENERGIA INJ. OUC MPT TUSD','ENERGIAINJOUCMPTTUSD')
        texto = texto.replace('AJUSTE CONSU ANTERIOR','AJUSTECONSUANTERIOR')
        texto = texto.replace('COMP CONS MICRO/MINI GERACAO','COMPCONSMICROMINIGERACAO')
        texto = texto.replace ('Industrial', 'ONIDADECONSUMIDORA')
        texto = texto.replace('TOTAL ','VALORAPAGAR ')
        texto = texto.replace('-','')
        texto = texto.replace('kWh','') 
        texto = texto.replace('UN','')
        texto = texto.replace('\n',' ')

        texto = texto.split(' ')
        texto = list(filter(None, texto))

        valores = self.trataRepedidos(texto)

        return [texto, valores]

    def trataRepedidos (self, lista):

        valores = []
        keys = defaultdict(list)
        for key, value in enumerate(lista):

            keys[value].append(key)

        for value in keys:

            if value == 'ENERGIAINJOUCMPTTE':
                valores.append([value, keys[value]])

            if value == 'ENERGIAINJOUCMPTTUSD':
                valores.append([value, keys[value]])

            if value == 'ENERGIAELETCONSUMO':
                valores.append([value, keys[value]])
            
            if value == 'ENERGIAELETUSOSISTEMA':
                valores.append([value, keys[value]])
            
            if value == 'CONTILUMINPUBLICAMICIPIO':
                valores.append([value, keys[value]])
            
            if value == 'PONTODEPARTIDA':
                valores.append([value, keys[value]])

        return valores
    
    def extraiIdentificacao(self, caminho, arquivo):
       
        pdf = pdfplumber.open(f'{caminho}/{arquivo}')
        p = pdf.pages[2]
        
        texto = p.extract_text()  

        texto = texto.replace('Mês','')
        texto = texto.replace('\n',' ')
        texto = texto.split(' ')
        texto = list(filter(None, texto))

        return texto

    def extraiUC(self,caminho,arquivo, pagina ):
        pdf = pdfplumber.open(f'{caminho}/{arquivo}')
        p = pdf.pages[pagina]
        
        texto = p.extract_text()

        texto = texto.split('Endereço:')
        texto = texto[1]
        texto = texto.split('\n')
        texto = texto[0]
        texto = texto.split(' ')
        texto = texto[-1]

        return texto    

    def virgulaemponto(self, texto):

        texto = texto.replace(',','.')

        return texto

    def Trataqtd(self, lista):
        
        lista_nova = []
        for i in lista:
            i = str(i).replace('.','')
            lista_nova.append(i)

        return lista_nova
    
    def Trasformaemvalor(self, lista):
        lista_nova = []
        for i in lista:
            i = self.virgulaemponto(str(i))
            if '.' in i:
                try:
                    i = float(i)
                except:
                    i = i
                lista_nova.append(i)
            else:
                try:
                    i = int(i)
                except:
                    i = i
                lista_nova.append(i)

        return lista_nova
    
    def TrataRetornoDic(self,repositorio): 
        
        ucs = self.filtraUc(repositorio)

        s = []
        for uc in ucs:
            rep = []
            for dic in repositorio:
                if dic['uc'] == uc:
                    rep.append(dic)
            s.append(rep)

        retorno = self.SomaUc(s)

        return retorno

    def filtraUc(self,lista):

        repositorio = []
        for i in lista:
            if i['uc'] not in repositorio:
                repositorio.append(i['uc'])
        
        return repositorio

    def TrataRetorno(self,lista):
        dic = {}
        for i in lista:
            dic['identificacao'] = i[1]
            dic['uc'] = i[2]
            dic['referencia'] = i[3]
            dic['valor'] = i[4]
            dic['qtdmptte'] = i[5]
            dic['precomptte'] = i[6]
            dic['valormptte'] = i[7]
            dic['qtdmpttusd'] = i[8]
            dic['precompttusd'] = i[9]
            dic['valormpttusd'] = i[10]
            dic['qtdconsumo'] = i[11]
            dic['precoconsumo'] = i[12]
            dic['valorconsumo'] = i[13]
            dic['qtduss'] = i[14]
            dic['precouss'] = i[15]
            dic['valoruss'] = i[16]
            dic['qtdilupubli'] = i[17]
            dic['precoilupubli'] = i[18]
            dic['valorilupubli'] = i[19 ]
        
        return dic
    
    def SomaUc(self, lista):
        
        retorno = []
        for i in lista:
            r = {}
            tamanho = len(i)
            r['identificacao'] = i[0]['identificacao']
            r['uc'] = i[0]['uc']
            r['referencia'] = i[0]['referencia']
            r['valor'] = round(sum(valor['valor'] for valor in i),2)
            r['qtdmptte'] = sum(valor['qtdmptte'] for valor in i)
            r['precomptte'] =round(sum(valor['precomptte'] for valor in i)/tamanho,6)
            r['valormptte'] = round(sum(valor['valormptte'] for valor in i),2)
            r['qtdmpttusd'] = sum(valor['qtdmpttusd'] for valor in i)
            r['precompttusd'] = round(sum(valor['precompttusd'] for valor in i)/tamanho,6)
            r['valormpttusd'] = round(sum(valor['valormpttusd'] for valor in i),2)
            r['qtdconsumo'] = sum(valor['qtdconsumo'] for valor in i)
            r['precoconsumo'] = round(sum(valor['precoconsumo'] for valor in i)/tamanho,6)
            r['valorconsumo'] = round(sum(valor['valorconsumo'] for valor in i),2)
            r['qtduss'] = sum(valor['qtduss'] for valor in i)
            r['precouss'] = round(sum(valor['precouss'] for valor in i)/tamanho,6)
            r['valoruss'] = round(sum(valor['valoruss'] for valor in i),2)
            r['qtdilupubli'] = sum(valor['qtdilupubli'] for valor in i)
            r['precoilupubli'] = round(sum(valor['precoilupubli'] for valor in i),6)
            r['valorilupubli'] = round(sum(valor['valorilupubli'] for valor in i),2)

            retorno.append(r)    

        return retorno
    
    def inserirConsumidor(self, identificacao,uc,valor,referencia,qtdmptte,precomptte,valormptte,qtdmpttusd,precompttusd,valormpttusd,qtdconsumo,precoconsumo,valorconsumo,qtduss,precouss,valoruss,qtdilupubli,precoilupubli,valorilupubli,status,admin_id,distribuidora_id,cliente_id): 
       
        query = 'INSERT INTO relatorios_consumidor (identificacao,uc,valor,referencia,qtdmptte,precomptte,valormptte,qtdmpttusd,precompttusd,valormpttusd,qtdconsumo,precoconsumo,valorconsumo,qtduss,precouss,valoruss,qtdilupubli,precoilupubli,valorilupubli,status,admin_id,distribuidora_id,cliente_id)'
        query+= f' VALUES ("{identificacao}","{uc}","{valor}","{referencia}","{qtdmptte}","{precomptte}","{valormptte}","{qtdmpttusd}","{precompttusd}","{valormpttusd}","{qtdconsumo}","{precoconsumo}","{valorconsumo}","{qtduss}","{precouss}","{valoruss}","{qtdilupubli}","{precoilupubli}","{valorilupubli}","{status}","{admin_id}","{distribuidora_id}","{cliente_id}")'
        
        cursor = connection.cursor()
        cursor.execute(query)

        cursor.fetchone()

    def infoGerador(self, caminho, arquivo):

        pdf = pdfplumber.open(f'{caminho}/{arquivo}')
        p = pdf.pages[0]
        
        texto = p.extract_text()
        
        base = texto.replace('Nùmero da fatura: ', 'PONTODEPARTIDA ')
        base = base.replace('\n',' ')
        base = base.split(' ')
        uc = base.index('PONTODEPARTIDA')
        uc = base[uc-4]

        referencia = base.index('PONTODEPARTIDA')
        referencia = base[referencia-3]


        valor = texto.split('R$')
        valor = valor[1]
        valor = valor.replace('\n',' ')
        valor = valor.split(' ')
        valor = valor[0]

        pdf.close()
        
        return [uc, valor,referencia]

    def VerificaGerador(self, uc,referencia,cli): 

        query = 'SELECT * FROM relatorios_gerador'
        query += f' WHERE uc={uc}'
        query += f' AND Referencia={referencia}'
        query += f' AND cliente_id={cli}'

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        return resultado

    def AtualizarContaGerador(self, id, valor):
        
        query = f'UPDATE relatorios_gerador SET valor = "{valor}"'
        query+= f' WHERE id = "{id}"' 

        cursor = connection.cursor()
        cursor.execute(query)

        cursor.fetchone()
    
    def inserirContaGerador(self,uc,valor,Referencia,Saldo_Anterior,Cred_Receb,Energia_Injetada,Energia_Ativa,Credito_Utilizado,Saldo_Mes,Saldo_Transferido,Saldo_Final,status,admin_id,distribuidora_id,cliente_id):
        query = 'INSERT INTO relatorios_gerador (uc,valor,Referencia,Saldo_Anterior,Cred_Receb,Energia_Injetada,Energia_Ativa,Credito_Utilizado,Saldo_Mes,Saldo_Transferido,Saldo_Final,status,admin_id,distribuidora_id,cliente_id)'
        query+= f' VALUES ("{uc}","{valor}","{Referencia}","{Saldo_Anterior}","{Cred_Receb}","{Energia_Injetada}","{Energia_Ativa}","{Credito_Utilizado}","{Saldo_Mes}","{Saldo_Transferido}","{Saldo_Final}","{status}","{admin_id}","{distribuidora_id}","{cliente_id}")'

        cursor = connection.cursor()
        cursor.execute(query)

        cursor.fetchone()
    
    def Verificarelatorio(self, uc, Referencia,cli): 

        query = 'SELECT * FROM relatorios_azul'
        query += f' WHERE uc = {uc}'
        query += f' AND Referencia = {Referencia}'
        query += f' AND cliente_id = {cli}'

        cursor = connection.cursor()
        cursor.execute(query)

        resultado = cursor.fetchall()

        return resultado  