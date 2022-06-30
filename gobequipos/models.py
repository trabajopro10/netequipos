# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your models here.
from operator import mod
from tabnanny import verbose
from django.db import models
#from ckeditor.fields import RichTextField  # Facilita colocar un editor de texto completo con todas sus opciones 

# Create your models here.


class Empresa(models.Model):
        idempresa=models.IntegerField('Id Empresa',primary_key=True, help_text='Identificación de la Empresa')
        emprfecha=models.DateTimeField('Fecha',help_text='Fecha actualizada en la tabla Empresa')
        emprdesc=models.CharField('Descripcion',max_length=60, help_text='Descripción de la Empresa')
        empimage=models.CharField('Imagen',max_length=60, help_text='Imágen que identifica la Empresa')
        
        def __str__(self):
                return 'Id_Empresa %s Fecha %s Descripcion %s RutaImagen %s' % (self.idempresa, self.emprfecha, self.emprdesc, self.empimage) 
	
class Eqpconectados(models.Model):
        equipo=models.CharField('Equipo',max_length=60, help_text='Nombre del Equipo')
        direccionipv4=models.CharField('DireccionIpv4',max_length=60, primary_key=True, help_text='Dirección IPV4 4 octetos')
        direccionipv6=models.CharField('DireccionIpv6',max_length=60, help_text='Dirección IPV6 8 octetos')
        estado=models.IntegerField('Estado',default=1,help_text='El estado en <0> cuando el equipo no contesta y <1> si esta bien')
        imagen=models.CharField('Imagen',max_length=100, help_text='Imágen del equipo')
        imgestado=models.CharField('Imagen de Estado',max_length=100, help_text='Imágen que muestra el estado Ok o con problemas')
        tipoequipo=models.CharField('Tipo Equipo',default='-',max_length=10, help_text='Identificación interna del tipo ')
        descripcion=models.CharField('Descripción',max_length=100, help_text='Descripción breve del equipo ')
        sensar=models.BooleanField('Sensar Equipo',default=True, help_text='Está en True para que se muestre por patalla')
        
        class Meta:
            ordering = ['equipo']
	
        LOAN_TIPOEQUIPO = (
            ('eqpse', 'Equipos Server'),
            ('eqpna', 'Equipos NAS'),
            ('eqpac', 'Equipos ACTIVOS'),
            ('eqpra', 'Equipos RADIOS'),
        )
        
        tipoequipo = models.CharField(
            max_length=6,
            choices=LOAN_TIPOEQUIPO,
            blank=True,
            default='-',
            help_text='Tipo de equipo a Sensar',
        )

        LOAN_ESTADO = (
            (1, 'Equipo Sensado OK'),
            (0, 'Equipos NAS'),
        )
        
        estado = models.IntegerField(
            choices=LOAN_ESTADO,
            blank=True,
            default=1,
            help_text='Estado equipo Ok o NoOk',
        )

        LOAN_IMAGEN = (
            ('EquipoActivoUp.gif', 'EQUIPO ACTIVO'),
            ('nasStorageUp.gif', 'EQUIPO NAS'),
            ('EquipoServer.gif', 'EQUIPO SERVER'),
            ('RadioActivoUp.png', 'EQUIPO RADIO'),
	    )           

        imagen = models.CharField(
            max_length=30,
            choices=LOAN_IMAGEN,
            blank=True,
            default='-',
            help_text='Imagen de Equipo',
        )

        LOAN_IMGESTADO = (
            ('EquipoActivoUp.gif', 'EQUIPO ACTIVO'),
            ('nasStorageUp.gif', 'EQUIPO NAS'),
            ('EquipoServer.gif', 'EQUIPO SERVER'),
            ('RadioActivoUp.png', 'EQUIPO RADIO'),
	    )        

        imgestado = models.CharField(
            max_length=30,
            choices=LOAN_IMGESTADO,
            blank=True,
            default='-',
            help_text='Imagen de Estado Equipo',
        )

        def __str__(self):
                return 'Equipo %s DirIpv4 %s DirIpv6 %s Estado %s RutaImagen %s RutaImagenEst %s TipoEquipo %s Descripcion %s Sensar %s' % (self.equipo, self.direccionipv4, self.direccionipv6, self.estado, self.imagen , self.imgestado, self.tipoequipo, self.descripcion, self.sensar)

class Tablelog(models.Model):
        idlog=models.IntegerField('Id registro',help_text='Id registro en la tabla',primary_key=True)
        equipo=models.CharField('Equipo',max_length=60)
        direccionipv4=models.ForeignKey(Eqpconectados, on_delete=models.CASCADE)
        direccionipv6=models.CharField('Direccion IPv6',max_length=60)
        fechanove=models.DateTimeField('Fecha Novedad')
        fecharecup=models.DateTimeField('Fecha Recuperación')
        evento=models.CharField('Evento ',max_length=60, help_text='Evento')
        
        class Meta:
            ordering = ['fechanove']
        
        def get_absolute_url(self):
            return reversed('equipo-log', args=[str(self.idlog)])
        
        def __str__(self):
                return 'Equipo %s DirIpv4 %s DirIpv6 %s FechaNovedad %s Evento %s' % (self.equipo, self.direccionipv4, self.direccionipv6, self.fechanove, self.evento)
