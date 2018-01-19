from django.contrib import admin
from sisdespenda.models import DespesaTbl, EventoTbl, RendaTbl, TipoRendaTbl, TipoDespesaTbl, RecorrenciaDespesaTbl

admin.site.register(DespesaTbl)
admin.site.register(EventoTbl)
admin.site.register(RendaTbl)
admin.site.register(TipoRendaTbl)
admin.site.register(TipoDespesaTbl)
admin.site.register(RecorrenciaDespesaTbl)