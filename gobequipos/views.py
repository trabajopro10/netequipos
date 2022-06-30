# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse 
from django.shortcuts import render
from django.template import Template, Context
from django.conf import settings
from gobequipos.models import Eqpconectados, Tablelog, Empresa
from django.db.models import Q, Max
from django.utils import timezone
from datetime import date
import datetime 

""" Administrar las conexiones de los equipos """
import sqlite3 
import psycopg2 
import os       
import sys
import platform 
from datetime import datetime, timedelta  
from django.conf.urls.static import static 
import time
                                           
from time import sleep              
""" GUARDA EN VARIABLES LAS IMÁGENES QUE UTILIZA EN LAS TABLAS   """
offServicio="EquipoFuera.gif"
upServicio="EquipoActivo.gif"
offServerimg="EquipoServerFuera.gif"
upServerimg="EquipoServer.gif"
offEquipoAct="EquipoActivoDown.gif"
upEquipoAct="EquipoActivoUp.gif"
offEquiraAct="RadioActivoDown.png"
upEquiraAct="RadioActivoUp.png"
upEquiNasAct="nasStorageUp.gif"
offEquiNasAct="nasStorageOff.jpg"
fechaHoyBitacora="AHOY.gif"
fechaDiaspasados="diaspasados.png"
masde10latencias="AHOYMAS.gif"

""" CLASE CONEXIÓN BASE DE DATOS EQUIPOS PARA FUNCIONALIDADES COMPLICADAS DE HACER CON get o filter   """
class conectar():
	def __init__(self,dbDatos,dbUser, dbClave):
		self.__dbDatos = dbDatos
		self.__dbUser = dbUser
		self.__dbClave = dbClave

	""" CONECTAR LA BASE DE DATOS """
	def conectar(self):
		return psycopg2.connect(database=self.__dbDatos, user=self.__dbUser, password=self.__dbClave)

""" ACTUALIZAR TABLA Eqpconectados E INSERTAR EN LA TABLA Tablelog REGISTROS DE BITACORA  QUE SUCEDAN DE LOS MOVIMIENTOS DE CONECTIVIDAD  """
def ipconectequipos(request):
                agrega="S"
                strNomEquipo=""
                intEstado=0
                txtEstado=" Equipo Activo.. "
		""" LE QUITA A LA HORA DEL SISTEMA 5 HORAS, DE ESTA FORMA TENEMOS LA FECHA current, DEBIDO A QUE SE UTILIZÓ LA VARIABLE DEL SISTEMA Y SIEMPRE DABA 
                    CINCO HORAS MÁS QUE LA HORA ACTUAL   """
		FechaCurrent= datetime.utcnow()-timedelta(hours=5)

		""" MATRIZ DONDE SE GUARDARÁN LOS DATOS DE LOS EQUIPOS CONECTADOS """
                equipomtx = [ [0 for columna in range(0,20)] for fila in range (0,20)]
                nuFila=0
       	
		""" CONEXIÓN A LA  BASE  DE  DATOS """
		conectaDB=conectar('equipos','postgres','hola123456')
	        """ ACTUALIZA LA TABLA DE log CON LA IMAGEN DE NOVEDAD CURRENT O DÍAS PASADOS """                                 
		def tablelogupdate(imagenFechaEvento):
	            try:
			cn = conectaDB.conectar()
                	miCursor=cn.cursor()
			miCursor.execute("update gobequipos_tablelog set evento = '" + imagenFechaEvento + "' where FechaNove::date = now()::date;")
			miCursor.execute("update gobequipos_tablelog set evento = '" + fechaDiaspasados +  "' where FechaNove::date != now()::date;")
                        cn.commit()
                	cn.close()
                    except sqlite3.OperationalError:
                        print("Base bloqueada para insertar") 

		""" LA FUNCIÓN equipoactualiza ACTUALIZA LOS REGISTROS DE LOS EQUIPOS CONECTADOS CON LA IMAGEN DE SI ESTÁN EN LÍNEA O  NO """
                def equipoactualiza(pserver, pdireccion,pintEstado, pimgEstado, pImgequipo):
		    Eqpconectados.objects.filter(Q(equipo=pserver) | Q(direccionipv4=pdireccion)).update(estado=pintEstado, imgestado=pimgEstado, imagen = pImgequipo)		
		    Empresa.objects.filter(Q(idempresa=1)).update(emprfecha=FechaCurrent)		


		""" INSERTAR REGISTROS DE CUANDO EL EQUIPO NO RESPONDA EN LA RED   """	
		def tableloginserta(nuidlog,pequipo, pdiripv4, pdiripv6,FechaFallo,FechaRecupera,imagenFechaEvento):
			"""print("Hola Mensaje",pequipo, pdiripv4, pdiripv6,FechaFallo,FechaRecupera,imagenFechaEvento)"""
			tablelog = Tablelog.objects.create(idlog=nuidlog,equipo=pequipo,direccionipv4_id=pdiripv4,direccionipv6=pdiripv6,fechanove=FechaFallo,fecharecup=FechaRecupera,evento=imagenFechaEvento)


		""" HACE EL PING AL EQUIPO Y TIENE LA OPCIÓN DE VALIDAR SI ES Windows o Linux  """
                if (platform.system()=="Windows"):
                    ping = "ping -n 1 -i 5"
                else :
                    ping = "ping -c 1 -i 5"

		""" GUARDA LOS DATOS DEL EQUIPO EN LA MATRIZ equipomtx, A MEDIDA QUE SE RECORRE EL For CON LOS EQUIPOS PARA AVERIGUAR SI RESPONDE   """
		for valor in Eqpconectados.objects.filter(Q(sensar='t')).exclude(equipo='-').values_list():
       		    strNomEquipo=list(valor)[0]
       		    direccionipv4=list(valor)[1]
       		    direccionipv6=list(valor)[2]
       		    estado=list(valor)[6]
       		    imagen=list(valor)[7]
       		    imgestado=list(valor)[7]
       		    TipoEquipo=list(valor)[5]
       		    descripcion=list(valor)[3]
                    #print("DATOS .....",strNomEquipo,direccionipv4, direccionipv6, TipoEquipo)			    
                    equipomtx[nuFila][1]=strNomEquipo
                    equipomtx[nuFila][2]=direccionipv4
                    equipomtx[nuFila][3]=direccionipv6
                    equipomtx[nuFila][5]=imagen
                    equipomtx[nuFila][6]=imgestado
                    equipomtx[nuFila][7]=estado
                    equipomtx[nuFila][8]=descripcion

		    """ SE HACE EL PING Y SE GUARDA LA RESPUESTA  """
                    response = os.popen(ping+" "+direccionipv4)

                    intEstado=0
                    imgEstado=offServicio
                    equipoactualiza(strNomEquipo,direccionipv4,intEstado,imgEstado,offServerimg)

		    """ SE VALIDA LA RESPUESTA DEL PING PARA SABER SI ESTÁN EN LÍNEA O NO    """
                    nuFila+=1
                    for line in response.readlines():
                        if ("ttl" in line.lower() ):
                            intEstado=1
                        imgEstado = offServicio if intEstado == 0 else upServicio
			
			""" COLOCA LA IMAGEN DE ACTIVO O INACTIVO, DEPENDIENDO DE LA RESPUESTA QUE DE EL EQUIPO EN EL PING  """
                        if (TipoEquipo == 'eqpse'):
                            imgEquipo = offServerimg if intEstado == 0 else upServerimg
                        elif  (TipoEquipo == 'eqpac'):
                            imgEquipo = offEquipoAct if intEstado == 0 else upEquipoAct
                        elif  (TipoEquipo == 'eqpna'):
                            imgEquipo = offEquiNasAct  if intEstado == 0 else upEquiNasAct     
                        else: imgEquipo = offEquiraAct if intEstado == 0 else upEquiraAct
                        #print('EQUIPOACTUALIZA..',strNomEquipo,direccionipv4,intEstado,imgEstado, imgEquipo)
                        equipoactualiza(strNomEquipo,direccionipv4,intEstado,imgEstado, imgEquipo)

		    """ INSERTA EL REGISTRO EN LA TABLA DE LOG SI HAY UNA LATENCIA  """	
		    if intEstado==0:
		    	idtablelog = Tablelog.objects.aggregate(Max('idlog'))
			tableloginserta((idtablelog['idlog__max'] + 1),strNomEquipo, direccionipv4, direccionipv6, FechaCurrent, FechaCurrent,fechaHoyBitacora)
		    """ SE ENVÍA ESTE PROCEDIMIENTO SIEMPRE POR FUERA DEL IF, PORQUE AL DÍA SIGUIENTE SE QUEDAN REGISTROS COMO SI FUERAN DEL DÍA ACTUAL Y NO SE ACTUALIZAN 
                        HASTA QUE HAYA UNA NOVEDAD DEL DIA ACTUAL, SE VE MAL, POR ESO SIEMPRE SE ENVÍA PARA QUE HAGA LA VALIDACIÓN  """
		    tablelogupdate(fechaHoyBitacora)

		""" SOLO ENVÍA LA FECHA ACTUAL PARA MOSTRAR EN PANTALLA EN LA PLANTILLA  plneinicio.html """ 		                
		return render(request,'plneinicio.html',{"Fecha":FechaCurrent,})


""" *********  HACE EL PROCESO DE CONSULTAR EN LA BASE DE DATOS, NO ACTUALIA O INSERTA DATOS EN NINGUNA TABLA *********** """
def ipequiposonline(request):

		strTituloLog=""
		conectaDB=conectar('equipos','postgres','hola123456')
		cn = conectaDB.conectar()
               	miCursor=cn.cursor()

		"""SE CONSULTAN TODOS LOS REGISTROS DE LA TABLA tablelog, PARA COLOCAR EL INDICE FINAL A LA MATRIZ QUE GUARDARÁ LOS REGISTROS QUE SE MOSTRARÁN EN LA 
		BITACORA POR PANTALLA """
 		miCursor.execute("select count(*) from (Select equipo,(fechanove)::date As FechaNovedad, evento, count(*) As Latencias from gobequipos_tablelog group by equipo ,(fechanove)::date, evento order by count(*) desc ) as total;")
		#Tablelog.objects.filter(Q(equipo,fechanove__date,evento,count(*))).count()
		regactu = miCursor.fetchall()
               	cn.close()
		regbitacora=list(regactu)[0][0]
		#print("Registros bitácora .." +  str(regbitacora))
                agrega="S"
                strNomEquipo=""
                eveneto=""
                intEstado=0
		strTitulo="OK_SERVERS"
		intEstadoCero=0  
                txtEstado=" Equipo Activo.. "
                equipomtx = [ [0 for columna in range(0,20)] for fila in range (0,25)]
                """ EL INDICE MAS CINCO LÍNEAS MAS """
                equipolog = [ [0 for columna in range(0,20)] for fila in range (0,int(regbitacora)+5)]
                nuFila=0
                nuFilalog=0
		nuMinutos=0
		""" SE COLOCA LA HORA DEL SISTEMA Y LUEGO SE RESTAN CINCO,DEBIDO A QUE AL COLOCAR LA VARIABLE DEL SISTEMA CON LA HORA
                    FUE IMPOSIBLE QUE FUNCIONARA CON LA HORA ACTUAL  """
		FechaCurrent= datetime.now() - timedelta(hours=5)

		cn = conectaDB.conectar()
               	miCursor=cn.cursor()
                
		""" fcontexto, ENVÍA AL FRONTEND LOS DATOS PARA SER DESPLEGADOS POR LA PLANTILLA plnetequipos.html """	
		def fcontexto (datosequipos,Estado,Ruta,FechaActual,EstadoCero,elTitulo,datosBitacora,bitacoraTitulo):
                	return render(request,'plnetequipos.html',{"Equipos":datosequipos,"Estadoepq":Estado,"Path":Ruta,"Fecha":FechaActual,"RegCero":EstadoCero,"Titulo":elTitulo,"Bitacora":datosBitacora,"TituloBitacora":bitacoraTitulo,})
		
		try:
			""" SI HA PASADO MAS DE UN MINUTO SIN ACTUALIZAR LA TABLA EMPRESA, NO SE ACTUALIZA MAS LAS TABLAS DE LA BASE DE DATOS 
                            Y GENERA UN ERROR EN EL SITIO WEB DICIENDO QUE HAY UN ERROR Y QUE EL PROCESO NO ESTA EN LINEA O TRABAJANDO """
			miCursor.execute("Select extract(minute from current_timestamp)::int - extract(minute from emprfecha)::int AS minutos From gobequipos_empresa ")  
			regactu = miCursor.fetchall()
			nuMinutos=list(regactu)[0][0]
		except sqlite3.OperationalError:
			print("Error en consulta fecha en Empresa ..")
	        print (" Vlor de los minutos ", nuMinutos)	
		if  int(nuMinutos) >=2:
			print("Error de proceso, no esta actualizando la tabla de Empresa..")
               		cn.close()
			strTitulo="ERROR NO ESTA  ACTUALIZANDO"
                	return HttpResponse(fcontexto(equipomtx,txtEstado,sys.path[0],FechaCurrent,intEstadoCero,strTitulo,equipolog,strTituloLog))       
		else:
               		""" SI EL PROCESO CONTINUA SIN PROBLEMAS LLEVA LOS REGISTROS A LA MATRIZ equipomtx, LOS DATOS DE LA TABLA eqpconectados --> EQUIPOS EN LINEA """  
       		        filas= miCursor.fetchall()
                	#for valor in Eqpconectados.objects.all().filter(sensar='t').values_list():
			for valor in Eqpconectados.objects.filter(Q(sensar='t')).exclude(equipo='-').values_list():
       		        	strNomEquipo=list(valor)[0]
       		             	direccionIpv4=list(valor)[1]
       		             	direccionipv6=list(valor)[2]
       		             	estado=list(valor)[6]
       		             	imagen=list(valor)[7]
       		             	imgestado=list(valor)[7]
       		             	TipoEquipo=list(valor)[5]
       		             	descripcion=list(valor)[3]
                   		#print ('CAMPOS ..',strNomEquipo,direccionIpv4, direccionipv6,'Esatado -->', estado, imagen, imgestado, TipoEquipo, descripcion)
       		             	nuFila+=1
               		     	equipomtx[nuFila][1]=strNomEquipo
                    		equipomtx[nuFila][2]=direccionIpv4
                    		equipomtx[nuFila][3]=direccionipv6
                    		equipomtx[nuFila][5]=imagen
                    		equipomtx[nuFila][6]=imgestado
                    		equipomtx[nuFila][7]=estado
                    		equipomtx[nuFila][8]=descripcion
                   		#print ('CAMPOS EquipoMtx..',equipomtx[1],equipomtx[2],equipomtx[3],equipomtx[5],equipomtx[6],'Estado --> ',equipomtx[7],equipomtx[8])
                   		#print ('CAMPOS EquipoMtx..','Estado --> ',equipomtx[7])

		    		#if (equipomtx[nuFila][7]==0):
				#print ('Es el estado --> ',estado)
		    		if (estado==0):
					intEstadoCero+=1  
					strTitulo="!!PROBLEMAS_SERVERS!!"

		""" SE CONECTA A LA BASE DE DATOS Y HACE UNA CONSULTA PARA CADA EQUIPO DE CUANTAS LATENCIAS HA TENIDO Y LAS ACUMULA PARA MOSTRAR EN PANTALLA 
                    LA FECHA Y LOS REGISTROS ACUMULADOS PARA ESE EQUIPO   """
	     	try:
			cn = conectaDB.conectar()
               		miCursor=cn.cursor()
			miCursor.execute("Select equipo,(fechanove)::date As FechaNovedad, evento As Evento, count(*) As Latencias from gobequipos_tablelog  group by equipo ,(fechanove)::date, evento order by evento asc,(fechanove)::date desc,count(*) desc;")
			#print ('FILAS... --> ', filas)
       	      		filas= miCursor.fetchall()
               		cn.close()
              	except sqlite3.OperationalError:
               		print("Base bloqueada para consulta") 
       		for fila in filas:
       	 		strNomEquipo=list(fila)[0]
       		   	fechanovedad=list(fila)[1]
       		   	evento=list(fila)[2]
       		   	latencias=list(fila)[3]
                   	""" SE GUARDAN LOS REGISTROS EN LA TABLA DE BITACORA Y SE COLOCA UNA MARCA DE fechaHoyBitacora PARA LATENCIAS DEL DÍA current, 
			    Y SE COLOCA UNA MARCA EN ROJO A LOS REGISTROS QUE TIENEN MAS DE 10 LATENCIAS EN DÍA current   """
       		   	nuFilalog+=1
			"""print("nuFilalog .." + str(nuFilalog))"""
               	   	equipolog[nuFilalog][1]=strNomEquipo
                   	equipolog[nuFilalog][2]=fechanovedad
			if (latencias >= 10 and evento==fechaHoyBitacora):
                   		equipolog[nuFilalog][3]=masde10latencias
			else:
                   		equipolog[nuFilalog][3]=evento
                   	equipolog[nuFilalog][4]=latencias
			
		#print('EquipoLog --> ',equipolog[nuFilalog][3])
	     	if (equipolog[nuFilalog][3]==0):
			intEstadoCero+=1  
			strTitulo="!!NO HAY LATENCIAS  DE CONECTIVIDAD......, QUE COSA RARA!!"

                """ SE LLAMA LA FUNCIÓN fcontexto SE ENCARGA DE LLEVAR LOS DATOS A LA PLATILLA plnetequipos.html  """
	        #print ('EQUIPO MTX',equipomtx)
               	return HttpResponse(fcontexto(equipomtx,txtEstado,sys.path[0],FechaCurrent,intEstadoCero,strTitulo,equipolog,strTituloLog))
