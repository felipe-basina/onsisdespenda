# -*- coding: utf-8 -*-
from django.http import *
from django.shortcuts import render
from django.utils.timezone import utc
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db import connection
from sisdespenda.models import DespesaTbl, TipoDespesaTbl
from sisdespenda.models import DespesaForm
from sisdespenda.views.recorrencia.recorrencia_despesa import recuperar_recorrencias_usuario
from itertools import chain
import datetime
import itertools

@login_required(login_url='/accounts/login/')
def despesa_list(request):
    dict_despesa = definir_valores_despesa_template(request)
    return render(request, 'onsis/despesa/despesa_list.html', {'template': dict_despesa})
    
@login_required(login_url='/accounts/login/')
def despesa_new(request):
    if request.method == "POST":
        form = DespesaForm(request.POST)
        if form.is_valid():
            despesa = form.save(commit=False)
            despesa.cd_usuario = request.user.id
            despesa.dt_criacao = datetime.datetime.utcnow().replace(tzinfo=utc)
            despesa.dt_atualizacao = datetime.datetime.utcnow().replace(tzinfo=utc)
            despesa.save()
            
            dict_despesa = definir_valores_despesa_template(request)
            dict_despesa['mensagem'] = 'Despesa salva com sucesso!'
            dict_despesa['status'] = 'success'
        else:
            dict_despesa = definir_valores_despesa_template(request)
            dict_despesa['mensagem'] = 'Não foi possível salvar a despesa!'
            dict_despesa['status'] = 'danger'
            
    dict_despesa['futura'] = despesa.dt_despesa.date() > datetime.date.today()
    
    return render(request, 'onsis/despesa/despesa_list.html', {'template': dict_despesa})
    
@login_required(login_url='/accounts/login/')	
def despesa_update(request, pk):
    dict_despesa = definir_valores_despesa_template(request)
    
    if not pk:
        dict_despesa['mensagem'] = 'Registro invalido!'
        dict_despesa['status'] = 'danger'
    
        return render(request, 'onsis/despesa/despesa_list.html', {'template': dict_despesa, 'cd_reg': 0})
    try:
        
        despesa_cadastrada = DespesaTbl.objects.get(cd_registro=pk, cd_usuario=request.user.id)
    
    except DespesaTbl.DoesNotExist:
        dict_despesa['mensagem'] = 'Registro não encontrado!'
        dict_despesa['status'] = 'danger'
        
        return render(request, 'onsis/despesa/despesa_list.html', {'template': dict_despesa, 'cd_reg': 0})
    
    if request.method == "POST":
        form = DespesaForm(request.POST)
        if form.is_valid():
            despesa = form.save(commit=False)
            
            try:
            
                descricao = unicode(despesa.ds_despesa)
                
            except TypeError:
            
                descricao = despesa.ds_despesa
                
            except NameError:
            
                descricao = despesa.ds_despesa
            
            try:
            
                tipo_despesa = unicode(despesa.cd_tipo_despesa)
                
            except TypeError:
            
                tipo_despesa = despesa.cd_tipo_despesa
                
            except NameError:
            
                tipo_despesa = despesa.cd_tipo_despesa    
            
            try:
        
                tipo_despesa = TipoDespesaTbl.objects.get(ds_tipo_despesa=tipo_despesa)

            except TipoDespesaTbl.MultipleObjectsReturned:
                # Caso mais de um registro seja recuperado, retorna o valor definido
                # pelo administrador
                tipo_despesa = TipoDespesaTbl.objects.get(ds_tipo_despesa=str(despesa.cd_tipo_despesa),
                                                        cd_usuario=0)
                                                        
            except TipoDespesaTbl.DoesNotExist:
                dict_despesa['mensagem'] = 'Tipo despesa não encontrado!'
                dict_despesa['status'] = 'danger'
        
                return render(request, 'onsis/despesa/despesa_list.html', {'template': tupla_renda, 'cd_reg': 0})
                        
            cd_recorrencia_despesa = 0
            if despesa_cadastrada.cd_recorrencia_despesa and despesa_cadastrada.cd_recorrencia_despesa > 0:
                cd_recorrencia_despesa = despesa_cadastrada.cd_recorrencia_despesa

            nova_despesa = DespesaTbl(cd_registro=pk,
                                    dt_criacao=despesa_cadastrada.dt_criacao,
                                    cd_usuario=despesa_cadastrada.cd_usuario,
                                    dt_atualizacao=datetime.datetime.utcnow().replace(tzinfo=utc),
                                    ds_despesa=descricao,
                                    cd_tipo_despesa=tipo_despesa,
                                    dt_despesa=str(despesa.dt_despesa),
                                    vl_despesa=str(despesa.vl_despesa),
                                    cd_recorrencia_despesa=cd_recorrencia_despesa)
            nova_despesa.save(force_insert=False)
                                            
            dict_despesa = definir_valores_despesa_template(request, 
                                                             ano=despesa_cadastrada.dt_despesa.year)
            
            dict_despesa['mensagem'] = 'Despesa atualizada com sucesso!'
            dict_despesa['status'] = 'success'
            dict_despesa['futura'] = despesa.dt_despesa.date() > datetime.date.today()

            return render(request, 'onsis/despesa/despesa_list.html', {'template': dict_despesa, 'cd_reg': 0})
    else:
        form = DespesaForm()
        dict_despesa = definir_valores_despesa_template(request)
        
    dict_despesa['mensagem'] = 'Nao foi possivel atualizar despesa!'
    dict_despesa['status'] = 'danger'

    return render(request, 'onsis/despesa/despesa_list.html', {'template': dict_despesa, 'cd_reg': 0})

@login_required(login_url='/accounts/login/')
def despesa_edit(request, pk):
    dict_despesa = definir_valores_despesa_template(request)
    
    dict_despesa['mensagem'] = 'Despesa não encontrada!'
    dict_despesa['status'] = 'danger'
    
    try:
        
        despesa = DespesaTbl.objects.get(cd_registro=pk, cd_usuario=request.user.id)
        
    except DespesaTbl.DoesNotExist:
        
        return render(request, 'onsis/despesa/despesa_list.html', {'template': dict_despesa})
    
    if not despesa:
    
        return render(request, 'onsis/despesa/despesa_list.html', {'template': dict_despesa})
        
    else:
        
        data = despesa.dt_despesa
        
        dia = data.day
        mes = data.month
        ano = data.year
        
        dia = completar_parte_registro_data(dia)
        
        mes = completar_parte_registro_data(mes)
           
        # Para ser apresentada corretamente na tela, a data precisa estar no formato
        # yyyy-MM-dd
        nova_data = str(ano) + '-' + str(mes) + '-' + str(dia)
        
        form = DespesaForm(initial={'cd_registro': despesa.cd_registro, 
                                               'ds_despesa': despesa.ds_despesa,
                                               'cd_tipo_despesa': despesa.cd_tipo_despesa,
                                               'dt_despesa': nova_data,
                                               'vl_despesa': despesa.vl_despesa})
        
        dict_despesa = definir_valores_despesa_template(request, ano=ano)
        
        dict_despesa['mensagem'] = 'Despesa selecionada para edição!'
        dict_despesa['status'] = 'info'
        dict_despesa['form'] = form
        dict_despesa['form'].fields['cd_tipo_despesa'].queryset = recuperar_todos_tipo_despesa_usuario(request)
        dict_despesa['futura'] = despesa.dt_despesa.date() > datetime.date.today()
        
        return render(request, 'onsis/despesa/despesa_list.html', {'template': dict_despesa, 'cd_reg': pk})
    
    
@login_required(login_url='/accounts/login/')
def despesa_list_param(request, ano):
    dict_despesa = definir_valores_despesa_template(request, ano=ano)
    dict_despesa['mensagem'] = ('Exibindo despesas para o ano de %s' % ano)
    dict_despesa['status'] = 'warning'
    return render(request, 'onsis/despesa/despesa_list.html', {'template': dict_despesa})
    
@login_required(login_url='/accounts/login/')
def despesa_remove(request, pk):
    despesa = recuperar_despesa_usuario_por_id_despesa(request, pk)
    
    if not despesa:
        dict_despesa = definir_valores_despesa_template(request)
        dict_despesa['mensagem'] = 'Despesa não encontrada!'
        dict_despesa['status'] = 'danger'
    else:
        despesa.delete()        
        dict_despesa = definir_valores_despesa_template(request)
        dict_despesa['mensagem'] = 'Despesa removida com sucesso!'
        dict_despesa['status'] = 'success'
        
    return render(request, 'onsis/despesa/despesa_list.html', {'template': dict_despesa})
    
######################################
#          Funcoes diversas          #
######################################

# Adiciona '0' ao dia ou mes. Exemplo: '1' = '01'
def completar_parte_registro_data(parte_data):
    if len(str(parte_data)) < 2:
        parte_data = '0' + str(parte_data)
    return parte_data

# Recuperar todas as despesas, realizadas e futuras, por usuario no ano especifico
def recuperar_todas_despesas_usuario(request, ano):
    return DespesaTbl.objects.all().filter(cd_usuario=request.user.id, 
                                            dt_despesa__year=ano).order_by('-dt_despesa') 

# Recuperar todas as despesas realizadas por usuario no ano especifico
def recuperar_despesas_usuario(request, ano):
    hoje = datetime.date.today()

    return DespesaTbl.objects.all().filter(cd_usuario=request.user.id, 
                                            dt_despesa__lte=hoje,
                                            dt_despesa__year=ano).order_by('-dt_despesa') 
    
# Recuperar todas as despesas futuras por usuario
def recuperar_despesas_futura_usuario(request, ano):
    hoje = datetime.date.today()
    return DespesaTbl.objects.all().filter(cd_usuario=request.user.id, 
                                            dt_despesa__gt=hoje,
                                            dt_despesa__year=ano).order_by('-dt_despesa')
    
# Recuperar despesa por usuario e id despesa
def recuperar_despesa_usuario_por_id_despesa(request, id):
    return DespesaTbl.objects.all().filter(cd_usuario=request.user.id, cd_registro=id).order_by('-dt_despesa')

# Recuperar total de despesa por mes
def recuperar_total_despesa_usuario_mes(request, ano):
    hoje = datetime.date.today()
    return DespesaTbl.objects.filter(cd_usuario=request.user.id,
                                    dt_despesa__lte=hoje,
                                    dt_despesa__month=hoje.month,
                                    dt_despesa__year=ano).aggregate(Sum('vl_despesa'))
                                    
# Recuperar total de despesa no ano
def recuperar_total_despesa_usuario_ano(request, ano):
    hoje = datetime.date.today()
    return DespesaTbl.objects.filter(cd_usuario=request.user.id,
                                    dt_despesa__lte=hoje,
                                    dt_despesa__year=ano).aggregate(Sum('vl_despesa'))

# Recuperar total de despesa futura no mes
def recuperar_total_despesa_futura_usuario_ano(request, ano):
    hoje = datetime.date.today()
    return DespesaTbl.objects.filter(cd_usuario=request.user.id,
                                    dt_despesa__gt=hoje, 
                                    dt_despesa__month=hoje.month,
                                    dt_despesa__year=ano).aggregate(Sum('vl_despesa'))
    
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
    
    # 2. Usando retorno como dicionario
    #columns = [col[0] for col in cursor.description]
    #lista = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    # 3. Usando retorno como 'named tupla'
    #desc = cursor.description
    #nt_result = namedtuple('Ano', [col[0] for col in desc])
    #lista = [nt_result(*row) for row in cursor.fetchall()]

    #print ('####### lista %s' % lista)
    
    return lista

# Tipo de despesa: recuperar tudo por usuario
def recuperar_todos_tipo_despesa_usuario(request):
    return TipoDespesaTbl.objects.filter(cd_usuario__in=[0, request.user.id]).order_by('ds_tipo_despesa')
    
# Verificar se a despesa recorrente ja se encontra na listagem de despesas    
def verificar_despesa_recorrente(despesas, id_despesa_recorrente):
    return any(despesa.cd_recorrencia_despesa == id_despesa_recorrente for despesa in despesas)

# Define a nova despesa, a partir da despesa recorrente, caso ainda nao exista
def definir_despesa_apartir_despesa_recorrente(request, despesas, recorrente, mes, ano):
    if recorrente.recorrencia == 'M' or recorrente.mes_recorrencia == mes:
        if not verificar_despesa_recorrente(despesas, recorrente.cd_registro):
            nova_despesa = DespesaTbl(cd_usuario=request.user.id,
                vl_despesa=recorrente.vl_despesa,
                ds_despesa=recorrente.ds_despesa,
                dt_despesa=(str(ano) + '-' + str(mes) + '-' + str(recorrente.dia_recorrencia)),
                dt_criacao=datetime.datetime.utcnow().replace(tzinfo=utc),
                dt_atualizacao=datetime.datetime.utcnow().replace(tzinfo=utc),
                cd_recorrencia_despesa=recorrente.cd_registro,
                cd_tipo_despesa=recorrente.cd_tipo_despesa)
        
            nova_despesa.save()
            return nova_despesa
    return None

# Adicionar despesas recorrentes existentes
def adicionar_despesas_recorrentes(request, dict_despesa, todas_despesas, ano):
    ano_atual = datetime.date.today().year
    mes_atual = datetime.date.today().month
    dia_atual = datetime.date.today().day

    # Recuperar despesas recorrentes
    despesas_recorrentes = recuperar_recorrencias_usuario(request)

    # Adiciona despesas recorrentes na lista de despesas atuais e futuras
    if despesas_recorrentes:
        for recorrente in despesas_recorrentes:
            # Verifica se a recorrencia ja foi adicionada na lista de despesas
            # Caso nao esteja deve-se adicionar na base
            for _mes in range(mes_atual, 13):
                nova_despesa = definir_despesa_apartir_despesa_recorrente(request, 
                                                                            todas_despesas, 
                                                                            recorrente, 
                                                                            _mes, 
                                                                            ano_atual)

            # Adiciona despesas futuras para o proximo ano a partir do mes especifico
            if mes_atual >= 10:
                proximo_ano = ano + 1
                todas_despesas = recuperar_todas_despesas_usuario(request, proximo_ano)
                for _mes in range(1, 13):
                    nova_despesa = definir_despesa_apartir_despesa_recorrente(request, 
                                                                                todas_despesas, 
                                                                                recorrente,
                                                                                _mes,
                                                                                proximo_ano)

        despesas = recuperar_despesas_usuario(request, ano)
        dict_despesa['despesas'] = despesas
        despesas_futura = recuperar_despesas_futura_usuario(request, ano)
        dict_despesa['despesas_futura'] = despesas_futura

    return dict_despesa

# Definir valores para template
def definir_valores_despesa_template(request, ano=datetime.date.today().year):
    dict_despesa = {}
        
    ano_atual = datetime.date.today().year
    dia_atual = datetime.date.today().day

    # Caso o ano de pesquisa seja maior do que o ano atual
    # Entao nao existirao despesas realizadas!
    if int(ano) > ano_atual:
        dict_despesa['despesas'] = []
    else:
        despesas = recuperar_despesas_usuario(request, ano)

        if not despesas:
            ano = datetime.date.today().year # Se nao existirem despesas para o ano selecionado, define o ano atual

        dict_despesa['despesas'] = despesas
        
    despesas_futura = recuperar_despesas_futura_usuario(request, ano)
    dict_despesa['despesas_futura'] = despesas_futura

    # Adiciona despesas recorrentes caso existam
    if int(ano) == ano_atual:
        # Junta as duas listas para verificacao de despesas recorrentes
        todas_despesas = list(chain(despesas, despesas_futura))
        dict_despesa = adicionar_despesas_recorrentes(request, dict_despesa, todas_despesas, int(ano))
    
    total_despesa_mes = recuperar_total_despesa_usuario_mes(request, ano)
    if total_despesa_mes['vl_despesa__sum'] == None:
        total_despesa_mes['vl_despesa__sum'] = 0.0
    dict_despesa['total_mes'] = total_despesa_mes
    
    total_despesa_ano = recuperar_total_despesa_usuario_ano(request, ano)
    if total_despesa_ano['vl_despesa__sum'] == None:
        total_despesa_ano['vl_despesa__sum'] = 0.0    
    dict_despesa['total_ano'] = total_despesa_ano

    total_despesa_futura_ano = recuperar_total_despesa_futura_usuario_ano(request, ano)
    if total_despesa_futura_ano['vl_despesa__sum'] == None:
        total_despesa_futura_ano['vl_despesa__sum'] = 0.0    
    dict_despesa['total_futura_ano'] = total_despesa_futura_ano
    
    anos_despesa = recuperar_anos_despesa(request)
    dict_despesa['anos'] = anos_despesa
        
    # Verifica se o ano atual esta presente na lista, caso contrario, adiciona
    ano_atual_aux = datetime.date.today().year
    if int(ano_atual_aux) not in dict_despesa['anos']:
        dict_despesa['anos'].insert(0, int(ano_atual_aux)) # Adiciona novo elemento na primeira posicao
   
    form = DespesaForm()
    form.fields['cd_tipo_despesa'].queryset = recuperar_todos_tipo_despesa_usuario(request)
    dict_despesa['form'] = form
    
    dict_despesa['ano_atual'] = ano
    
    dict_despesa['futura'] = False
    
    return dict_despesa
