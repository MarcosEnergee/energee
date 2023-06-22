from django.db import connection

class Relatorio:

    def ExtrairValor(self, texto, tabela):
        
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
            Saldo_Anterior = tabela[2][1]
        except:
            Saldo_Anterior = '-'

        try:
            Cred_Receb = tabela[2][2]
        except:
            Cred_Receb = '-'
        
        try:
            Energia_Injetada = tabela[2][3]
        except:
            Energia_Injetada = '-'

        try:
            Energia_Ativa = tabela[2][4]
        except:
            Energia_Ativa = '-'
        
    
        try:
            Credito_Utilizado = tabela[2][5]
        except:
            Credito_Utilizado = '-'
        
        try:
            Saldo_Mes = tabela[2][6]
        except:
            Saldo_Mes = '-'

        try:
            Saldo_Transferido = tabela[2][7]
        except:
            Saldo_Transferido = '-'

        try:
            Saldo_Final = tabela[2][8]
        except:
            Saldo_Final = '-'
        

        dic['uc'] = uc
        dic['referencia'] = Referencia
        dic['Saldo_Anterior'] = Saldo_Anterior
        dic['Cred_Receb'] = Cred_Receb
        dic['Energia_Injetada'] = Energia_Injetada
        dic['Energia_Ativa'] = Energia_Ativa
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
    
    def inserirAzulcopel(self, uc,Referencia,Saldo_Anterior,Cred_Receb,Energia_Injetada,Energia_Ativa,Credito_Utilizado,Saldo_Mes,Saldo_Transferido,Saldo_Final	,status	,admin_id,distribuidora_id,cliente_id ):

        query = 'INSERT INTO relatorios_Azul (uc,Referencia,Saldo_Anterior,Cred_Receb,Energia_Injetada,Energia_Ativa,Credito_Utilizado,Saldo_Mes,Saldo_Transferido,Saldo_Final	,status	,admin_id,distribuidora_id,cliente_id)'
        query+= f' VALUES ("{uc}","{Referencia}","{Saldo_Anterior}","{Cred_Receb}","{Energia_Injetada}","{Energia_Ativa}","{Credito_Utilizado}","{Saldo_Mes}","{Saldo_Transferido}","{Saldo_Final}","{status}","{admin_id}","{distribuidora_id}","{cliente_id}" ) '

        cursor = connection.cursor()
        cursor.execute(query)

        cursor.fetchone()

    def inserirAzulcopelGerador(self, uc,Referencia,Saldo_Anterior,Cred_Receb,Energia_Injetada,Energia_Ativa,Credito_Utilizado,Saldo_Mes,Saldo_Transferido,Saldo_Final,valor,status,admin_id,distribuidora_id,cliente_id):

        query = 'INSERT INTO relatorioAzulGerador (uc,Referencia,Saldo_Anterior,Cred_Receb,Energia_Injetada,Energia_Ativa,Credito_Utilizado,Saldo_Mes,Saldo_Transferido,Saldo_Final,valor,status,admin_id,distribuidora_id,cliente_id)'
        query+= f' VALUES ("{uc}","{Referencia}","{Saldo_Anterior}","{Cred_Receb}","{Energia_Injetada}","{Energia_Ativa}","{Credito_Utilizado}","{Saldo_Mes}","{Saldo_Transferido}","{Saldo_Final}","{valor}","{status}","{admin_id}","{distribuidora_id}","{cliente_id}")'

        cursor = connection.cursor()
        cursor.execute(query)

        cursor.fetchone()

    def AtualizarContaAzul(self,  unid_consumidora, referencia, Saldo_Anterior,Cred_Receb,Energia_Injetada,Energia_Ativa,Credito_Utilizado,Saldo_Mes,Saldo_Transferido,Saldo_Final,cliente_id):
        
        query = f'UPDATE relatorios_gerador SET Saldo_Anterior = "{Saldo_Anterior}",Cred_Receb = "{Cred_Receb}",Energia_Injetada = "{Energia_Injetada}" ,Energia_Ativa = "{Energia_Ativa}",Credito_Utilizado = "{Credito_Utilizado}",Saldo_Mes = "{Saldo_Mes}",Saldo_Transferido = "{Saldo_Transferido}",Saldo_Final = "{Saldo_Final}" '
        query+= f' WHERE uc = "{unid_consumidora}" ' 
        query+= f' AND Referencia = "{referencia}" ' 
        query+= f' AND cliente_id = "{cliente_id}" ' 

        cursor = connection.cursor()
        cursor.execute(query)

        cursor.fetchone()

"""     def inserirAzulcelesc(self, uc,Referencia,unidadeGeradora, Saldo_Anterior,Cred_Receb,Energia_Injetada,Energia_Ativa,Credito_Utilizado,Saldo_Mes,Saldo_Transferido,Saldo_Final):

        query = 'INSERT INTO relatorioAzul (uc,Referencia, unid_Gerad, Saldo_Anterior,Cred_Receb,Energia_Injetada,Energia_Ativa,Credito_Utilizado,Saldo_Mes,Saldo_Transferido,Saldo_Final)'
        query+= f' VALUES ("{uc}","{Referencia}", "{unidadeGeradora}" , "{Saldo_Anterior}","{Cred_Receb}","{Energia_Injetada}","{Energia_Ativa}","{Credito_Utilizado}","{Saldo_Mes}","{Saldo_Transferido}","{Saldo_Final}")'

        conect = Conexao()
        conect.inserir('celesc', query)

    def inserirAzulcelescGerador(self, uc,Referencia,Saldo_Anterior,Cred_Receb,Energia_Injetada,Energia_Ativa,Credito_Utilizado,Saldo_Mes,Saldo_Transferido,Saldo_Final,valor):

        query = 'INSERT INTO relatorioAzulGerador (uc,Referencia,Saldo_Anterior,Cred_Receb,Energia_Injetada,Energia_Ativa,Credito_Utilizado,Saldo_Mes,Saldo_Transferido,Saldo_Final,valor)'
        query+= f' VALUES ("{uc}","{Referencia}","{Saldo_Anterior}","{Cred_Receb}","{Energia_Injetada}","{Energia_Ativa}","{Credito_Utilizado}","{Saldo_Mes}","{Saldo_Transferido}","{Saldo_Final}","{valor}")'

        conect = Conexao()
        conect.inserir('celesc', query)

    def AtualizarContaAzul(self, tabela, unid_consumidora, referencia, Saldo_Anterior,Cred_Receb,Energia_Injetada,Energia_Ativa,Credito_Utilizado,Saldo_Mes,Saldo_Transferido,Saldo_Final):
        
        query = f'UPDATE relatorioAzulGerador SET Saldo_Anterior = "{Saldo_Anterior}",Cred_Receb = "{Cred_Receb}",Energia_Injetada = "{Energia_Injetada}" ,Energia_Ativa = "{Energia_Ativa}",Credito_Utilizado = "{Credito_Utilizado}",Saldo_Mes = "{Saldo_Mes}",Saldo_Transferido = "{Saldo_Transferido}",Saldo_Final = "{Saldo_Final}"  '
        query+= f' WHERE uc = "{unid_consumidora}" ' 
        query+= f' AND Referencia = "{referencia}" ' 

        conect = Conexao()
        conect.atualizar(tabela, query) """