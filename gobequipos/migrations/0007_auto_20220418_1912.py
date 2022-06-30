# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2022-04-18 19:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gobequipos', '0006_auto_20220418_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eqpconectados',
            name='estado',
            field=models.IntegerField(blank=True, choices=[(1, 'Equipo sensado OK'), (0, 'Equipo No sensado OK')], default='-', help_text='Equipo en Linea o no ', max_length=2),
        ),
    ]
