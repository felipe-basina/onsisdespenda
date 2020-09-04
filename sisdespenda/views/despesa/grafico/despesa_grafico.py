# -*- coding: utf-8 -*-
from django.http import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection
import datetime
import itertools
import json
    
@login_required(login_url='/accounts/login/')
def despesa_grafico_mes_ano(request, mes=datetime.date.today().month, indice=-1):
    indice = int(indice)

    if int(mes) < 1 or int(mes) > 12:
        mes = datetime.date.today().month
    
    # Visualizacao de despesas futuras, entao deve-se definir o mes atual
    mes_futura_numerico = 0
    mes_futura = 0

    if indice == 1:
        mes_futura_numerico = mes
        mes = datetime.date.today().month

    mes_numerico = mes

    # Relacao despesas realizadas
    total_despesas_agrupadas = recuperar_despesas_agrupadas_mes_ano_por_tipo(request, mes)

    rotulos_descricao = [descricao for (descricao, total) in total_despesas_agrupadas]
    valores_total = [str(total) for (descricao, total) in total_despesas_agrupadas]

    meses = recuperar_meses_despesa(request)
    
    # Caso nao existam meses, define pelo menos o mes atual
    if not meses:
        meses.insert(0, int(mes)) # Adiciona novo elemento na primeira posicao
    
    mes = recuperar_descricao_mes(int(mes))
    
    # Relacao despesas futuras
    meses_futura = recuperar_meses_despesa_futura(request)
    
    if not meses_futura:
    
        rotulos_descricao_futura = []
        
        valores_total_futura = []
    
    else:
    
        # Recupera o primeiro mes disponivel
        mes_futura = meses_futura[len(meses_futura) - 1]
    
        if indice == 1:
            mes_futura = mes_futura_numerico
    
        total_despesas_futuras_agrupadas = recuperar_despesas_futuras_agrupadas_mes_ano_por_tipo(request, mes_futura)
        
        rotulos_descricao_futura = [descricao for (descricao, total) in total_despesas_futuras_agrupadas]
        valores_total_futura = [str(total) for (descricao, total) in total_despesas_futuras_agrupadas]
    
    mensagem = 'Exibindo relatorio de despesas realizadas no mes de %s' % mes
    status = 'info'
    
    if indice == 1:
        mensagem = 'Exibindo relatorio de despesas futuras no mes de %s' % recuperar_descricao_mes(int(mes_futura))    
        status = 'warning'

    if indice > 1 and not total_despesas_agrupadas:
        mensagem = 'Nao existem despesas realizadas no mes de %s' % mes
        status = 'danger'
    
    data = {
        'rotulos': json.dumps(rotulos_descricao),
        'valores': json.dumps(valores_total),
        'rotulos_futura': json.dumps(rotulos_descricao_futura),
        'valores_futura': json.dumps(valores_total_futura),
        'meses': meses,
        'mes_atual': mes_numerico,
        'meses_futura': meses_futura,
        'mes_futura': mes_futura,
        'mensagem': mensagem,
        'status': status
    }

    return render(request, 'onsis/despesa/grafico/despesa_mes_grafico.html', data)

@login_required(login_url='/accounts/login/')
def despesa_grafico_ano(request, ano=datetime.date.today().year):    
    total_despesas_agrupadas = recuperar_despesas_agrupadas_ano_por_tipo(request, ano)

    rotulos_descricao = [descricao for (descricao, total) in total_despesas_agrupadas]
    valores_total = [str(total) for (descricao, total) in total_despesas_agrupadas]
    
    anos = recuperar_anos_despesa(request)
    
    # Caso nao existam anos, define pelo menos o ano atual
    if not anos:
        anos.insert(0, int(ano)) # Adiciona novo elemento na primeira posicao
        
    mensagem = 'Exibindo relatorio de despesas realizadas no ano de %s' % ano
    status = 'warning'
        
    if not rotulos_descricao or not valores_total:
        mensagem = 'Nao exitem despesas realizadas no ano de %s' % ano    
        status = 'danger'        
    
    data = {
        'rotulos': json.dumps(rotulos_descricao),
        'valores': json.dumps(valores_total),
        'anos': anos,
        'ano_atual': int(ano),
        'mensagem': mensagem,
        'status': status
    }
    
    return render(request, 'onsis/despesa/grafico/despesa_ano_grafico.html', data)
    
######################################
#          Funcoes diversas          #
######################################

# Recuperar o agrupamento de despesas x total de registros no mes e ano especifico
def recuperar_despesas_agrupadas_mes_ano_por_tipo(request, mes, ano=datetime.date.today().year):
    cursor = connection.cursor()
    cursor.execute('SELECT tp.DS_TIPO_DESPESA AS DESPESA, SUM(d.VL_DESPESA) AS TOTAL_REGISTROS FROM '
                        'DESPESA_TBL d INNER JOIN TIPO_DESPESA_TBL tp ON tp.CD_REGISTRO = d.CD_TIPO_DESPESA '
                        'WHERE d.CD_USUARIO = %s ' 
                        'AND d.DT_DESPESA <= now() '
                        'AND EXTRACT(month FROM d.DT_DESPESA) = %s '
                        'AND EXTRACT(year FROM d.DT_DESPESA) = %s '
                        'GROUP BY tp.CD_REGISTRO '
                        'ORDER BY tp.DS_TIPO_DESPESA ', 
                        [request.user.id, mes, ano])
    lista = cursor.fetchall()
    return lista  

# Recuperar o agrupamento de despesas x total de registros no ano especifico
def recuperar_despesas_agrupadas_ano_por_tipo(request, ano=datetime.date.today().year):
    cursor = connection.cursor()
    cursor.execute('SELECT tp.DS_TIPO_DESPESA AS DESPESA, SUM(d.VL_DESPESA) AS TOTAL_REGISTROS FROM '
                        'DESPESA_TBL d INNER JOIN TIPO_DESPESA_TBL tp ON tp.CD_REGISTRO = d.CD_TIPO_DESPESA '
                        'WHERE d.CD_USUARIO = %s ' 
                        'AND d.DT_DESPESA <= now() '
                        'AND EXTRACT(year FROM d.DT_DESPESA) = %s '
                        'GROUP BY tp.CD_REGISTRO '
                        'ORDER BY tp.DS_TIPO_DESPESA ', 
                        [request.user.id, ano])
    lista = cursor.fetchall()
    return lista     
    
# Recuperar o agrupamento de despesas futuras x total de registros no mes e ano especifico
def recuperar_despesas_futuras_agrupadas_mes_ano_por_tipo(request, mes, ano=datetime.date.today().year):
    cursor = connection.cursor()
    cursor.execute('SELECT tp.DS_TIPO_DESPESA AS DESPESA, SUM(d.VL_DESPESA) AS TOTAL_REGISTROS FROM '
                        'DESPESA_TBL d INNER JOIN TIPO_DESPESA_TBL tp ON tp.CD_REGISTRO = d.CD_TIPO_DESPESA '
                        'WHERE d.CD_USUARIO = %s ' 
                        'AND d.DT_DESPESA > now() '
                        'AND EXTRACT(month FROM DT_DESPESA) = %s '
                        'AND EXTRACT(year FROM d.DT_DESPESA) = %s '
                        'GROUP BY tp.CD_REGISTRO '
                        'ORDER BY tp.DS_TIPO_DESPESA ', 
                        [request.user.id, mes, ano])
    lista = cursor.fetchall()
    return lista      
   
# Recuperar meses disponiveis
def recuperar_meses_despesa(request, ano=datetime.date.today().year):
    cursor = connection.cursor()
    cursor.execute('SELECT cast(EXTRACT(month FROM dt_despesa) as bigint) as MESES '
                        'FROM despesa_tbl WHERE cd_usuario = %s '
                        'AND DT_DESPESA <= now() '
                        'AND EXTRACT(year FROM DT_DESPESA) = %s '
                        'GROUP BY EXTRACT(month FROM dt_despesa) ' 
                        'ORDER BY EXTRACT(month FROM dt_despesa) DESC ', 
                        [request.user.id, ano])
    # 1. Usando fetchall
    lista = cursor.fetchall()
    lista = list(itertools.chain.from_iterable(lista)) # Converte a tupla em lista
    
    return lista   
    
# Recuperar anos disponiveis
def recuperar_anos_despesa(request):
    cursor = connection.cursor()
    cursor.execute('SELECT cast(EXTRACT(year FROM dt_despesa) as bigint) as ANOS '
                        'FROM despesa_tbl WHERE cd_usuario = %s '
                        'AND DT_DESPESA <= now() '
                        'GROUP BY EXTRACT(year FROM dt_despesa) ' 
                        'ORDER BY EXTRACT(year FROM dt_despesa) DESC ', 
                        [request.user.id])
    # 1. Usando fetchall
    lista = cursor.fetchall()
    lista = list(itertools.chain.from_iterable(lista)) # Converte a tupla em lista
    
    return lista  
    
# Recuperar meses despesas futuras disponiveis
def recuperar_meses_despesa_futura(request, ano=datetime.date.today().year):
    cursor = connection.cursor()
    cursor.execute('SELECT cast(EXTRACT(month FROM dt_despesa) as bigint) as MESES '
                        'FROM despesa_tbl WHERE cd_usuario = %s '
                        'AND DT_DESPESA > now() '
                        'AND EXTRACT(year FROM DT_DESPESA) = %s '
                        'GROUP BY EXTRACT(month FROM dt_despesa) ' 
                        'ORDER BY EXTRACT(month FROM dt_despesa) DESC ', 
                        [request.user.id, ano])
    # 1. Usando fetchall
    lista = cursor.fetchall()
    lista = list(itertools.chain.from_iterable(lista)) # Converte a tupla em lista
    
    return lista  
   
# Recuperar a descricao do mes referente ao seu numero   
def recuperar_descricao_mes(mes):
    if mes == 1: return 'janeiro'
    if mes == 2: return 'fevereiro'
    if mes == 3: return 'marco'
    if mes == 4: return 'abril'
    if mes == 5: return 'maio'
    if mes == 6: return 'junho'
    if mes == 7: return 'julho'
    if mes == 8: return 'agosto'
    if mes == 9: return 'setembro'
    if mes == 10: return 'outubro'
    if mes == 11: return 'novembro'
    if mes == 12: return 'dezembro'
    