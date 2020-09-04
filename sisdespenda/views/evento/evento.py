# -*- coding: utf-8 -*-
from django.http import *
from django.shortcuts import render
from django.utils.timezone import utc
from django.contrib.auth.decorators import login_required
from django.db import connection
from collections import namedtuple
from sisdespenda.models import EventoTbl
import datetime
import itertools

@login_required(login_url='/accounts/login/')
def evento_list(request):
    tupla_evento = definir_valores_evento_template(request)
    return render(request, 'onsis/evento/evento_list.html', {'template': tupla_evento})

@login_required(login_url='/accounts/login/')
def evento_list_param(request, ano):
    tupla_evento = definir_valores_evento_template(request, ano=ano)
    tupla_evento['mensagem'] = ('Exibindo eventos para o ano de %s' % ano)
    tupla_evento['status'] = 'warning'
    return render(request, 'onsis/evento/evento_list.html', {'template': tupla_evento})
    
def evento_new(request, nome_evento):
    EventoTbl.objects.create(cd_usuario=request.user.id, 
                                dt_evento=datetime.datetime.utcnow().replace(tzinfo=utc),
                                ds_evento=nome_evento)
    
######################################
#          Funcoes diversas          #
######################################

# Recuperar todos os eventos por usuario
def recuperar_eventos_usuario(request, ano):
    return EventoTbl.objects.all().filter(cd_usuario=request.user.id, dt_evento__year=ano).order_by('-dt_evento')
    
# Recuperar anos disponiveis
def recuperar_anos_evento(request):
    cursor = connection.cursor()
    cursor.execute('SELECT cast(EXTRACT(year FROM dt_evento) as bigint) as ANOS '
                        'FROM evento_tbl WHERE cd_usuario = %s '
                        'GROUP BY EXTRACT(year FROM dt_evento) ' 
                        'ORDER BY EXTRACT(year FROM dt_evento) DESC ', 
                        [request.user.id])
    # 1. Usando fetchall
    lista = cursor.fetchall()
    lista = list(itertools.chain.from_iterable(lista)) # Converte a tupla em lista
    
    return lista
    
# Definir valores para template
def definir_valores_evento_template(request, ano=datetime.date.today().year):
    tupla_evento = {}
    
    eventos = recuperar_eventos_usuario(request, ano)
    if not eventos:
        ano = datetime.date.today().year # Se nao existirem eventos para o ano selecionado, define o ano atual
    tupla_evento['eventos'] = eventos
    
    anos_evento = recuperar_anos_evento(request)
    tupla_evento['anos'] = anos_evento
    
    tupla_evento['ano_atual'] = ano

    return tupla_evento