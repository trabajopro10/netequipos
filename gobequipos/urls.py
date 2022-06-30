from gobequipos import views
from django.conf.urls import url

from gobequipos import views
from django.contrib import admin

urlpatterns = [
    url('vipequiposonline/',views.ipequiposonline),
    url('vnipconectequipos/',views.ipconectequipos),
]
