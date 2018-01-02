# -*- coding: utf-8 -*-
from django.http import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection
import datetime
import itertools

@login_required(login_url='/accounts/login/')
def despesas_realizadas_mes_ano(request):
    tupla_despesa = definir_valores_template_mes_ano(request)
    return render(request, 'onsis/despesa_mes_relatorio.html', { 'template': tupla_despesa })

@login_required(login_url='/accounts/login/')    
def despesas_realizadas_mes_ano_param(request, ano):
    tupla_despesa = definir_valores_template_mes_ano(request, ano)
    tupla_despesa['mensagem'] = 'Exibindo relatorio de despesas para o ano de %s' % ano
    tupla_despesa['status'] = 'warning'
    return render(request, 'onsis/despesa_mes_relatorio.html', { 'template': tupla_despesa })
    
@login_required(login_url='/accounts/login/')
def despesas_realizadas_ano(request):
    tupla_despesa = definir_valores_template_ano(request)
    return render(request, 'onsis/despesa_ano_relatorio.html', { 'template': tupla_despesa })
    
######################################
#          Funcoes diversas          #
######################################

# Auxiliar = imprimir valores tupla!
def imprimir_valores(tupla, operacao):
    print ('## Exibindo valores para operacao = %s' % operacao)
    for valor in tupla:
        print ('valor[0] = %s -- valor[1] = %s' % (valor[0], valor[1]))

# Recuperar anos disponiveis
def recuperar_anos_despesa(request):
    cursor = connection.cursor()
    cursor.execute('SELECT cast(EXTRACT(year FROM dt_despesa) as bigint) as ANOS '
                        'FROM despesa_tbl WHERE cd_usuario = %s '
                        'GROUP BY EXTRACT(year FROM dt_despesa) ' 
                        'ORDER BY EXTRACT(year FROM dt_despesa) DESC ', 
                        [request.user.id])
    # 1. Usando fetchall
    lista = cursor.fetchall()
    lista = list(itertools.chain.from_iterable(lista)) # Converte a tupla em lista
    
    return lista        
        
# Definir valores template para mes/ano
def definir_valores_template_mes_ano(request, ano=datetime.date.today().year):
    tupla_despesa = {}
    
    tupla_despesa['ano_atual'] = ano
    
    anos_despesa = recuperar_anos_despesa(request)
    tupla_despesa['anos'] = anos_despesa
        
    # Verifica se o ano atual esta presente na lista, caso contrario, adiciona
    ano_atual_aux = datetime.date.today().year
    if int(ano_atual_aux) not in tupla_despesa['anos']:
        tupla_despesa['anos'].insert(0, int(ano_atual_aux)) # Adiciona novo elemento na primeira posicao
    
    despesa_realizada = recuperar_despesas_realizadas_mes_ano(request, ano)
    tupla_despesa['realizada'] = despesa_realizada
    
    despesa_futura = recuperar_despesas_futuras_mes_ano(request, ano)
    tupla_despesa['futura'] = despesa_futura
    
    if not despesa_realizada and not despesa_futura:
        tupla_despesa['ano_atual'] = datetime.date.today().year
    
    return tupla_despesa
    
# Definir valores template para ano
def definir_valores_template_ano(request, ano=datetime.date.today().year):
    tupla_despesa = {}

    tupla_despesa['ano_atual'] = ano
    
    despesa_realizada = recuperar_despesas_realizadas_ano(request)
    tupla_despesa['realizada'] = despesa_realizada
    
    despesa_futura = recuperar_despesas_futuras_ano(request)
    tupla_despesa['futura'] = despesa_futura
    
    return tupla_despesa

# Recuperar despesas realizadas por mes/ano
def recuperar_despesas_realizadas_mes_ano(request, ano=datetime.date.today().year):
    cursor = connection.cursor()
    consulta = ('SELECT concat(lpad(cast(extract(month from dt_despesa) as text), 2, \'0\'), \'/\', extract(year from dt_despesa)), sum(vl_despesa) '
                        'from despesa_tbl WHERE cd_usuario = %s '
                        'and dt_despesa <= now() ' 
                        'and extract(year from dt_despesa) = %s '
                        'group by concat(lpad(cast(extract(month from dt_despesa) as text), 2, \'0\'), \'/\', extract(year from dt_despesa)) '
                        'order by concat(lpad(cast(extract(month from dt_despesa) as text), 2, \'0\'), \'/\', extract(year from dt_despesa)) desc ')
    cursor.execute(consulta, [request.user.id, ano])
    tupla = cursor.fetchall()

    imprimir_valores(tupla, 'recuperar_despesas_realizadas_mes_ano')
    return tupla
    
# Recuperar despesas futuras por mes/ano
def recuperar_despesas_futuras_mes_ano(request, ano=datetime.date.today().year):
    cursor = connection.cursor()
    consulta = ('SELECT concat(lpad(cast(extract(month from dt_despesa) as text), 2, \'0\'), \'/\', extract(year from dt_despesa)), sum(vl_despesa) '
                        'from despesa_tbl WHERE cd_usuario = %s '
                        'and dt_despesa > now() ' 
                        'and extract(year from dt_despesa) = %s '
                        'group by concat(lpad(cast(extract(month from dt_despesa) as text), 2, \'0\'), \'/\', extract(year from dt_despesa)) '
                        'order by concat(lpad(cast(extract(month from dt_despesa) as text), 2, \'0\'), \'/\', extract(year from dt_despesa)) desc ')
    cursor.execute(consulta, [request.user.id, ano])
    tupla = cursor.fetchall()

    imprimir_valores(tupla, 'recuperar_despesas_futuras_mes_ano')
    return tupla
    
# Recuperar despesas realizadas por ano
def recuperar_despesas_realizadas_ano(request, ano=datetime.date.today().year):
    cursor = connection.cursor()
    consulta = ('SELECT cast(extract(year from dt_despesa) as bigint), sum(vl_despesa) '
                        'from despesa_tbl WHERE cd_usuario = %s '
                        'and dt_despesa <= now() ' 
                        'group by extract(year from dt_despesa) '
                        'order by extract(year from dt_despesa) desc ')
    cursor.execute(consulta, [request.user.id])
    tupla = cursor.fetchall()

    imprimir_valores(tupla, 'recuperar_despesas_realizadas_ano')
    return tupla
    
# Recuperar despesas futuras por ano
def recuperar_despesas_futuras_ano(request, ano=datetime.date.today().year):
    cursor = connection.cursor()
    consulta = ('SELECT cast(extract(year from dt_despesa) as bigint), sum(vl_despesa) '
                        'from despesa_tbl WHERE cd_usuario = %s '
                        'and dt_despesa > now() ' 
                        'group by extract(year from dt_despesa) '
                        'order by extract(year from dt_despesa) desc ')
    cursor.execute(consulta, [request.user.id])
    tupla = cursor.fetchall()

    imprimir_valores(tupla, 'recuperar_despesas_futuras_ano')
    return tupla