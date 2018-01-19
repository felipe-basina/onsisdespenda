# -*- coding: utf-8 -*-
from django.http import *
from django.shortcuts import render
from django.utils.timezone import utc
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db import connection
from collections import namedtuple
from ..models import RecorrenciaDespesaTbl, TipoDespesaTbl
from ..models import RecorrenciaDespesaForm
import datetime
import itertools

@login_required(login_url='/accounts/login/')
def recorrencia_despesa_list(request):
    dict_recorrencia_despesa = {}#definir_valores_despesa_template(request)
    dict_recorrencia_despesa['form'] = RecorrenciaDespesaForm()
    return render(request, 'onsis/recorrencia_despesa_list.html', { 'template': dict_recorrencia_despesa })