# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.admin import AdminSite

# Register your models here.
from gobequipos.models import Empresa, Eqpconectados, Tablelog

from csv import list_dialects
from re import search
from pkg_resources import ResourceManager

class NetequiposAdminSite(AdminSite):
    title_header = 'Equipos Gobernacion Quindio'
    site_header = 'Administración Equipos Gobernacion Quindio'
    index_title = 'Sitio admin Gobernacion Quindio'

admin_site = NetequiposAdminSite(name='netequipos')

class EmpresaAdmin(admin.ModelAdmin):
    list_display =('idempresa','emprfecha','emprdesc','empimage',)

class EqpconectadosAdmin(admin.ModelAdmin):
    search_fields= ['equipo','tipoequipo','imagen',]
    list_display =('equipo','direccionipv4','direccionipv6','estado','imagen','imgestado','tipoequipo','descripcion','sensar',)

class TablelogAdmin(admin.ModelAdmin):
    search_fields = ['equipo','direccionipv4','fechanove']

admin.site.register(Empresa,EmpresaAdmin)
admin.site.register(Eqpconectados,EqpconectadosAdmin)
admin.site.register(Tablelog)
