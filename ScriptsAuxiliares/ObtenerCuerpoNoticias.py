#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unicodedata
import tweepy
import json
import codecs
import os
import signal
import time
import random
import requests
from multiprocessing import Queue
import re
import math
import sys

#Descriptores de archivos auxiliares
STOPWORDS_LIST = "ScriptsAuxiliares/stopwords.txt"

# Descriptores de archivos de contenidos
TN = "ScriptsAuxiliares/Archivos/TodoNoticias.txt"
CLARIN = "ScriptsAuxiliares/Archivos/Clarin.txt"
LA_NACION = "ScriptsAuxiliares/Archivos/LaNacion.txt"
PAGINA_DOCE = "ScriptsAuxiliares/Archivos/PaginaDoce.txt"
LA_IZQUIERDA = "ScriptsAuxiliares/Archivos/LaIzquierda.txt"

#Descriptores de archivos para corpus de palabras
CORPUS_RING_1_TN = "ScriptsAuxiliares/Corpus/Ring1/TodoNoticias.txt"
CORPUS_RING_1_CLARIN = "ScriptsAuxiliares/Corpus/Ring1/Clarin.txt"
CORPUS_RING_1_LA_NACION = "ScriptsAuxiliares/Corpus/Ring1/LaNacion.txt"
CORPUS_RING_1_PAGINA_DOCE = "ScriptsAuxiliares/Corpus/Ring1/PaginaDoce.txt"
CORPUS_RING_1_LA_IZQUIERDA = "ScriptsAuxiliares/Corpus/Ring1/LaIzquierda.txt"
CORPUS_RING_2 = "ScriptsAuxiliares/Corpus/Ring2/CorpusGlobal.txt"


#Creacion de conjunto de stopwords
stopwords= set()

with open(STOPWORDS_LIST) as f:
	stopwords = f.read().splitlines()
	stopwords = [re.sub("[\s]","",w) for w in stopwords ]
	#for line in f:
	#	stopwords.add(line[:-1])

def isStopword(word):
	return (word.lower() in stopwords) or (word.lower().startswith("no_") and word[3:].lower() in stopwords) or (len(word)<2) or (word.lower().startswith("no_") and len(word[3:])<2)

#elimina_tildes(texto)
#Recibe un texto y devuelve el mismo pero sin tildes
def elimina_tildes(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

#limpiezaHTMLGral(contenido_en_html)
#Recibe un texto HTML y  retorna el mismo pero habiendo
#elminado sus tags y remplazado los links por su descripciones
def limpiezaHTMLGral(contenido):
	#Remplazo los links por su descripcion
	patron=re.compile("<a href=[^>]+>")
	contenido=patron.sub(" ",contenido)
	patron=re.compile("</a>")
	contenido=patron.sub(" ",contenido)
	
	#Limpio los tags html
	patron=re.compile("<param[^>]*>")
	contenido=patron.sub(" ",contenido)
	patron=re.compile("</p>(<[^p][^>]*>([^<])*)*(<p>)?")
	contenido=patron.sub(" ",contenido)
	patron=re.compile("<[^>]*>")
	contenido=patron.sub(" ",contenido)
	
	return contenido
	
#remplazar(contenido)
#recibe un texto y retorna el mismo pero antecediendo a cada palabra un NO_	
def remplazar(contenido):
	patron=re.compile(" ")
	return patron.sub(" NO_",contenido)
	
#Chen(contenido_de_la_noticia)
#Recibe un texto y devuelve el mismo pero aplicandole el metodo de Chen
def Chen(contenido):
	#Encuentro las apariciones de los no y de los puntos
	nos=re.finditer('[\s|\.|\,|\;|\:|\!|\?|\"|\']no\s', contenido.lower())
	puntos = re.finditer('[\.|\,|\;|\:|\!|\?|\"|\']', contenido)
	
	#remplazo las oraciones que tienen un no por la 
	#	aplicacion del metodo de chen  de la misma
	for i in nos:
		ini= i.start()
		puntocercano=0
		for j in puntos :
			if(j.start()>ini):
				puntocercano=j.start()
				break
		remp=remplazar(contenido[ini:puntocercano])
		contenido=contenido[:ini]+remp+contenido[puntocercano:]
	return contenido
				
#limpiar_Contenido(contenido)
#limpia la cadena de todo lo que no sea relevante y aplica Chen
def limpiar_Contenido(contenido):
	
	#Elimino los links
	PATTERN_URL = "http[^\ ]*"
	PATTERN_URL_B = "www[^\ ]*"
	contenido = re.sub(PATTERN_URL,"",contenido)
	contenido = re.sub(PATTERN_URL_B,"",contenido)
	#patron=re.compile("\shttp\S+")
	#contenido= patron.sub("",contenido)
	
	#Elimino espacios dobles
	PATTERN_ESPACIOS = " +"
	contenido = re.sub(PATTERN_ESPACIOS," ",contenido)

	#Aplico Chen al texto
	contenido=Chen(contenido)
	
	#Separo el texto por los signos de puntuacion en la lista
	lista_contenido = re.split('[\.\;\:\!\?]', contenido)

	#Elimino todo caracter y digito de las unidades de texto de la lista
	PATTERN_SIGNOS_PUNTUACION = "[\.\,\;\:\!\?\"\'\&]"
	PATTERN_CARACTERES_ESPECIALES = "[^\ ]*[^a-zA-Z\_\ ][^\ ]*"
	aux = []
	for element in lista_contenido:
		element = re.sub(PATTERN_SIGNOS_PUNTUACION,"",element)
		element = re.sub(PATTERN_CARACTERES_ESPECIALES,"",element)
		aux.append(element)
		#patron=re.compile("[^(\w|\s)]")
		#element= patron.sub("",element)
		#patron=re.compile("\d+")
		#element= patron.sub("",element)
	lista_contenido = aux

	#todas las palabras qedan separadas unicamente por espacios
	#elimino las stopwords
	aux = []
	for element in lista_contenido:
		lista_element = element.split(" ")
		lista_nueva = []
		for item in lista_element:
			if not isStopword(item):
				lista_nueva.append(item)
		string = " ".join(lista_nueva)
		aux.append(string)

	lista_contenido = aux

	return lista_contenido
	
	
def recolectarNoticia(URL):
	pagina=""
	req = requests.get(URL)
	#print(req.encoding)
	req.encoding = 'utf-8'
	status_code = req.status_code
	if status_code == 200:
		pagina=req.text
	else:
		print("Error")
	return  elimina_tildes(pagina)

#detectarEntidades(contenido_de_la_noticia)
#Dado un texto (contenido de la noticia), encuentra todos sus Bigramas y Trigramas que sean Title,
#calcula la cantidad de apariciones de los mismos,y los ordena de mayor frecuencia a menor
#retorna un areglo con 2 componentes [BG,TG]
#BG:coleccion de Bigramas Title de la noticia con su frecuencia (pares (frecuencia,bigrama))
#TG:coleccion de Trigramas Title de la noticia con su frecuencia (pares (frecuencia,trigrama))	
def detectarEntidades(contenido):
	#Recolecto Bigramas y Trigramas
	bigramas=list(set(re.findall("([A-Z][a-z]+\s[A-Z][a-z]+)+",contenido)))
	#print('Bigramas Title:',bigramas)
	trigramas=list(set(re.findall("([A-Z][a-z]+\s[A-Z][a-z]+\s[A-Z][a-z]+)+",contenido)))
	#print('Trigramas Title:',trigramas)
	
	#Armo pares (frecuencia,cont)
	BG=[ (contenido.count(i),i) for i in bigramas]
	TG=[ (contenido.count(i),i) for i in trigramas]
	
	#Los ordeno segun su frecuencia
	BG.sort(reverse=True)
	TG.sort(reverse=True)
	
	#print("BG ordenado: ",BG)
	#print("TG ordenado: ",TG)
	
	
	return [BG,TG]

	
#....------------------------------------------------------------------------------------------------------------------....
#-----------------------------------------------NOTICIEROS-----------------------------------------------------------------
#....------------------------------------------------------------------------------------------------------------------....



#obtenerNoticiaNacion(URL_de_la_Noticia)
#retorna un arreglo con 3 componentes [contenido,BG,TG]
#contenido: contenido de la noticia,limpia, con aplicacion del metodo chen, todo en una linea
#BG:coleccion de Bigramas Title de la noticia con su frecuencia (ordenados de mas frecuente a menos frecuente).
#	Para obtener los Bigramas b=[i[1] for i in BG]
#	Para obtener las frecuencias f=[i[0] for i in BG]
#TG:coleccion de Trigramas Title de la noticia con su frecuencia (ordenados de mas frecuente a menos frecuente).
#	Para obtener los Trigramas t=[i[1] for i in TG]
#	Para obtener las frecuencias f=[i[0] for i in TG]

def obtenerNoticiaNacion(url):
	#Recolecto el html de la noticia
	contenido=recolectarNoticia(url)
	
	#Obtengo principio y fin del contenido de la noticia
	patron=re.compile("<p class=\"primero\">")
	ini= patron.search(contenido).end()
	patron=re.compile("<span itemprop=\"name\">LA NACION</span>")
	fin=patron.search(contenido).start()
	contenido=contenido[ini:fin]
	
	#Limpio el contenido de links y tags
	contenido=limpiezaHTMLGral(contenido)

	#Detecto trigramas y bigramas y limpio el contenido de la noticia y aplico Chen
	[BG,TG]=detectarEntidades(contenido)
	contenido= limpiar_Contenido(contenido)
	
	return [contenido,BG,TG]


#obtenerNoticiaClarin(URL_de_la_Noticia)
#retorna un arreglo con 3 componentes [contenido,BG,TG]
#contenido: contenido de la noticia,limpia, con aplicacion del metodo chen, todo en una linea
#BG:coleccion de Bigramas Title de la noticia con su frecuencia (ordenados de mas frecuente a menos frecuente).
#	Para obtener los Bigramas b=[i[1] for i in BG]
#	Para obtener las frecuencias f=[i[0] for i in BG]
#TG:coleccion de Trigramas Title de la noticia con su frecuencia (ordenados de mas frecuente a menos frecuente).
#	Para obtener los Trigramas t=[i[1] for i in TG]
#	Para obtener las frecuencias f=[i[0] for i in TG]
def obtenerNoticiaClarin(url):
	#Recolecto el html de la noticia
	contenido=recolectarNoticia(url)
	
	#Obtengo principio y fin del contenido de la noticia
	patron=re.compile("<span itemprop=\"articleBody\"> <p>")
	ini= patron.search(contenido).end()
	patron=re.compile("</span> </div> </div> </div> </div> <div id")
	fin=patron.search(contenido).start()
	contenido=contenido[ini:fin]
	
	#Limpio el contenido de links y tags
	contenido=limpiezaHTMLGral(contenido)

	#Detecto trigramas y bigramas y limpio el contenido de la noticia y aplico Chen
	[BG,TG]=detectarEntidades(contenido)
	contenido= limpiar_Contenido(contenido)
	
	return [contenido,BG,TG]

#obtenerNoticiaTN(URL_de_la_Noticia)
#retorna un arreglo con 3 componentes [contenido,BG,TG]
#contenido: contenido de la noticia,limpia, con aplicacion del metodo chen, todo en una linea
#BG:coleccion de Bigramas Title de la noticia con su frecuencia (ordenados de mas frecuente a menos frecuente).
#	Para obtener los Bigramas b=[i[1] for i in BG]
#	Para obtener las frecuencias f=[i[0] for i in BG]
#TG:coleccion de Trigramas Title de la noticia con su frecuencia (ordenados de mas frecuente a menos frecuente).
#	Para obtener los Trigramas t=[i[1] for i in TG]
#	Para obtener las frecuencias f=[i[0] for i in TG]
def obtenerNoticiaTN(url):
	#Recolecto el html de la noticia
	contenido=recolectarNoticia(url)
	
	#Obtengo principio y fin del contenido de la noticia
	patron=re.compile("<div class=\"col-12 news-article-content entry-content\" >")
	ini= patron.search(contenido).end()
	patron=re.compile("<div class=\"col-12 news-article-tag-list\">")
	fin=patron.search(contenido).start()
	contenido=contenido[ini:fin]
	
	#Limpio el contenido de links y tags
	contenido=limpiezaHTMLGral(contenido)

	#Detecto trigramas y bigramas y limpio el contenido de la noticia y aplico Chen
	[BG,TG]=detectarEntidades(contenido)
	contenido= limpiar_Contenido(contenido)
	
	return [contenido,BG,TG]

#obtenerNoticiaP12(URL_de_la_Noticia)
#retorna un arreglo con 3 componentes [contenido,BG,TG]
#contenido: contenido de la noticia,limpia, con aplicacion del metodo chen, todo en una linea
#BG:coleccion de Bigramas Title de la noticia con su frecuencia (ordenados de mas frecuente a menos frecuente).
#	Para obtener los Bigramas b=[i[1] for i in BG]
#	Para obtener las frecuencias f=[i[0] for i in BG]
#TG:coleccion de Trigramas Title de la noticia con su frecuencia (ordenados de mas frecuente a menos frecuente).
#	Para obtener los Trigramas t=[i[1] for i in TG]
#	Para obtener las frecuencias f=[i[0] for i in TG]
def obtenerNoticiaP12(url):
	#Recolecto el html de la noticia
	contenido=recolectarNoticia(url)
	
	#Obtengo principio y fin del contenido de la noticia
	patron=re.compile("<div class=\"article-text\">")
	ini= patron.search(contenido).end()
	patron=re.compile("</div><div class=\"article-footer\">")
	fin=patron.search(contenido).start()
	contenido=contenido[ini:fin]
	
	#Limpio el contenido de links y tags
	contenido=limpiezaHTMLGral(contenido)

	#Detecto trigramas y bigramas y limpio el contenido de la noticia y aplico Chen
	[BG,TG]=detectarEntidades(contenido)
	contenido= limpiar_Contenido(contenido)
	
	return [contenido,BG,TG]

#obtenerNoticiaLaIzq(URL_de_la_Noticia)
#retorna un arreglo con 3 componentes [contenido,BG,TG]
#contenido: contenido de la noticia,limpia, con aplicacion del metodo chen, todo en una linea
#BG:coleccion de Bigramas Title de la noticia con su frecuencia (ordenados de mas frecuente a menos frecuente).
#	Para obtener los Bigramas b=[i[1] for i in BG]
#	Para obtener las frecuencias f=[i[0] for i in BG]
#TG:coleccion de Trigramas Title de la noticia con su frecuencia (ordenados de mas frecuente a menos frecuente).
#	Para obtener los Trigramas t=[i[1] for i in TG]
#	Para obtener las frecuencias f=[i[0] for i in TG]
def obtenerNoticiaLaIzq(url):
	#Recolecto el html de la noticia
	contenido=recolectarNoticia(url)
	
	#Obtengo principio y fin del contenido de la noticia
	#if re.match("<div class=\"articulo\">", contenido) and re.match("<div class=\"widget-area\">", contenido) :
	patron=re.compile("<div class=\"articulo\">")
	ini= patron.search(contenido).end()
	patron=re.compile("<div class=\"widget-area\">")
	fin=patron.search(contenido).start()
	contenido=contenido[ini:fin]
	
	#else:
	#	contenido = ""
	#Limpio el contenido de links y tags
	contenido=limpiezaHTMLGral(contenido)
	
	#Detecto trigramas y bigramas y limpio el contenido de la noticia y aplico Chen
	[BG,TG]=detectarEntidades(contenido)
	contenido= limpiar_Contenido(contenido)
			
	return [contenido,BG,TG]
	



#obtenerNoticiaTelam(URL_de_la_Noticia)
#retorna un arreglo con 3 componentes [contenido,BG,TG]
#contenido: contenido de la noticia,limpia, con aplicacion del metodo chen, todo en una linea
#BG:coleccion de Bigramas Title de la noticia con su frecuencia (ordenados de mas frecuente a menos frecuente).
#	Para obtener los Bigramas b=[i[1] for i in BG]
#	Para obtener las frecuencias f=[i[0] for i in BG]
#TG:coleccion de Trigramas Title de la noticia con su frecuencia (ordenados de mas frecuente a menos frecuente).
#	Para obtener los Trigramas t=[i[1] for i in TG]
#	Para obtener las frecuencias f=[i[0] for i in TG]	
def obtenerNoticiaTelam(url):
	#Recolecto el html de la noticia
	contenido=recolectarNoticia(url)
	
	#Obtengo principio y fin del contenido de la noticia	
	patron=re.compile("<div class=\"editable-content clearfix\">")
	ini= patron.search(contenido).end()
	patron=re.compile("<div class=\"wrapper-tags\">")
	fin=patron.search(contenido).start()
	contenido=contenido[ini:fin]
	
	#Limpio el contenido de links y tags
	contenido=limpiezaHTMLGral(contenido)

	#Detecto trigramas y bigramas y limpio el contenido de la noticia y aplico Chen
	[BG,TG]=detectarEntidades(contenido)
	contenido= limpiar_Contenido(contenido)
	
	return [contenido,BG,TG]

#obtenerNoticiaAmbito(URL_de_la_Noticia)
#retorna un arreglo con 3 componentes [contenido,BG,TG]
#contenido: contenido de la noticia,limpia, con aplicacion del metodo chen, todo en una linea
#BG:coleccion de Bigramas Title de la noticia con su frecuencia (ordenados de mas frecuente a menos frecuente).
#	Para obtener los Bigramas b=[i[1] for i in BG]
#	Para obtener las frecuencias f=[i[0] for i in BG]
#TG:coleccion de Trigramas Title de la noticia con su frecuencia (ordenados de mas frecuente a menos frecuente).
#	Para obtener los Trigramas t=[i[1] for i in TG]
#	Para obtener las frecuencias f=[i[0] for i in TG]	
def obtenerNoticiaAmbito(url):
	#Recolecto el html de la noticia
	contenido=recolectarNoticia(url)
	
	#Obtengo principio y fin del contenido de la noticia
	patron=re.compile("<p id=\"cuerpo_noticia\">")
	ini= patron.search(contenido).end()
	patron=re.compile("<aside class=\"container-fluid tag\">")
	fin=patron.search(contenido).start()
	contenido=contenido[ini:fin]
	
	#Limpio el contenido de links y tags
	contenido=limpiezaHTMLGral(contenido)

	#Detecto trigramas y bigramas y limpio el contenido de la noticia y aplico Chen
	[BG,TG]=detectarEntidades(contenido)
	contenido= limpiar_Contenido(contenido)
	
	return [contenido,BG,TG]


	
#....------------------------------------------------------------------------------------------------------------------....
#-------------------------------------------------------------------------------------------------------------------------
#....------------------------------------------------------------------------------------------------------------------....	
	
if __name__ == '__main__':

	writerGlobal = codecs.open(CORPUS_RING_2, "w",encoding='utf8')

	#TN
	lista_terminos = []

	with open(TN) as f:
		num_noticia = 1
		name = "ScriptsAuxiliares/Noticias/TN/Noticia_"
		for line in f:
			nombre = name + str(num_noticia) + ".txt"
			print(nombre + "\n")
			url = line[:-1]
			if (len(url)>2):
				[contenido,BG,TG]= obtenerNoticiaTN(url)
				b=[i[1] for i in BG]
				fb=[i[0] for i in BG]
				t=[i[1] for i in TG]
				ft=[i[0] for i in TG]
				writer = codecs.open(nombre, "w",encoding='utf8')
				writerCorpus = codecs.open(CORPUS_RING_1_TN, "w",encoding='utf8')
				for element in contenido:
					if (len(element)>1):
						writer.write(str(element) + "\n")
						lista_element = element.split(" ")
						for item in lista_element:
							if not isStopword(item):
								lista_terminos.append(item)
				l = [elem for elem in lista_terminos if (lista_terminos.count(elem)>1)]
				for palabra in l:
					writerCorpus.write(palabra + "\n")
					writerGlobal.write(palabra + "\n")
				writer.write(str(b) + "\n")
				writer.write(str(fb) + "\n")
				writer.write(str(t) + "\n")
				writer.write(str(ft) + "\n")
				writer.close()
				num_noticia = num_noticia + 1
		writerCorpus.close()


	#Clarin
	lista_terminos = []

	with open(CLARIN) as f:
		num_noticia = 1
		name = "ScriptsAuxiliares/Noticias/Clarin/Noticia_"
		for line in f:
			nombre = name + str(num_noticia) + ".txt"
			print(nombre + "\n")
			url = line[:-1]
			if (len(url)>2):
				[contenido,BG,TG]= obtenerNoticiaClarin(url)
				b=[i[1] for i in BG]
				fb=[i[0] for i in BG]
				t=[i[1] for i in TG]
				ft=[i[0] for i in TG]
				writer = codecs.open(nombre, "w",encoding='utf8')
				writerCorpus = codecs.open(CORPUS_RING_1_CLARIN, "w",encoding='utf8')
				for element in contenido:
					if (len(element)>1):
						writer.write(str(element) + "\n")
						lista_element = element.split(" ")
						for item in lista_element:
							if not isStopword(item):
								lista_terminos.append(item)
				l = [elem for elem in lista_terminos if (lista_terminos.count(elem)>1)]
				for palabra in l:
					writerCorpus.write(palabra + "\n")
					writerGlobal.write(palabra + "\n")
				writer.write(str(b) + "\n")
				writer.write(str(fb) + "\n")
				writer.write(str(t) + "\n")
				writer.write(str(ft) + "\n")
				writer.close()
				num_noticia = num_noticia + 1
		writerCorpus.close()
		

	#La Nacion
	lista_terminos = []

	with open(LA_NACION) as f:
		num_noticia = 1
		name = "ScriptsAuxiliares/Noticias/LaNacion/Noticia_"
		for line in f:
			nombre = name + str(num_noticia) + ".txt"
			print(nombre + "\n")
			url = line[:-1]
			if (len(url)>2):
				[contenido,BG,TG]= obtenerNoticiaNacion(url)
				b=[i[1] for i in BG]
				fb=[i[0] for i in BG]
				t=[i[1] for i in TG]
				ft=[i[0] for i in TG]
				writer = codecs.open(nombre, "w",encoding='utf8')
				writerCorpus = codecs.open(CORPUS_RING_1_LA_NACION, "w",encoding='utf8')
				for element in contenido:
					if (len(element)>1):
						writer.write(str(element) + "\n")
						lista_element = element.split(" ")
						for item in lista_element:
							if not isStopword(item):
								lista_terminos.append(item)
				l = [elem for elem in lista_terminos if (lista_terminos.count(elem)>1)]
				for palabra in l:
					writerCorpus.write(palabra + "\n")
					writerGlobal.write(palabra + "\n")
				writer.write(str(b) + "\n")
				writer.write(str(fb) + "\n")
				writer.write(str(t) + "\n")
				writer.write(str(ft) + "\n")
				writer.close()
				num_noticia = num_noticia + 1
		writerCorpus.close()

	#Pagina 12
	lista_terminos = []

	with open(PAGINA_DOCE) as f:
		num_noticia = 1
		name = "ScriptsAuxiliares/Noticias/PaginaDoce/Noticia_"
		for line in f:
			nombre = name + str(num_noticia) + ".txt"
			print(nombre + "\n")
			url = line[:-1]
			if (len(url)>2):
				[contenido,BG,TG]= obtenerNoticiaP12(url)
				b=[i[1] for i in BG]
				fb=[i[0] for i in BG]
				t=[i[1] for i in TG]
				ft=[i[0] for i in TG]
				writer = codecs.open(nombre, "w",encoding='utf8')
				writerCorpus = codecs.open(CORPUS_RING_1_PAGINA_DOCE, "w",encoding='utf8')
				for element in contenido:
					if (len(element)>1):
						writer.write(str(element) + "\n")
						lista_element = element.split(" ")
						for item in lista_element:
							if not isStopword(item):
								lista_terminos.append(item)
				l = [elem for elem in lista_terminos if (lista_terminos.count(elem)>1)]
				for palabra in l:
					writerCorpus.write(palabra + "\n")
					writerGlobal.write(palabra + "\n")
				writer.write(str(b) + "\n")
				writer.write(str(fb) + "\n")
				writer.write(str(t) + "\n")
				writer.write(str(ft) + "\n")
				writer.close()
				num_noticia = num_noticia + 1
		writerCorpus.close()

	#LaIzquierda
	lista_terminos = []

	with open(LA_IZQUIERDA) as f:
		num_noticia = 1
		name = "ScriptsAuxiliares/Noticias/LaIzquierda/Noticia_"
		for line in f:
			nombre = name + str(num_noticia) + ".txt"
			print(nombre + "\n")
			url = line[:-1]
			if (len(url)>2):
				[contenido,BG,TG]= obtenerNoticiaLaIzq(url)
				b=[i[1] for i in BG]
				fb=[i[0] for i in BG]
				t=[i[1] for i in TG]
				ft=[i[0] for i in TG]
				writer = codecs.open(nombre, "w",encoding='utf8')
				writerCorpus = codecs.open(CORPUS_RING_1_LA_IZQUIERDA, "w",encoding='utf8')
				for element in contenido:
					if (len(element)>1):
						writer.write(str(element) + "\n")
						lista_element = element.split(" ")
						for item in lista_element:
							if not isStopword(item):
								lista_terminos.append(item)
				l = [elem for elem in lista_terminos if (lista_terminos.count(elem)>1)]
				for palabra in l:
					writerCorpus.write(palabra + "\n")
					writerGlobal.write(palabra + "\n")
				writer.write(str(b) + "\n")
				writer.write(str(fb) + "\n")
				writer.write(str(t) + "\n")
				writer.write(str(ft) + "\n")
				writer.close()
				num_noticia = num_noticia + 1
		writerCorpus.close()

	writerGlobal.close()