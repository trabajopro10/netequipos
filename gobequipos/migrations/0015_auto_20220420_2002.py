# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2022-04-20 20:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gobequipos', '0014_auto_20220418_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tablelog',
            name='fechanove',
            field=models.DateField(verbose_name='Fecha Novedad'),
        ),
        migrations.AlterField(
            model_name='tablelog',
            name='fecharecup',
            field=models.DateField(verbose_name='Fecha Recuperaci\xf3n'),
        ),
    ]
