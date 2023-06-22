# Gerador celesc

import pandas as pd
import mysql.connector
import glob

def extrair_primeira_coluna(planilhas):
    colunas_totais = []
    for planilha in planilhas:
        df = pd.read_excel(planilha)
        #print(df)
        df = df.fillna(0)
        primeira_coluna = df.iloc[:, 18].tolist()
        colunas_totais.append(primeira_coluna)
    return colunas_totais

# Caminho dos arquivos
caminho = r'C:\Users\Thiago Silva\Downloads\testeCopel\\'

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


def inserirHistorico(uc,Referencia,ValorBruto,splitConsumo,splitBruto,faturaGerador,splitFatura,descontoCliente,splitCliente,descontoGerador,splitGerador,descontoImpostos,admin_id,cliente_id,distribuidora_id):

    query = ' INSERT INTO relatorios_historico (uc,Referencia,ValorBruto,splitConsumo,splitBruto,faturaGerador,splitFatura,descontoCliente,splitCliente,descontoGerador,splitGerador,descontoImpostos,admin_id,cliente_id,distribuidora_id) '
    query+= f' VALUES ("{uc}","{Referencia}","{ValorBruto}","{splitConsumo}","{splitBruto}","{faturaGerador}","{splitFatura}","{descontoCliente}","{splitCliente}","{descontoGerador}","{splitGerador}","{descontoImpostos}","{admin_id}","{cliente_id}","{distribuidora_id}") '

    cursor.execute(query)
    conexao.commit()


def tratavalor(valor):
    if valor == 0.0 or valor == '- ' :
        valor=0
    else:
        valor=valor
    return valor

periodo = ['052005','072019','082019','092019','102019','112019','122019','012020','022020','032020','042020','052020','062020','072020','082020','092020','102020','112020','122020','012021','022021','032021','042021','052021','062021','072021','082021','092021','102021','112021','122021','012022','022022','032022','042022','052022','062022','072022','082022','092022','102022','112022','122022','012023','022023','032023','042023','052023']



# --- celesc --------
for i,ref in zip(zip(*colunas_totais),periodo):
    
   
    uc = int(colunas_totais[0][0])
    Referencia = ref

    ValorBruto = round(tratavalor(i[0]),2)
    splitBruto = round(tratavalor(i[1]),3)

    faturaGerador = round(tratavalor(i[6]),2)
    splitFatura = 0 

    descontoCliente = round(tratavalor(i[2]),2)
    splitCliente = round(tratavalor(i[3]),3)

    descontoGerador = round(tratavalor(i[4]),2)
    splitGerador = round(tratavalor(i[5]),3)

    descontoImpostos = tratavalor(i[7])
    splitConsumo = tratavalor(i[8])

    admin_id = 1 
    cliente_id = 1 
    distribuidora_id = 2 

    inserirHistorico(uc,Referencia,ValorBruto,splitConsumo,splitBruto,faturaGerador,splitFatura,descontoCliente,splitCliente,descontoGerador,splitGerador,descontoImpostos,admin_id,cliente_id,distribuidora_id)


    """ print(uc,
    Referencia,
    ValorBruto,
    splitConsumo,
    splitBruto,
    faturaGerador,
    splitFatura,
    descontoCliente,
    splitCliente,
    descontoGerador,
    splitGerador,
    descontoImpostos,
    admin_id,
    cliente_id,
    distribuidora_id) """


   