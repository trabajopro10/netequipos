# -*- coding: utf-8 -*-
from __future__ import unicode_literals

'''from django.apps import AppConfig'''
from django.contrib.admin.apps import AdminConfig


'''class GobequiposConfig(AppConfig):
    name = 'gobequipos' '''

class GobequiposAdminConfig(AdminConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    default_site = 'admin.NetequiposAdminSite'
    name = 'gobequipos'
