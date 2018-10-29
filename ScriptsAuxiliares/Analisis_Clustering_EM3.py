#Analisis_Clustering_EM3.py
import os.path
import re
import codecs
import math
import numpy
#from scipy.cluster.vq import kmeans2

#Descriptores de archivos utilizados
RESULT_CLUSTERING = "ScriptsAuxiliares/ResultadosWeka/resultados-EM3.arff"

SALIDA = "Resultados.txt"

CARPETA_LINKS = "ScriptsAuxiliares/Archivos/"
Medios = ["TodoNoticias","Clarin","LaNacion","LaIzquierda","PaginaDoce"]

Clusters =  ["cluster0","cluster1","cluster2"]


def obtener_cant_noticias_cada_medio():
	lista_cantidades = []
	for medio in Medios:
		fname = CARPETA_LINKS + medio + ".txt"
		with open(fname) as f:
			text = f.read()
			lineas = text.splitlines()
		
			cant_noticias_en_medio = len(lineas)
			lista_cantidades.append(cant_noticias_en_medio)
	return lista_cantidades

index_noticias = []

num = 0
with open(RESULT_CLUSTERING) as f:
	for line in f:
		if (line[0] != '@') and (line[0] !="\n"):
			line = line[:-1]
			cosas = line.split(",")

			#Agrego el indice de noticia a la lista de labels (index_noticias)
			index_noticias.append(cosas[-1])

#Busco en que clusters esta cada noticia y lo voy marcando en las listas de cada medio
lista_cantidades = obtener_cant_noticias_cada_medio()
cantTN = lista_cantidades[0]
cantClarin = lista_cantidades[1]
cantLaNacion = lista_cantidades[2]
cantLaIzq = lista_cantidades[3]
cantPagDoce = lista_cantidades[4]

#Creacion de lista de terminos global con repeticiones
lista_TN = [0] * cantTN
lista_Clarin = [0] * cantClarin
lista_LaNacion = [0] * cantLaNacion
lista_LaIzquierda = [0] * cantLaIzq
lista_PaginaDoce = [0] * cantPagDoce

#TN
acum = 0
n = 0
while (n<(cantTN + acum)):
	lista_TN[n-acum] = index_noticias[n]
	n+=1
#Clarin
acum+=cantTN
while (n<(cantClarin+acum)):
	lista_Clarin[n-acum] = index_noticias[n]
	n+=1
#LaNacion
acum+=cantClarin
while (n<(cantLaNacion+acum)):
	lista_LaNacion[n-acum] = index_noticias[n]
	n+=1
#LaIzquierda
acum+=cantLaNacion
while (n<(cantLaIzq+acum)):
	lista_LaIzquierda[n-acum] = index_noticias[n]
	n+=1
#PaginaDoce
acum+=cantLaIzq
while (n<(cantPagDoce+acum)):
	lista_PaginaDoce[n-acum] = index_noticias[n]
	n+=1

#Confeccion de archivo de resultados
writer = codecs.open(SALIDA, "a",encoding='utf8')

writer.write("\n-------------------------------------------------------------------------------------------------\n")
writer.write("Corpus Ring 2: Expresion de similitud entre noticias de distintos portales\n")
writer.write("Clustering: Expectation Maximization (3 clusters) - ResultadosWeka/resultados-EM-3.arff\n")
writer.write("-------------------------------------------------------------------------------------------------\n")

for item in Clusters:
	writer.write("\n--------------------------------------------------------\n")
	writer.write("    " + item + ":\n")
	writer.write("--------------------------------------------------------\n\n")

	#TN
	fname = CARPETA_LINKS + Medios[0] + ".txt"
	with open(fname) as f:
		text = f.read()
		links = text.splitlines()
		num_elemento = 0
		for elemento in lista_TN:
			if item == elemento:
				writer.write(links[num_elemento] + "\n")
			num_elemento+=1

	writer.write ("\n")

	#Clarin
	fname = CARPETA_LINKS + Medios[1] + ".txt"
	with open(fname) as f:
		text = f.read()
		links = text.splitlines()
		num_elemento = 0
		for elemento in lista_Clarin:
			if item == elemento:
				writer.write(links[num_elemento] + "\n")
			num_elemento+=1

	writer.write ("\n")

	#LaNacion
	fname = CARPETA_LINKS + Medios[2] + ".txt"
	with open(fname) as f:
		text = f.read()
		links = text.splitlines()
		num_elemento = 0
		for elemento in lista_LaNacion:
			if item == elemento:
				writer.write(links[num_elemento] + "\n")
			num_elemento+=1

	writer.write ("\n")

	#LaIzquierda
	fname = CARPETA_LINKS + Medios[3] + ".txt"
	with open(fname) as f:
		text = f.read()
		links = text.splitlines()
		num_elemento = 0
		for elemento in lista_LaIzquierda:
			if item == elemento:
				writer.write(links[num_elemento] + "\n")
			num_elemento+=1

	writer.write ("\n")

	#PaginaDoce
	fname = CARPETA_LINKS + Medios[4] + ".txt"
	with open(fname) as f:
		text = f.read()
		links = text.splitlines()
		num_elemento = 0
		for elemento in lista_PaginaDoce:
			if item == elemento:
				writer.write(links[num_elemento] + "\n")
			num_elemento+=1

writer.close()
		