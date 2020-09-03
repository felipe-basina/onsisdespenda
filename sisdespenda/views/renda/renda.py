# -*- coding: utf-8 -*-
from django.http import *
from django.shortcuts import render
from django.utils.timezone import utc
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db import connection
from collections import namedtuple
from sisdespenda.models import RendaTbl, TipoRendaTbl
from sisdespenda.models import RendaForm
import datetime
import itertools

@login_required(login_url='/accounts/login/')
def renda_list(request):
    dict_renda = definir_valores_renda_template(request)
    return render(request, 'onsis/renda/renda_list.html', {'template': dict_renda})

@login_required(login_url='/accounts/login/')
def renda_new(request):
    if request.method == "POST":
        form = RendaForm(request.POST)
        if form.is_valid():
            renda = form.save(commit=False)
            renda.cd_usuario = request.user.id
            renda.dt_criacao = datetime.datetime.utcnow().replace(tzinfo=utc)
            renda.dt_atualizacao = datetime.datetime.utcnow().replace(tzinfo=utc)
            renda.save()
            
            dict_renda = definir_valores_renda_template(request)
            dict_renda['mensagem'] = 'Renda salva com sucesso!'
            dict_renda['status'] = 'success'
        else:
            dict_renda = definir_valores_renda_template(request)
            dict_renda['mensagem'] = 'Não foi possível salvar a renda!'
            dict_renda['status'] = 'danger'
            
    return render(request, 'onsis/renda/renda_list.html', {'template': dict_renda})
    
@login_required(login_url='/accounts/login/')	
def renda_update(request, pk):
    print ('Registro selecionado: %s' % pk)

    dict_renda = definir_valores_renda_template(request)
    
    if not pk:
        dict_renda['mensagem'] = 'Registro invalido!'
        dict_renda['status'] = 'danger'
    
        return render(request, 'onsis/renda/renda_list.html', {'template': dict_renda, 'cd_reg': 0})
    try:
        
        renda_cadastrada = RendaTbl.objects.get(cd_registro=pk, cd_usuario=request.user.id)
    
    except RendaTbl.DoesNotExist:
        dict_renda['mensagem'] = 'Registro não encontrado!'
        dict_renda['status'] = 'danger'
        
        return render(request, 'onsis/renda/renda_list.html', {'template': dict_renda, 'cd_reg': 0})
    
    if request.method == "POST":
        form = RendaForm(request.POST)
        if form.is_valid():
            renda = form.save(commit=False)
            
            try:
            
                descricao = unicode(renda.cd_tipo_renda)
                
            except TypeError:
            
                descricao = renda.cd_tipo_renda
                
            except NameError:
            
                descricao = renda.cd_tipo_renda    
            
            try:
        
                tipo_renda = TipoRendaTbl.objects.get(ds_tipo_renda=descricao)

            except TipoRendaTbl.MultipleObjectsReturned:
                # Caso mais de um registro seja recuperado, retorna o valor definido
                # pelo administrador
                tipo_renda = TipoRendaTbl.objects.get(ds_tipo_renda=str(renda.cd_tipo_renda),
                                                        cd_usuario=0)
                                                        
            except TipoRendaTbl.DoesNotExist:
                dict_renda['mensagem'] = 'Tipo renda não encontrado!'
                dict_renda['status'] = 'danger'
        
                return render(request, 'onsis/renda/renda_list.html', {'template': dict_renda, 'cd_reg': 0})
            
            print ('form = %s' % renda)
            nova_renda = RendaTbl(cd_registro=pk,
                                    dt_criacao=renda_cadastrada.dt_criacao,
                                    cd_usuario=renda_cadastrada.cd_usuario,
                                    dt_atualizacao=datetime.datetime.utcnow().replace(tzinfo=utc),
                                    cd_tipo_renda=tipo_renda,
                                    dt_renda=str(renda.dt_renda),
                                    vl_renda=str(renda.vl_renda))
            nova_renda.save(force_insert=False)
                                            
            dict_renda = definir_valores_renda_template(request, 
                                                         ano=renda_cadastrada.dt_renda.year)
            
            dict_renda['mensagem'] = 'Renda atualizada com sucesso!'
            dict_renda['status'] = 'success'

            return render(request, 'onsis/renda/renda_list.html', {'template': dict_renda, 'cd_reg': 0})
    else:
        form = RendaForm()
        dict_renda = definir_valores_renda_template(request)
        
    dict_renda['mensagem'] = 'Não foi possivel atualizar renda!'
    dict_renda['status'] = 'danger'

    return render(request, 'onsis/renda/renda_list.html', {'template': dict_renda, 'cd_reg': 0})

@login_required(login_url='/accounts/login/')
def renda_edit(request, pk):
    dict_renda = definir_valores_renda_template(request)
    
    dict_renda['mensagem'] = 'Renda não encontrada!'
    dict_renda['status'] = 'danger'
    
    try:
        
        renda = RendaTbl.objects.get(cd_registro=pk, cd_usuario=request.user.id)
        print ('renda identificada para id = %s : %s' %(pk, renda))
        
    except RendaTbl.DoesNotExist:
        
        return render(request, 'onsis/renda/renda_list.html', {'template': dict_renda})
    
    if not renda:
    
        return render(request, 'onsis/renda/renda_list.html', {'template': dict_renda})
        
    else:
        
        data = renda.dt_renda
        print ('data = %s' %data)
        
        dia = data.day
        mes = data.month
        ano = data.year
        print ('dia %s - mes %s - ano %s' % (dia, mes, ano))
        
        dia = completar_parte_registro_data(dia)
        
        mes = completar_parte_registro_data(mes)
           
        # Para ser apresentada corretamente na tela, a data precisa estar no formato
        # yyyy-MM-dd
        nova_data = str(ano) + '-' + str(mes) + '-' + str(dia)
        print ('nova data = %s' % nova_data)
        
        form = RendaForm(initial={'cd_tipo_renda': renda.cd_tipo_renda,
                                             'dt_renda': nova_data,
                                             'vl_renda': renda.vl_renda})
        print ('form %s' % form)
        
        dict_renda = definir_valores_renda_template(request, ano=ano)
        
        dict_renda['mensagem'] = 'Renda selecionada para edição!'
        dict_renda['status'] = 'info'
        dict_renda['form'] = form
        dict_renda['form'].fields['cd_tipo_renda'].queryset = recuperar_todos_tipo_renda_usuario(request)
        
        return render(request, 'onsis/renda/renda_list.html', {'template': dict_renda, 'cd_reg': pk})

@login_required(login_url='/accounts/login/')
def renda_list_param(request, ano):
    dict_renda = definir_valores_renda_template(request, ano=ano)
    dict_renda['mensagem'] = ('Exibindo rendas para o ano de %s' % ano)
    dict_renda['status'] = 'warning'
    return render(request, 'onsis/renda/renda_list.html', {'template': dict_renda})
    
@login_required(login_url='/accounts/login/')
def renda_remove(request, pk):
    renda = recuperar_renda_usuario_por_id_renda(request, pk)

    if not renda:
        dict_renda = definir_valores_renda_template(request)
        dict_renda['mensagem'] = 'Renda não encontrada!'
        dict_renda['status'] = 'danger'
    else:
        renda.delete()        
        dict_renda = definir_valores_renda_template(request)
        dict_renda['mensagem'] = 'Renda removida com sucesso!'
        dict_renda['status'] = 'success'
        
    return render(request, 'onsis/renda/renda_list.html', {'template': dict_renda})

######################################
#          Funcoes diversas          #
######################################

# Adiciona '0' ao dia ou mes. Exemplo: '1' = '01'
def completar_parte_registro_data(parte_data):
    if len(str(parte_data)) < 2:
        parte_data = '0' + str(parte_data)
    return parte_data

# Recuperar todas as rendas por usuario
def recuperar_rendas_usuario(request, ano):
    return RendaTbl.objects.all().filter(cd_usuario=request.user.id, dt_renda__year=ano).order_by('-dt_renda')

# Recuperar renda por usuario e id renda
def recuperar_renda_usuario_por_id_renda(request, id):
    return RendaTbl.objects.all().filter(cd_usuario=request.user.id, cd_registro=id).order_by('-dt_renda')
    
# Tipo de renda: recuperar tudo por usuario
def recuperar_todos_tipo_renda_usuario(request):
    return TipoRendaTbl.objects.filter(cd_usuario__in=[0, request.user.id]).order_by('ds_tipo_renda')
    
# Recuperar total de renda por mes
def recuperar_total_renda_usuario_mes(request, ano):
    hoje = datetime.date.today()
    return RendaTbl.objects.filter(cd_usuario=request.user.id,
                                    dt_renda__month=hoje.month,
                                    dt_renda__year=ano).aggregate(Sum('vl_renda'))
                                    
# Recuperar total de renda no ano
def recuperar_total_renda_usuario_ano(request, ano):
    return RendaTbl.objects.filter(cd_usuario=request.user.id, 
                                    dt_renda__year=ano).aggregate(Sum('vl_renda'))
    
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
    
    # 2. Usando retorno como dicionario
    #columns = [col[0] for col in cursor.description]
    #lista = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    # 3. Usando retorno como 'named tupla'
    #desc = cursor.description
    #nt_result = namedtuple('Ano', [col[0] for col in desc])
    #lista = [nt_result(*row) for row in cursor.fetchall()]

    #print ('####### lista %s' % lista)
    
    return lista

# Definir valores para template
def definir_valores_renda_template(request, ano=datetime.date.today().year):
    dict_renda = {}
    
    rendas = recuperar_rendas_usuario(request, ano)
    if not rendas:
        ano = datetime.date.today().year # Se nao existirem rendas para o ano selecionado, define o ano atual
    dict_renda['rendas'] = rendas
    
    total_renda_mes = recuperar_total_renda_usuario_mes(request, ano)
    if total_renda_mes['vl_renda__sum'] == None:
        total_renda_mes['vl_renda__sum'] = 0.0
    dict_renda['total_mes'] = total_renda_mes
    
    total_renda_ano = recuperar_total_renda_usuario_ano(request, ano)
    if total_renda_ano['vl_renda__sum'] == None:
        total_renda_ano['vl_renda__sum'] = 0.0    
    dict_renda['total_ano'] = total_renda_ano
    
    anos_renda = recuperar_anos_renda(request)
    dict_renda['anos'] = anos_renda
    
    # Verifica se o ano atual esta presente na lista, caso contrario, adiciona
    ano_atual_aux = datetime.date.today().year
    if int(ano_atual_aux) not in dict_renda['anos']:
        dict_renda['anos'].insert(0, int(ano_atual_aux)) # Adiciona novo elemento na primeira posicao
    
    form = RendaForm()
    # Referencia: http://stackoverflow.com/questions/8841502/how-to-use-the-request-in-a-modelform-in-django
    form.fields['cd_tipo_renda'].queryset = recuperar_todos_tipo_renda_usuario(request)
    dict_renda['form'] = form
    
    dict_renda['ano_atual'] = ano

    return dict_renda