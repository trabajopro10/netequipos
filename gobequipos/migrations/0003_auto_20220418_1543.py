# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2022-04-18 15:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gobequipos', '0002_auto_20220417_1647'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Empresa',
        ),
        migrations.RemoveField(
            model_name='tablelog',
            name='direccionIpv4',
        ),
        migrations.DeleteModel(
            name='Eqpconectados',
        ),
        migrations.DeleteModel(
            name='Tablelog',
        ),
    ]
