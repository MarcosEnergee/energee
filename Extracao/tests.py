
# celesc

import mysql.connector

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='energee'
)
cursor = conexao.cursor()

#print('credito kwh ->',Relatorio.CredCompensado(referencia,cli))# relatorios_consumidor
#print('Credito R$ ->',Relatorio.CreditoBruto(referencia))# relatorios_consumidor
#print('Arm kwh ->', Relatorio.SaldoFinalCli(referencia,cli))# relatorios_azul
#print('consumo total->', Relatorio.TotalConsumo(referencia)[0][1])# relatorios_consumidor

def Insere_Consumidor_Celesc(uc,referencia,MptTEQtd,MptTEValor,MptTUSDValor,MptQtd,MptValor,OptTEQtd,OptTEValor,OptTUSDValor,OptQtd,OptValor,PtMptTEQtd,PtMptTUSDQtd,PtMptTUSDValor,PtMptValor,FpMptTEValor,FpMptTUSDValor,FpMptValor,status,admin_id,cliente_id,distribuidora_id,PtMptTEValor):

    query = ' INSERT INTO relatorios_consumidor_celesc (uc,referencia,MptTEQtd,MptTEValor,MptTUSDValor,MptQtd,MptValor,OptTEQtd,OptTEValor,OptTUSDValor,OptQtd,OptValor,PtMptTEQtd,PtMptTUSDQtd,PtMptTUSDValor,PtMptValor,FpMptTEValor,FpMptTUSDValor,FpMptValor,status,admin_id,cliente_id,distribuidora_id,PtMptTEValor) '
    query += f'  VALUES ("{uc}","{referencia}","{MptTEQtd}","{MptTEValor}","{MptTUSDValor}","{MptQtd}","{MptValor}","{OptTEQtd}","{OptTEValor}","{OptTUSDValor}","{OptQtd}","{OptValor}","{PtMptTEQtd}","{PtMptTUSDQtd}","{PtMptTUSDValor}","{PtMptValor}","{FpMptTEValor}","{FpMptTUSDValor}","{FpMptValor}","{status}","{admin_id}","{cliente_id}","{distribuidora_id}","{PtMptTEValor}") '
    cursor.execute(query)
    conexao.commit()

def Insere_Azul_Celesc(uc,valor,Referencia,Saldo_Anterior,Cred_Receb,Energia_Injetada,Energia_InjetadaFP,Energia_Ativa,Energia_AtivaFP,Credito_Utilizado,Saldo_Mes,Saldo_Transferido,Saldo_Final,status,up,admin_id,cliente_id,distribuidora_id):

    query = ' INSERT INTO relatorios_azul_celesc (uc,valor,Referencia,Saldo_Anterior,Cred_Receb,Energia_Injetada,Energia_InjetadaFP,Energia_Ativa,Energia_AtivaFP,Credito_Utilizado,Saldo_Mes,Saldo_Transferido,Saldo_Final,status,up,admin_id,cliente_id,distribuidora_id) '
    query += f'  VALUES ("{uc}","{valor}","{Referencia}","{Saldo_Anterior}","{Cred_Receb}","{Energia_Injetada}","{Energia_InjetadaFP}","{Energia_Ativa}","{Energia_AtivaFP}","{Credito_Utilizado}","{Saldo_Mes}","{Saldo_Transferido}","{Saldo_Final}","{status}","{up}","{admin_id}","{cliente_id}","{distribuidora_id}") '
    cursor.execute(query)
    conexao.commit()


periodo = ['072018','082018','092018','102018','112018','122018','012019','022019','032019','042019','052019','062019','072019','082019','092019','102019','112019','122019','012020','022020','032020','042020','052020','062020','072020','082020','092020','102020','112020','122020','012021','022021','032021','042021','052021','062021','072021','082021','092021','102021','112021','122021','012022','022022','032022','042022','052022','062022','072022','082022','092022','102022','112022','122022','012023','022023','032023','042023']
Credito_kwh = ['0','0','18060','21339','20109','18197','11248','21856','46868','36996','26572','25675','89042','97236','90887','126606','154712','176073','158635','137919','183800','211557','218447','194654','110069','89041','90117','154068','206559','205654','249460','224524','200853','224447','199348','193560','157234','166678','200820','198202','211162','287695','284662','339947','278044','324038','329912','274902','278532','254098','254357','220864','270972','250319','248611','197049','184792','175680']
credito_R = ['0','0','18640','22461','20780','19942','44477','73837','76662','51891','72149','66319','51055','57955','50798','65256','78664','81239','71861','97832','111376','125576','144365','133129','62245','52119','57192','99774','138732','142894','178809','154889','144176','159862','146618','141578','116463','131322','173964','180864','180046','241262','243850','284207','235431','268957','226502','179642','178151','163886','168871','166340','162568','169883','165076','133638','124843','118460']
armazenado = ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','12665','13505','16300','22642','28518','21836','27177','51449','57247','90865','43838','59479','50800','58518','65609','76237','89084','90760','109742','107531','122194','129798','100097','85334','85133','817434','0','38526']
#consumo =['0','0','405619','522402','570549','743181','78154','92942','72157','63222','49890','39100','440390','418428','436530','512203','717064','785781','1015449','987791','861637','830823','872154','880078','434218','371176','454176','575275','658512','873362','949414','977612','992980','905883','632451','469353','451674','450779','486569','536348','617315','831156','65395','70920','63130','39681','29299','19350','357217','372054','354436','354103','457037','613219','687520','817434','0','668342']


#for referencia,MptTEQtd,MptTEValor in zip(periodo,Credito_kwh,credito_R):
    #print(referencia,MptTEQtd,MptTEValor)

#------------------------------#
# relatorios_consumidor_celesc |
#------------------------------#
#'valormptte' --> Credito_R    |
#'qtdmptte' --> credito_kwh    |
#'qtdconsumo' --> consumo      |
#-------------------------- ---#

    #Insere_Consumidor_Celesc(0,referencia,MptTEQtd,MptTEValor,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,2,2)

for Referencia,Saldo_Final in zip(periodo,armazenado):
    print(Referencia,Saldo_Final)

    #Insere_Azul_Celesc(0,0,Referencia,0,0,0,0,0,0,0,0,0,Saldo_Final,1,1,1,1,2)









