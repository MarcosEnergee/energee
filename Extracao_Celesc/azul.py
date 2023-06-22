from django.db import connection

class Relatorio:

    def Verificarelatorio(self, uc, Referencia,cli): 
 
        query = 'SELECT * FROM relatorioAzul'
        query += f' WHERE uc = {uc}'
        query += f' AND Referencia = {Referencia}'
        query += f' AND cliente_id = {cli}'

        cursor = connection.cursor()
        cursor.execute(query)
        resultado = cursor.fetchall()
        return resultado 
    
    def Verificarelatorio_celesc(self, uc, Referencia,cli): 
 
        query = 'SELECT * FROM relatorios_azul_celesc'
        query += f' WHERE uc = {uc}'
        query += f' AND Referencia = {Referencia}'
        query += f' AND cliente_id = {cli}'

        cursor = connection.cursor()
        cursor.execute(query)
        resultado = cursor.fetchall()
        return resultado 

    def tratar(self,valor):

        valor = int(str(valor).replace('.',''))

        return valor
    
    def ExtrairValor(self, texto, tabela):

        tamanho = len(tabela[2])

        dic = {}

        uc = texto.split("UC :")
        del uc[0]
        uc = uc[-1]
        uc = uc.split("Tipo da Fase")
        uc = uc[0]
        uc = uc.replace(" ","")

        try:
            Referencia = tabela[2][0]
            Referencia = Referencia.replace("/","")
            Referencia = Referencia.replace("-","")
        except:
            Referencia = '-'


        try:
            if tamanho == 9:
                Saldo_Anterior = self.tratar(tabela[2][1])
            elif tamanho == 17:
                Saldo_Anterior = self.tratar(tabela[2][1])+self.tratar(tabela[2][2])
            elif tamanho == 25:
                Saldo_Anterior = self.tratar(tabela[2][1])+self.tratar(tabela[2][2])+self.tratar(tabela[2][3])
        except:
            Saldo_Anterior = '-'

        try:
            if tamanho == 9:
                Cred_Receb = self.tratar(tabela[2][2])
            elif tamanho == 17:
                Cred_Receb = self.tratar(tabela[2][3])+self.tratar(tabela[2][4])
            elif tamanho == 25:
                Cred_Receb = self.tratar(tabela[2][4])+self.tratar(tabela[2][5])+self.tratar(tabela[2][6])
        except:
            Cred_Receb = '-'

        try:
            if tamanho == 9:
                Energia_Injetada = self.tratar(tabela[2][3])
            elif tamanho == 17:
                Energia_Injetada = self.tratar(tabela[2][5])
            elif tamanho == 25:
                Energia_Injetada = self.tratar(tabela[2][9])
        except:
            Energia_Injetada = '-'
        
        try:
            if tamanho == 9:
                Energia_InjetadaFP = 0
            elif tamanho == 17:
                Energia_InjetadaFP = self.tratar(tabela[2][6])
            elif tamanho == 25:
                Energia_InjetadaFP = self.tratar(tabela[2][8])
        except:
            Energia_Injetada = '-'

        try:
            if tamanho == 9:
                Energia_Ativa = self.tratar(tabela[2][4])
            elif tamanho == 17:
                Energia_Ativa = self.tratar(tabela[2][7])
            elif tamanho == 25:
                Energia_Ativa = self.tratar(tabela[2][12])
        except:
            Energia_Ativa = '-'
        
        try:
            if tamanho == 9:
                Energia_AtivaFP = self.tratar(tabela[2][4])
            elif tamanho == 17:
                Energia_AtivaFP = self.tratar(tabela[2][8])
            elif tamanho == 25:
                Energia_AtivaFP = self.tratar(tabela[2][11])

        except:
            Energia_Ativa = '-'
        
        try:
            if tamanho == 9:
                Credito_Utilizado = self.tratar(tabela[2][5])
            elif tamanho == 17:
                Credito_Utilizado = self.tratar(tabela[2][9])+self.tratar(tabela[2][10])
            elif tamanho == 25:
                Credito_Utilizado = self.tratar(tabela[2][13])+self.tratar(tabela[2][14])+self.tratar(tabela[2][15])
        except:
            Credito_Utilizado = '-'
        
        try:
            if tamanho == 9:
                Saldo_Mes = self.tratar(tabela[2][6])
            elif tamanho == 17:
                Saldo_Mes = self.tratar(tabela[2][11])+self.tratar(tabela[2][12])
            elif tamanho == 25:
                Saldo_Mes = self.tratar(tabela[2][16])+self.tratar(tabela[2][17])+self.tratar(tabela[2][18])
        except:
            Saldo_Mes = '-'

        try:
            if tamanho == 9:
                Saldo_Transferido = self.tratar(tabela[2][7])
            elif tamanho == 17:
                Saldo_Transferido = self.tratar(tabela[2][13])+self.tratar(tabela[2][14])
            elif tamanho == 25:
                Saldo_Transferido = self.tratar(tabela[2][19])+self.tratar(tabela[2][20])+self.tratar(tabela[2][21])
        except:
            Saldo_Transferido = '-'

        try:
            if tamanho == 9:
                Saldo_Final = self.tratar(tabela[2][8])
            elif tamanho == 17:
                Saldo_Final = self.tratar(tabela[2][15])+self.tratar(tabela[2][16])
            elif tamanho == 25:
                Saldo_Final = self.tratar(tabela[2][22])+self.tratar(tabela[2][23])+self.tratar(tabela[2][24])
        except:
            Saldo_Final = '-'
        
        dic['uc'] = uc
        dic['referencia'] = Referencia
        dic['Saldo_Anterior'] = Saldo_Anterior
        dic['Cred_Receb'] = Cred_Receb
        dic['Energia_Injetada'] = Energia_Injetada
        dic['Energia_InjetadaFP'] = Energia_InjetadaFP
        dic['Energia_Ativa'] = Energia_Ativa
        dic['Energia_AtivaFP'] = Energia_AtivaFP
        dic['Credito_Utilizado'] = Credito_Utilizado
        dic['Saldo_Mes'] = Saldo_Mes
        dic['Saldo_Transferido'] = Saldo_Transferido
        dic['Saldo_Final'] = Saldo_Final

        return dic

    def Verificarepetidos(self,uc,referencia,repo):

        retorno = False
        for i in repo:
            if i['uc']==uc and i['referencia']==referencia:
                retorno=True

        return retorno

    def inserirAzulCelescGerador(self, uc,Referencia,Saldo_Anterior,Cred_Receb,Energia_Injetada,Energia_InjetadaFP,Energia_Ativa,Energia_AtivaFP,Credito_Utilizado,Saldo_Mes,Saldo_Transferido,Saldo_Final,valor,status,up,admin_id,distribuidora_id,cliente_id):

        query = 'INSERT INTO relatorios_gerador_celesc (uc,Referencia,Saldo_Anterior,Cred_Receb,Energia_Injetada,Energia_InjetadaFP,Energia_Ativa,Energia_AtivaFP,Credito_Utilizado,Saldo_Mes,Saldo_Transferido,Saldo_Final,valor,status,up,admin_id,distribuidora_id,cliente_id)'
        query+= f' VALUES ("{uc}","{Referencia}","{Saldo_Anterior}","{Cred_Receb}","{Energia_Injetada}","{Energia_InjetadaFP}","{Energia_Ativa}","{Energia_AtivaFP}","{Credito_Utilizado}","{Saldo_Mes}","{Saldo_Transferido}","{Saldo_Final}","{valor}","{up}","{status}","{admin_id}","{distribuidora_id}","{cliente_id}")'

        cursor = connection.cursor()
        cursor.execute(query)
        cursor.fetchone()

    def AtualizarContaAzul(self,  uc,Referencia,Saldo_Anterior,Cred_Receb,Energia_Injetada,Energia_InjetadaFP,Energia_Ativa,Energia_AtivaFP,Credito_Utilizado,Saldo_Mes,Saldo_Transferido,Saldo_Final,cliente_id):
        
        query = f'UPDATE relatorios_gerador_celesc SET Saldo_Anterior = "{Saldo_Anterior}",Cred_Receb = "{Cred_Receb}",Energia_Injetada = "{Energia_Injetada}", Energia_InjetadaFP = "{Energia_InjetadaFP}" ,Energia_Ativa = "{Energia_Ativa}",Energia_AtivaFP = "{Energia_AtivaFP}",Credito_Utilizado = "{Credito_Utilizado}",Saldo_Mes = "{Saldo_Mes}",Saldo_Transferido = "{Saldo_Transferido}",Saldo_Final = "{Saldo_Final}" '
        query+= f' WHERE uc = "{uc}" ' 
        query+= f' AND Referencia = "{Referencia}" ' 
        query+= f' AND cliente_id = "{cliente_id}" ' 

        cursor = connection.cursor()
        cursor.execute(query)

        cursor.fetchone()

    def inserirAzulCelesc(self, uc,Referencia,Saldo_Anterior,Cred_Receb,Energia_Injetada,Energia_InjetadaFP,Energia_Ativa,Energia_AtivaFP,Credito_Utilizado,Saldo_Mes,Saldo_Transferido,Saldo_Final,valor,status,up,admin_id,distribuidora_id,cliente_id):

        query = 'INSERT INTO relatorios_azul_celesc (uc,Referencia,Saldo_Anterior,Cred_Receb,Energia_Injetada,Energia_InjetadaFP,Energia_Ativa,Energia_AtivaFP,Credito_Utilizado,Saldo_Mes,Saldo_Transferido,Saldo_Final,valor,status,up,admin_id,distribuidora_id,cliente_id)'
        query+= f' VALUES ("{uc}","{Referencia}","{Saldo_Anterior}","{Cred_Receb}","{Energia_Injetada}","{Energia_InjetadaFP}","{Energia_Ativa}","{Energia_AtivaFP}","{Credito_Utilizado}","{Saldo_Mes}","{Saldo_Transferido}","{Saldo_Final}","{valor}","{status}","{up}","{admin_id}","{distribuidora_id}","{cliente_id}") '

        cursor = connection.cursor()
        cursor.execute(query)

        cursor.fetchone()
