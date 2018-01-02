# -*- coding: utf-8 -*-
from django.http import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection
import datetime
import itertools

@login_required(login_url='/accounts/login/')
def relacao_mes_ano(request):
    tupla_relacao = definir_valores_template_mes_ano(request)
    return render(request, 'onsis/relacao_mes_relatorio.html', { 'template': tupla_relacao })

@login_required(login_url='/accounts/login/')    
def relacao_mes_ano_param(request, ano):
    tupla_relacao = definir_valores_template_mes_ano(request, ano)
    tupla_relacao['mensagem'] = 'Exibindo relatorio de rendas x despesas para o ano de %s' % ano
    tupla_relacao['status'] = 'warning'
    return render(request, 'onsis/relacao_mes_relatorio.html', { 'template': tupla_relacao })
    
@login_required(login_url='/accounts/login/')
def relacao_ano(request):
    tupla_relacao = definir_valores_template_ano(request)
    return render(request, 'onsis/relacao_ano_relatorio.html', { 'template': tupla_relacao })
    
######################################
#          Funcoes diversas          #
######################################

# Auxiliar = imprimir valores tupla!
def imprimir_valores(tupla, operacao):
    print ('## Exibindo valores para operacao = %s' % operacao)
    for valor in tupla:
        print ('valor[0] = %s -- valor[1] = %s -- valor[2] = %s -- valor[3] = %s' % (valor[0], valor[1], valor[2], valor[3]))

# Recuperar anos disponiveis
def recuperar_anos_relacao(request):
    cursor = connection.cursor()   
    cursor.execute('select '
                        'CASE WHEN r.periodorenda IS NOT NULL THEN cast(r.periodorenda as bigint) '
                        'ELSE cast(d.periododespesa as bigint) END as ano '
                        'from ( ' 
                        'select extract(year from dt_renda) as periodorenda, '
                        'sum(vl_renda) as valorrenda '
                        'from renda_tbl where cd_usuario = %s '
                        'group by extract(year from dt_renda) '
                        'order by extract(year from dt_renda) DESC) as r '
                        'RIGHT JOIN ( '
                        'select extract(year from dt_despesa) as periododespesa, '
                        'sum(vl_despesa) as valordespesa '
                        'from despesa_tbl where cd_usuario = %s '
                        'and dt_despesa <= now() '
                        'group by extract(year from dt_despesa) '
                        'order by extract(year from dt_despesa) DESC) as d '
                        'on d.periododespesa = r.periodorenda '
                        'order by r.periodorenda desc', 
                        [request.user.id, request.user.id])
    # 1. Usando fetchall
    lista = cursor.fetchall()
    lista = list(itertools.chain.from_iterable(lista)) # Converte a tupla em lista
    
    return lista
        
# Definir valores template para mes/ano
def definir_valores_template_mes_ano(request, ano=datetime.date.today().year):
    tupla_relacao = {}
    
    tupla_relacao['ano_atual'] = ano
    
    anos_relacao = recuperar_anos_relacao(request)
    tupla_relacao['anos'] = anos_relacao
    
    relacao = recuperar_relacao_mes_ano(request, ano)
    tupla_relacao['relacao'] = relacao
    
    if not relacao:
        tupla_relacao['ano_atual'] = datetime.date.today().year
    
    return tupla_relacao
    
# Definir valores template para ano
def definir_valores_template_ano(request, ano=datetime.date.today().year):
    tupla_relacao = {}
    
    relacao = recuperar_relacao_ano(request)
    tupla_relacao['relacao'] = relacao
    
    return tupla_relacao

# Recuperar relacao por mes/ano
def recuperar_relacao_mes_ano(request, ano=datetime.date.today().year):
    cursor = connection.cursor()
    consulta = ('select CASE WHEN r.periodorenda IS NOT NULL THEN r.periodorenda ELSE d.periododespesa '
                        'END as mes_ano, CASE WHEN r.valorrenda IS NOT NULL THEN r.valorrenda ELSE 0.0 '
                        'END as valor_renda, CASE WHEN d.valordespesa IS NOT NULL THEN d.valordespesa ELSE 0.0 '
                        'END as valor_despesa, CASE '
                        'WHEN (r.valorrenda - d.valordespesa) IS NOT NULL THEN (r.valorrenda - d.valordespesa) '
                        'WHEN r.valorrenda IS NOT NULL THEN r.valorrenda ELSE -1 * d.valordespesa '
                        'END as diferenca '
                        'from ( '
                        'select concat(lpad(cast(extract(month from dt_renda) as text), 2, \'0\'), \'/\', extract(year from dt_renda)) as periodorenda, '
                        'sum(vl_renda) as valorrenda '
                        'from renda_tbl '
                        'WHERE cd_usuario = %s '
                        'AND extract(year from dt_renda) = %s '
                        'group by concat(lpad(cast(extract(month from dt_renda) as text), 2, \'0\'), \'/\', extract(year from dt_renda)) '
                        'order by concat(lpad(cast(extract(month from dt_renda) as text), 2, \'0\'), \'/\', extract(year from dt_renda)) DESC '
                        ') as r '
                        'RIGHT JOIN ( '
                        'select concat(lpad(cast(extract(month from dt_despesa) as text), 2, \'0\'), \'/\', extract(year from dt_despesa)) as periododespesa, '
                        'sum(vl_despesa) as valordespesa '
                        'from despesa_tbl where cd_usuario = %s '
                        'and dt_despesa <= now() '
                        'and extract(year from dt_despesa) = %s '
                        'group by concat(lpad(cast(extract(month from dt_despesa) as text), 2, \'0\'), \'/\', extract(year from dt_despesa)) '
                        'order by concat(lpad(cast(extract(month from dt_despesa) as text), 2, \'0\'), \'/\', extract(year from dt_despesa)) DESC '
                        ') as d on d.periododespesa = r.periodorenda '
                        'order by to_date(d.periododespesa, \'MM/YYYY\') desc ')
    cursor.execute(consulta, [request.user.id, ano, request.user.id, ano])
    tupla = cursor.fetchall()

    imprimir_valores(tupla, 'recuperar_relacao_mes_ano')
    return tupla

# Recuperar relacao por ano
def recuperar_relacao_ano(request, ano=datetime.date.today().year):
    cursor = connection.cursor()
    consulta = ('select CASE WHEN r.periodorenda IS NOT NULL THEN cast(r.periodorenda as bigint) ELSE cast(d.periododespesa as bigint) '
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
                        'order by r.periodorenda desc ')
    cursor.execute(consulta, [request.user.id, request.user.id])
    tupla = cursor.fetchall()

    imprimir_valores(tupla, 'recuperar_relacao_ano')
    return tupla