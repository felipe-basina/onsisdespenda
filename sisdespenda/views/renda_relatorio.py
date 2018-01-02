# -*- coding: utf-8 -*-
from django.http import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection
import datetime
import itertools

@login_required(login_url='/accounts/login/')
def rendas_realizadas_mes_ano(request):
    tupla_renda = definir_valores_template_mes_ano(request)
    return render(request, 'onsis/renda_mes_relatorio.html', { 'template': tupla_renda })

@login_required(login_url='/accounts/login/')    
def rendas_realizadas_mes_ano_param(request, ano):
    tupla_renda = definir_valores_template_mes_ano(request, ano)
    tupla_renda['mensagem'] = 'Exibindo relatorio de rendas para o ano de %s' % ano
    tupla_renda['status'] = 'warning'
    return render(request, 'onsis/renda_mes_relatorio.html', { 'template': tupla_renda })
    
@login_required(login_url='/accounts/login/')
def rendas_realizadas_ano(request):
    tupla_renda = definir_valores_template_ano(request)
    return render(request, 'onsis/renda_ano_relatorio.html', { 'template': tupla_renda })
    
######################################
#          Funcoes diversas          #
######################################

# Auxiliar = imprimir valores tupla!
def imprimir_valores(tupla, operacao):
    print ('## Exibindo valores para operacao = %s' % operacao)
    for valor in tupla:
        print ('valor[0] = %s -- valor[1] = %s' % (valor[0], valor[1]))

# Recuperar anos disponiveis
def recuperar_anos_renda(request):
    cursor = connection.cursor()
    cursor.execute('SELECT cast(EXTRACT(year FROM dt_renda) as bigint) as ANOS '
                        'FROM renda_tbl WHERE cd_usuario = %s '
                        'GROUP BY EXTRACT(year FROM dt_renda) ' 
                        'ORDER BY EXTRACT(year FROM dt_renda) DESC ', 
                        [request.user.id])
    # 1. Usando fetchall
    lista = cursor.fetchall()
    lista = list(itertools.chain.from_iterable(lista)) # Converte a tupla em lista
    
    return lista        
        
# Definir valores template para mes/ano
def definir_valores_template_mes_ano(request, ano=datetime.date.today().year):
    tupla_renda = {}
    
    tupla_renda['ano_atual'] = ano
    
    anos_renda = recuperar_anos_renda(request)
    tupla_renda['anos'] = anos_renda
   
    # Verifica se o ano atual esta presente na lista, caso contrario, adiciona
    ano_atual_aux = datetime.date.today().year
    if int(ano_atual_aux) not in tupla_renda['anos']:
        tupla_renda['anos'].insert(0, int(ano_atual_aux)) # Adiciona novo elemento na primeira posicao
   
    renda_recebida = recuperar_rendas_realizadas_mes_ano(request, ano)
    tupla_renda['recebida'] = renda_recebida
    
    if not renda_recebida:
        tupla_renda['ano_atual'] = datetime.date.today().year
    
    return tupla_renda
    
# Definir valores template para ano
def definir_valores_template_ano(request, ano=datetime.date.today().year):
    tupla_renda = {}

    tupla_renda['ano_atual'] = ano
    
    renda_recebida = recuperar_rendas_realizadas_ano(request)
    tupla_renda['recebida'] = renda_recebida
    
    return tupla_renda

# Recuperar rendas realizadas por mes/ano
def recuperar_rendas_realizadas_mes_ano(request, ano=datetime.date.today().year):
    cursor = connection.cursor()
    consulta = ('SELECT concat(lpad(cast(extract(month from dt_renda) as text), 2, \'0\'), \'/\', extract(year from dt_renda)), sum(vl_renda) '
                        'from renda_tbl WHERE cd_usuario = %s '
                        'and extract(year from dt_renda) = %s '
                        'group by concat(lpad(cast(extract(month from dt_renda) as text), 2, \'0\'), \'/\', extract(year from dt_renda)) '
                        'order by concat(lpad(cast(extract(month from dt_renda) as text), 2, \'0\'), \'/\', extract(year from dt_renda)) desc ')
    cursor.execute(consulta, [request.user.id, ano])
    tupla = cursor.fetchall()

    imprimir_valores(tupla, 'recuperar_rendas_realizadas_mes_ano')
    return tupla

    
# Recuperar rendas realizadas por ano
def recuperar_rendas_realizadas_ano(request, ano=datetime.date.today().year):
    cursor = connection.cursor()
    consulta = ('SELECT cast(extract(year from dt_renda) as bigint), sum(vl_renda) '
                        'from renda_tbl WHERE cd_usuario = %s '
                        'group by extract(year from dt_renda) '
                        'order by extract(year from dt_renda) desc ')
    cursor.execute(consulta, [request.user.id])
    tupla = cursor.fetchall()

    imprimir_valores(tupla, 'recuperar_rendas_realizadas_ano')
    return tupla