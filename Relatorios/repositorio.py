import mysql.connector

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='energee'
)
cursor = conexao.cursor()

def tratavalor(valor):
    valor = str(valor).replace(",", "")
    valor = str(valor).replace(".", "")

    return int(valor)

def CredCompensado(referencia):
    query = f"SELECT SUM(qtdmptte) FROM relatorios_consumidor WHERE referencia = '{referencia}'"

    cursor.execute(query)
    resultado = cursor.fetchall()[0][0]

    if resultado == None or resultado == 0.0:
        resultado = 0

    return int(resultado)

def CreditoBruto(referencia):
    query = f'SELECT SUM(valormptte+valormpttusd) FROM relatorios_consumidor a WHERE Referencia= "{referencia}"'
    cursor.execute(query)
    resultado = cursor.fetchall()[0][0]

    if resultado == None or resultado == 0.0:
        resultado = 0

    return round(resultado,2)


def TotalConsumo(ref):
        
    query = f'SELECT sum(qtdconsumo) FROM relatorios_consumidor WHERE Referencia= "{ref}"'

    cursor.execute(query)
    resultado = cursor.fetchall()[0][0]
    if resultado == None or resultado == 0.0:
        resultado = 0
    
    return resultado

def SaldoFinalCliInd(referencia):

    query = f'SELECT sum(Saldo_Final) FROM relatorios_azul WHERE Referencia= "{referencia}"'
    cursor.execute(query)
    resultado = cursor.fetchall()[0][0]

    if resultado == None or resultado == 0.0:
        resultado = 0

    return resultado


def inserirDados(identificacao,uc,valor,referencia,qtdmptte,precomptte,valormptte,qtdmpttusd,precompttusd,valormpttusd,qtdconsumo,precoconsumo,valorconsumo,qtduss,precouss,valoruss,qtdilupubli,precoilupubli,valorilupubli,status,admin_id,distribuidora_id,cliente_id):
    query = 'INSERT INTO relatorios_consumidor (identificacao,uc,valor,referencia,qtdmptte,precomptte,valormptte,qtdmpttusd,precompttusd,valormpttusd,qtdconsumo,precoconsumo,valorconsumo,qtduss,precouss,valoruss,qtdilupubli,precoilupubli,valorilupubli,status,admin_id,distribuidora_id,cliente_id)'
    query+= f' VALUES ("{identificacao}","{uc}","{valor}","{referencia}","{qtdmptte}","{precomptte}","{valormptte}","{qtdmpttusd}","{precompttusd}","{valormpttusd}","{qtdconsumo}","{precoconsumo}","{valorconsumo}","{qtduss}","{precouss}","{valoruss}","{qtdilupubli}","{precoilupubli}","{valorilupubli}","{status}","{admin_id}","{distribuidora_id}","{cliente_id}")'

    cursor.execute(query)
    conexao.commit()

def inserirSaldo(uc,Referencia,Saldo_Anterior,Cred_Receb,Energia_Injetada,Energia_Ativa,Credito_Utilizado,Saldo_Mes,Saldo_Transferido,Saldo_Final,status,admin_id,distribuidora_id,cliente_id):
    query = 'INSERT INTO relatorios_azul (uc,Referencia,Saldo_Anterior,Cred_Receb,Energia_Injetada,Energia_Ativa,Credito_Utilizado,Saldo_Mes,Saldo_Transferido,Saldo_Final,status,admin_id,distribuidora_id,cliente_id)'
    query+= f' VALUES ("{uc}","{Referencia}","{Saldo_Anterior}","{Cred_Receb}","{Energia_Injetada}","{Energia_Ativa}","{Credito_Utilizado}","{Saldo_Mes}","{Saldo_Transferido}","{Saldo_Final}","{status}","{admin_id}","{distribuidora_id}","{cliente_id}")'

    cursor.execute(query)
    conexao.commit()


#'qtdconsumo' 
consumo =  ['226604','227416','178226','148530','129842','0','181941','350047','179427','263078','306106','266925','254179','276903','242986','230725','158900','173809','171895','183102','218465','291966','285559','322894','219838','202934','209617','189156','115841','105199','96535','107419','141823','150404','167983','244712','252188','285091','308557','182611','142529','113084','116823','122986','119699','110903','163031','223350','236668','265372','238865','268587'] 

#'valormptte' 
Credito_R=['0','0','0','0','0','0','3669,85','6199,45','27714,80','24806,44','21795,60','26906,42','25355,74','29421,91','24011,61','30062,07','27014,80','47430,73','47768,86','49989,76','57613,32','66133,07','74951,93','84630,29','75343,22','82698,38','67718,14','54696,11','65871,96','63739,30','64839,48','74875,31','97936,87','116148,03','131151,62','155510,93','139410,32','122292,20','111588,43','90098,69','75929,27','65571,38','66072,47','65704,18','0','50851,76','91454,43','127236,15','139399,30','155187,25','141335,77','140034,87']

#'qtdmptte' 
credito_kwh=['0','0','0','0','0','0','0','85405','0','0','0','0','35279','41342','34378','43294','38922','68569','70907','76262','88781','103366','116368','121463','105344','122190','100621','81405','95789','88074','80563','86492','107751','122094','140380','173731','156759','140139','129540','106830','103035','90912','100247','98878','90454','76557','137844','191416','210824','234143','213495','212736']

#'referencia' 
periodo = ['012019','022019','032019','042019','052019','062019','072019','082019','092019','102019','112019','122019','012020','022020','032020','042020','052020','062020','072020','082020','092020','102020','112020','122020','012021','022021','032021','042021','052021','062021','072021','082021','092021','102021','112021','122021','012022','022022','032022','042022','052022','062022','072022','082022','092022','102022','112022','122022','012023','022023','032023','042023']


saldo = ['0','0','0','0','0','0','0','0','0','0','0','2283','1038','0','613','1670','1473','8099','26999','35654','24169','18147','8423','12391','17417','11770','8586','9155','51778','93199','140665','138658','145803','109649','109176','58839','45976','34815','37420','36643','20890','65488','93613','100652','92331','138926','190271','185916','216297','212675','202934','212556']

""" for i,c in zip(periodo,credito_kwh):
    atual = tratavalor(CredCompensado(i))
    correto = tratavalor(c)
    dif = correto-atual
    
    print(atual,'-->',correto)

    if atual != correto:
        print(i)
        print(atual,'-->',correto)
        print(dif,'---> qtdmptte')
        print()
        inserirDados(0,0,0,i,dif,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1) #- qtdmptte """

for i,Saldo_Final in zip(periodo,saldo):    
    atual = SaldoFinalCliInd(i)
    correto = tratavalor(Saldo_Final)

    print(i, '-->', Saldo_Final)

    inserirSaldo(0,i,0,0,0,0,0,0,0,Saldo_Final,1,1,1,1)

    
    
    
    """ if correto != atual:
        dif = correto-atual
        print(i)
        print(atual,'-->',correto)#int(str(atual)[:len(str(correto))]))
        print(dif,'---> valormptte')
        print() """
        #inserirDados(0,i,dif,1,1,1,1) #- valormptte


""" for i,c in zip(periodo,consumo):    
    atual = tratavalor(TotalConsumo(i))
    correto = tratavalor(c)
    dif = correto-atual
    

    if dif > 0:
        print(i)
        print(atual,'-->',correto)
        print(dif,'---> qtdconsumo')
        print()
        #inserirDados(0,i,dif,1,1,1,1) #- qtdconsumo """

        

