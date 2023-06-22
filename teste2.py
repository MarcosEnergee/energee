
ucs = [48966365,52537266,31172756,42944114,21909386,53903541,41973722,52496373,32205151]

fatura = ['0','9554.81','377.99','164.64','65.54','148.53','3428.2','0','133.67']

gerado = [0,102811,9483,8561,7255,11659,35660,0,10555]

gerado_FP = ['9167',0,0,0,'3298',0,0,0,0 ]

consumo = [0,1096,1739,1112,120,971,3697,0,326]

consumo_FP = ['0',0,0,0,0,'0',0,0,0]

armazenado = [0,0,3200,2629,1700,1899,0,0,58909]


import mysql.connector
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='energee'
)
cursor = conexao.cursor()
def inserirdados(uc,valor,Referencia,Saldo_Anterior,Cred_Receb,Energia_Injetada,Energia_InjetadaFP,Energia_Ativa,Energia_AtivaFP,Credito_Utilizado,Saldo_Mes,Saldo_Transferido,Saldo_Final,status,up,admin_id,cliente_id,distribuidora_id,liberado,Imposto,descontoCliente,descontoGestao):

    query = ' INSERT INTO  relatorios_gerador_celesc (uc,valor,Referencia,Saldo_Anterior,Cred_Receb,Energia_Injetada,Energia_InjetadaFP,Energia_Ativa,Energia_AtivaFP,Credito_Utilizado,Saldo_Mes,Saldo_Transferido,Saldo_Final,status,up,admin_id,cliente_id,distribuidora_id,liberado,Imposto,descontoCliente,descontoGestao) '
    query+= f' VALUES ("{uc}","{valor}","{Referencia}","{Saldo_Anterior}","{Cred_Receb}","{Energia_Injetada}","{Energia_InjetadaFP}","{Energia_Ativa}","{Energia_AtivaFP}","{Credito_Utilizado}","{Saldo_Mes}","{Saldo_Transferido}","{Saldo_Final}","{status}","{up}","{admin_id}","{cliente_id}","{distribuidora_id}","{liberado}","{Imposto}","{descontoCliente}","{descontoGestao}") '
    cursor.execute(query)
    conexao.commit()


""" print(len(ucs))
print(len(fatura))
print(len(gerado))
print(len(gerado_FP))
print(len(consumo))
print(len(consumo_FP))
print(len(armazenado)) """



for uc,fat,gerac,gerac_FP,cons,cons_FP,arm in zip(ucs,fatura,gerado,gerado_FP,consumo,consumo_FP,armazenado):
    
    inserirdados(uc,fat,'052023',0,0,gerac,gerac_FP,cons,cons_FP,0,0,0,arm,1,0,1,1,2,0,0,0,0)

    
	