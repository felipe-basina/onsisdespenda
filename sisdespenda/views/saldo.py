# -*- coding: utf-8 -*-
from django.http import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection
import datetime
import itertools
from ..models import DespesaTbl, RendaTbl
from django.db.models import Sum
from decimal import Decimal
from operator import itemgetter

@login_required(login_url='/accounts/login/')
def saldo_list(request):
    tupla_saldo = definir_valores_saldo_template(request)
    return render(request, 'onsis/saldo.html', { 'template': tupla_saldo })
    
######################################
#          Funcoes diversas          #
######################################

# Recuperar despesa futura do mes
def recuperar_total_despesa_futura_usuario_mes(request, mes, ano):
    hoje = datetime.date.today()
    return DespesaTbl.objects.filter(cd_usuario=request.user.id,
                                    dt_despesa__gt=hoje, 
                                    dt_despesa__month=mes,
                                    dt_despesa__year=ano).aggregate(Sum('vl_despesa'))
                                    
# Contabilizar valor renda (diferenca)
def recuperar_valor_renda_diferenca(request):
    cursor = connection.cursor()
    consulta = ('select sum(consulta.diferenca) as total_renda from (SELECT CASE WHEN r.periodorenda IS NOT NULL THEN cast(r.periodorenda as bigint) ELSE cast(d.periododespesa as bigint) '
                        'END as ano, CASE WHEN r.valorrenda IS NOT NULL THEN r.valorrenda ELSE 0.0 '
                        'END as valor_renda, CASE WHEN d.valordespesa IS NOT NULL THEN d.valordespesa ELSE 0.0 '
                        'END as valor_despesa, CASE WHEN (r.valorrenda - d.valordespesa) IS NOT NULL THEN (r.valorrenda - d.valordespesa) '
                        'WHEN r.valorrenda IS NOT NULL THEN r.valorrenda ELSE -1 * d.valordespesa '
                        'END as diferenca from ( '
                        'select extract(year from dt_renda) as periodorenda, '
                        'sum(vl_renda) as valorrenda from renda_tbl '
                        'where cd_usuario = %s '
                        'group by extract(year from dt_renda) '
                        'order by extract(year from dt_renda) DESC) as r '
                        'RIGHT JOIN ( '
                        'select extract(year from dt_despesa) as periododespesa, '
                        'sum(vl_despesa) as valordespesa '
                        'from despesa_tbl where '
                        'cd_usuario = %s and '
                        'dt_despesa <= now() '
                        'group by extract(year from dt_despesa) '
                        'order by extract(year from dt_despesa) DESC) as d '
                        'on d.periododespesa = r.periodorenda '
                        'order by r.periodorenda desc) as consulta ')    
    cursor.execute(consulta, [request.user.id, request.user.id])
    # 1. Usando fetchall
    lista = cursor.fetchall()
    lista = list(itertools.chain.from_iterable(lista)) # Converte a tupla em lista
    
    return lista

# Recuperar total despesa futura
def recuperar_total_despesa_futura(request, mes, ano):    
    total_despesa_futura_mes = recuperar_total_despesa_futura_usuario_mes(request, mes, ano)
    if total_despesa_futura_mes['vl_despesa__sum'] == None:
        total_despesa_futura_mes['vl_despesa__sum'] = 0.0
        
    return total_despesa_futura_mes
    
# Recuperar total renda no mes
def recuperar_total_renda_mes(request, ano):    
    hoje = datetime.date.today()
    return RendaTbl.objects.filter(cd_usuario=request.user.id,
                                    dt_renda__month=hoje.month,
                                    dt_renda__year=ano).aggregate(Sum('vl_renda'))

# Recuperar total despesa no mes
def recuperar_total_despesa_mes(request, ano):
    hoje = datetime.date.today()
    return DespesaTbl.objects.filter(cd_usuario=request.user.id,
                                    dt_despesa__lte=hoje,
                                    dt_despesa__month=hoje.month,
                                    dt_despesa__year=ano).aggregate(Sum('vl_despesa'))    

def definir_despesa_futura_lista_por_ano(request, ano=datetime.date.today().year):
    cursor = connection.cursor()
    consulta = ('SELECT concat(lpad(cast(extract(month from dt_despesa) as text), 2, \'0\'), \'/\', extract(year from dt_despesa)), sum(vl_despesa) '
                        'from despesa_tbl WHERE cd_usuario = %s '
                        'and dt_despesa > now() ' 
                        'and extract(year from dt_despesa) = %s '
                        'group by concat(lpad(cast(extract(month from dt_despesa) as text), 2, \'0\'), \'/\', extract(year from dt_despesa)) '
                        'order by concat(lpad(cast(extract(month from dt_despesa) as text), 2, \'0\'), \'/\', extract(year from dt_despesa)) ')
    cursor.execute(consulta, [request.user.id, ano])
    dict = cursor.fetchall()

    return dict

# Definir saldo conforme existirem despesas futuras no ano passado como parametro
def definir_saldo(request, ano, lista, saldo_atual):
    despesa_futura_lista = definir_despesa_futura_lista_por_ano(request, ano)
    
    for periodo, total in despesa_futura_lista:
        novo_dict = {}
        
        novo_dict['periodo'] = periodo
        novo_dict['total_renda'] = str(saldo_atual)
        novo_dict['total_despesa'] = str(total)
        
        saldo_atual = Decimal(saldo_atual) - Decimal(total)
        
        novo_dict['saldo'] = str(saldo_atual)
        
        lista.insert(0, novo_dict) # Insere na primeira posicao da lista

    return lista
    
# Definir valores para template
def definir_valores_saldo_template(request, ano=datetime.date.today().year):
    dict_saldo = {}
      
    # 1. Recuperar total de despesa futura no mes/ano atual
    hoje = datetime.date.today()
    total_despesa_futura_mes = recuperar_total_despesa_futura(request, hoje.month, ano)
    
    # 2. Contabilizar total renda (diferenca)
    total_renda_diferenca = recuperar_valor_renda_diferenca(request)
    
    renda_diferenca = 0.0
    
    if total_renda_diferenca != [None]:
    
        renda_diferenca = total_renda_diferenca[0]
    
    else:
        
        # Recuperar valor renda no mes corrente
        total_renda_mes = recuperar_total_renda_mes(request, ano)
        
        if total_renda_mes['vl_renda__sum'] != None:
        
            renda_diferenca = total_renda_mes['vl_renda__sum']
        
        else:
            
            # Caso nao exista renda, recupera despesa no mes corrente
            total_despesa_mes = recuperar_total_despesa_mes(request, ano)
            
            if total_despesa_mes['vl_despesa__sum'] != None:
        
                renda_diferenca = (-1) * total_despesa_mes['vl_despesa__sum']    
    
    despesa_futura = total_despesa_futura_mes['vl_despesa__sum']
    
    saldo = Decimal(renda_diferenca)

    if Decimal(saldo) == 0:
        saldo = 0.0
    
    lista = []
    
    # Define saldo dos proximos meses, no ano corrente
    lista = definir_saldo(request, ano, lista, saldo)
    
    if len(lista) > 0:
        saldo = lista[0]['saldo']
    else:
        saldo = Decimal(renda_diferenca)
    
    if Decimal(saldo) == 0:
        saldo = 0.0
    
    # Define saldo dos proximos meses, do ano seguinte
    lista = definir_saldo(request, ano + 1, lista, saldo)
    
    return lista