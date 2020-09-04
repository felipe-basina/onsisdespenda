from django.conf.urls import url
from django.contrib import admin
from sisdespenda.views.saldo import saldo
from sisdespenda.views.evento import evento
from sisdespenda.views.despesa import despesa
from sisdespenda.views.renda import renda
from sisdespenda.views.relatorio import relacao_relatorio
from sisdespenda.views.renda.relatorio import renda_relatorio
from sisdespenda.views.despesa.relatorio import despesa_relatorio
from sisdespenda.views.despesa.grafico import despesa_grafico
from sisdespenda.views.recorrencia import recorrencia_despesa
from sisdespenda.views.tipos.despesa import tipo_despesa
from sisdespenda.views.tipos.renda import tipo_renda
from sisdespenda.views.entrypoint import inicial, login_logout

urlpatterns = [
    url(r'^onsisdespenda/acc/admin/', admin.site.urls),
    url(r'^$', inicial.inicio, name='inicio'),
	url(r'^accounts/login/$', login_logout.login_req, name='login_req'),
	url(r'^entrar/$', login_logout.login_user),
    url(r'^logout/$', login_logout.logout_user),
    url(r'^tipo/lista$', tipo_renda.tipo_renda_list, name='tipo_renda_list'),
    url(r'^tipo/novo/$', tipo_renda.tipo_renda_new, name='tipo_renda_new'),
    url(r'^tipo/novo/(?P<pk>\d+)$', tipo_renda.tipo_renda_update, name='tipo_renda_update'),
    url(r'^tipo/editar/(\d+)$', tipo_renda.tipo_renda_edit, name='tipo_renda_edit'),
    url(r'^tipo/despesa/lista$', tipo_despesa.tipo_despesa_list, name='tipo_despesa_list'),
    url(r'^tipo/despesa/novo/$', tipo_despesa.tipo_despesa_new, name='tipo_despesa_new'),
    url(r'^tipo/despesa/novo/(?P<pk>\d+)$', tipo_despesa.tipo_despesa_update, name='tipo_despesa_update'),
    url(r'^tipo/despesa/editar/(\d+)$', tipo_despesa.tipo_despesa_edit, name='tipo_despesa_edit'),
    url(r'^renda/lista$', renda.renda_list, name='renda_list'),
    url(r'^renda/novo/$', renda.renda_new, name='renda_new'),
    url(r'^renda/novo/(?P<pk>\d+)$', renda.renda_update, name='renda_update'),
    url(r'^renda/editar/(\d+)$', renda.renda_edit, name='renda_edit'),
    url(r'^renda/lista/ano/(\d+)$', renda.renda_list_param, name='renda_list_param'),
    url(r'^renda/remove/(?P<pk>\d+)$', renda.renda_remove, name='renda_remove'),
    url(r'^recorrencia/despesa/lista$', recorrencia_despesa.recorrencia_despesa_list, name='recorrencia_despesa_list'),
    url(r'^recorrencia/despesa/novo/$', recorrencia_despesa.recorrencia_despesa_new, name='recorrencia_despesa_new'),
    url(r'^recorrencia/despesa/novo/(?P<pk>\d+)$', recorrencia_despesa.recorrencia_despesa_new, name='recorrencia_despesa_new'),
    url(r'^recorrencia/despesa/remove/(?P<pk>\d+)$', recorrencia_despesa.recorrencia_despesa_remove, name='recorrencia_despesa_remove'),
    url(r'^despesa/lista$', despesa.despesa_list, name='despesa_list'),
    url(r'^despesa/novo/$', despesa.despesa_new, name='despesa_new'),
    url(r'^despesa/novo/(?P<pk>\d+)$', despesa.despesa_update, name='despesa_update'),
    url(r'^despesa/editar/(\d+)$', despesa.despesa_edit, name='despesa_edit'),
    url(r'^despesa/lista/ano/(\d+)$', despesa.despesa_list_param, name='despesa_list_param'),
    url(r'^despesa/remove/(?P<pk>\d+)$', despesa.despesa_remove, name='despesa_remove'),
    url(r'^despesa/grafico/mes/ano/$', despesa_grafico.despesa_grafico_mes_ano, name='despesa_grafico_mes_ano'),
    url(r'^despesa/grafico/mes/ano/(\d+)$', despesa_grafico.despesa_grafico_mes_ano, name='despesa_grafico_mes_ano'),
    url(r'^despesa/grafico/ano/$', despesa_grafico.despesa_grafico_ano, name='despesa_grafico_ano'),
    url(r'^despesa/grafico/ano/(\d+)$', despesa_grafico.despesa_grafico_ano, name='despesa_grafico_ano'),
    url(r'^despesa/grafico/mes/ano/(\d+)/(\d+)$', despesa_grafico.despesa_grafico_mes_ano, name='despesa_grafico_mes_ano'),
    url(r'^despesa/relatorio/mes/ano$', despesa_relatorio.despesas_realizadas_mes_ano, name='despesas_realizadas_mes_ano'),
    url(r'^despesa/relatorio/mes/ano/(\d+)$', despesa_relatorio.despesas_realizadas_mes_ano_param, name='despesas_realizadas_mes_ano_param'),
    url(r'^despesa/relatorio/ano$', despesa_relatorio.despesas_realizadas_ano, name='despesas_realizadas_ano'),
    url(r'^renda/relatorio/mes/ano$', renda_relatorio.rendas_realizadas_mes_ano, name='rendas_realizadas_mes_ano'),
    url(r'^renda/relatorio/mes/ano/(\d+)$', renda_relatorio.rendas_realizadas_mes_ano_param, name='rendas_realizadas_mes_ano_param'),
    url(r'^renda/relatorio/ano$', renda_relatorio.rendas_realizadas_ano, name='rendas_realizadas_ano'),
    url(r'^relacao/relatorio/mes/ano$', relacao_relatorio.relacao_mes_ano, name='relacao_mes_ano'),
    url(r'^relacao/relatorio/mes/ano/(\d+)$', relacao_relatorio.relacao_mes_ano_param, name='relacao_mes_ano_param'),
    url(r'^relacao/relatorio/ano$', relacao_relatorio.relacao_ano, name='relacao_ano'),
    url(r'^evento/mes/ano$', evento.evento_list, name='evento_list'),
    url(r'^evento/mes/ano/(\d+)$', evento.evento_list_param, name='evento_list_param'),
    url(r'^saldo/lista$', saldo.saldo_list, name='saldo_list'),
    url(r'^nova/senha$', login_logout.set_user_password_form, name='set_user_password_form'),
    url(r'^altera/senha/$', login_logout.change_user_password, name='change_user_password'),
]