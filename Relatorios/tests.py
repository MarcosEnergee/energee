# Gerador Copel

import pandas as pd
import mysql.connector
import glob

def extrair_primeira_coluna(planilhas):
    colunas_totais = []
    for planilha in planilhas:
        df = pd.read_excel(planilha)
        df = df.fillna(0)
        primeira_coluna = df.iloc[:, 8].tolist()
        colunas_totais.append(primeira_coluna)
    return colunas_totais

# Caminho dos arquivos
caminho = r'C:\Users\Thiago Silva\Downloads\palncelesc\\'

# Encontrar todos os arquivos .xlsx no diretório
arquivos = glob.glob(caminho + '*.xlsx')

# Extrair a primeira coluna de cada arquivo
colunas_totais = extrair_primeira_coluna(arquivos)

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='energee'
)
cursor = conexao.cursor()

""" def inserirAzulcopel(uc,valor,Referencia,Saldo_Anterior,Cred_Receb,Energia_Injetada,Energia_Ativa,Credito_Utilizado,Saldo_Mes,Saldo_Transferido,Saldo_Final,status,admin_id,distribuidora_id,cliente_id,up,liberado,Imposto,descontoCliente,descontoGestao ):

    query = 'INSERT INTO relatorios_gerador (uc,valor,Referencia,Saldo_Anterior,Cred_Receb,Energia_Injetada,Energia_Ativa,Credito_Utilizado,Saldo_Mes,Saldo_Transferido,Saldo_Final,status,admin_id,distribuidora_id,cliente_id,up,liberado,Imposto,descontoCliente,descontoGestao)'
    query+= f' VALUES ("{uc}","{valor}","{Referencia}","{Saldo_Anterior}","{Cred_Receb}","{Energia_Injetada}","{Energia_Ativa}","{Credito_Utilizado}","{Saldo_Mes}","{Saldo_Transferido}","{Saldo_Final}","{status}","{admin_id}","{distribuidora_id}","{cliente_id}","{up}","{liberado}","{Imposto}","{descontoCliente}","{descontoGestao}" ) '

    cursor.execute(query)
    conexao.commit() """

def inserirAzulcelesc(uc,valor,Referencia,Saldo_Anterior,Cred_Receb,Energia_Injetada,Energia_InjetadaFP,Energia_Ativa,Energia_AtivaFP,Credito_Utilizado,Saldo_Mes,Saldo_Transferido,Saldo_Final,status,up,admin_id,cliente_id,distribuidora_id,liberado,Imposto,descontoCliente,descontoGestao):

    query = ' INSERT INTO relatorios_gerador_celesc (uc,valor,Referencia,Saldo_Anterior,Cred_Receb,Energia_Injetada,Energia_InjetadaFP,Energia_Ativa,Energia_AtivaFP,Credito_Utilizado,Saldo_Mes,Saldo_Transferido,Saldo_Final,status,up,admin_id,cliente_id,distribuidora_id,liberado,Imposto,descontoCliente,descontoGestao) '
    query+= f' VALUES ("{uc}","{valor}","{Referencia}","{Saldo_Anterior}","{Cred_Receb}","{Energia_Injetada}","{Energia_InjetadaFP}","{Energia_Ativa}","{Energia_AtivaFP}","{Credito_Utilizado}","{Saldo_Mes}","{Saldo_Transferido}","{Saldo_Final}","{status}","{up}","{admin_id}","{cliente_id}","{distribuidora_id}","{liberado}","{Imposto}","{descontoCliente}","{descontoGestao}") '

    cursor.execute(query)
    conexao.commit()


def tratavalor(valor):
    if valor == 0.0 or valor == '- ' :
        valor=0
    else:
        valor=valor
    
    return valor
    

periodo = ['052005','072018','082018','092018','102018','112018','122018','012019','022019','032019','042019','052019','062019','072019','082019','092019','102019','112019','122019','012020','022020','032020','042020','052020','062020','072020','082020','092020','102020','112020','122020','012021','022021','032021','042021','052021','062021','072021','082021','092021','102021','112021','122021','012022','022022','032022','042022','052022','062022','072022','082022','092022','102022','112022','122022','012023','022023','032023','042023','052023']


# --- celesc --------
""" for i,ref in zip(zip(*colunas_totais),periodo):

    Referencia = ref
    uc = tratavalor(int(colunas_totais[0][0]))
    Energia_Ativa = int(tratavalor(i[0]))
    Energia_AtivaFP = int(tratavalor(i[1]))
    valor = tratavalor(i[2])
    Energia_Injetada = int(tratavalor(i[3]))
    Energia_InjetadaFP = int(tratavalor(i[4]))
    Impostos = tratavalor(i[5])
    Saldo_Final = int(tratavalor(i[6])) """
    #uc,valor,Referencia,Saldo_Anterior,Cred_Receb,Energia_Injetada,Energia_InjetadaFP,Energia_Ativa,Energia_AtivaFP,Credito_Utilizado,Saldo_Mes,Saldo_Transferido,Saldo_Final,status,up,admin_id,cliente_id,distribuidora_id,liberado,Imposto,descontoCliente,descontoGestao

    #print(uc, int(Energia_Ativa),int(Energia_AtivaFP),valor,Impostos,int(Energia_Injetada),int(Energia_InjetadaFP),int(Saldo_Final),Referencia)
    #inserirAzulcelesc(uc,valor,Referencia,0,0,Energia_Injetada,Energia_InjetadaFP,Energia_Ativa,Energia_AtivaFP,0,0,0,Saldo_Final,1,0,1,1,2,0,Impostos,13,13)

# ----- copel ---------
#for i,ref in zip(zip(*colunas_totais),periodo):
    
"""
    Referencia = ref
    uc = int(colunas_totais[0][0])
    Energia_Ativa = i[0]
    valor = tratavalor(i[1])
    Impostos = i[2]
    Energia_Injetada = i[3]
    Saldo_Final = i[4] 
"""

    #print(uc, int(Energia_Ativa),valor,Impostos,int(Energia_Injetada),int(Saldo_Final),Referencia)
     
    #inserirAzulcopel(uc,valor,Referencia,0,0,int(Energia_Injetada),int(Energia_Ativa),0,0,0,int(Saldo_Final),1,1,1,1,0,0,Impostos,15,12 )




for i,ref in zip(zip(*colunas_totais),periodo):
    print("['",int(colunas_totais[0][0]),"','",int(i[0]),"','",ref,"'],")