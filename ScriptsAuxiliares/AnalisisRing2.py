import re
import codecs
import math
import numpy
import os.path
#from scipy.cluster.vq import kmeans2

#Descriptores de archivos utilizados
CORPUS_RING_2 = "ScriptsAuxiliares/Corpus/Ring2/CorpusGlobal.txt"
CARPETA_NOTICIAS = "ScriptsAuxiliares/Noticias/"
MEDIOS = ("TN/","Clarin/","LaNacion/","LaIzquierda/","PaginaDoce/")
SIMCOS_ARFF_DENSE = "ScriptsAuxiliares/Simcos_ARFF_Dense.arff"

#Creacion de lista de terminos global con repeticiones
lista_terminos = []

with open(CORPUS_RING_2) as f:
	for line in f:
		termino = line[:-1]
		lista_terminos.append(termino)

#Creacion de un conjunto de terminos global sin repeticiones
#el corpus no contiene palabras que solo aparezcan una vez en las noticias
conjunto_terminos = set();

for word in lista_terminos:
	conjunto_terminos.add(word)

#Creacion de corpus de noticias global
listado_noticias = []

#Exploracion de carpetas de noticias y construccion de listado de noticias
#Cada noticia se representa con una lista de palabras; estas pueden contener
#palabras no consideradas dentro del corpus (por ejemplo, las que aparecen 
#solo una vez), las cuales seran obviadas en la matriz tf.
for medio in MEDIOS:
	
	carpeta_actual = CARPETA_NOTICIAS + medio
	num_noticia = 1
	fname = carpeta_actual +"Noticia_" + str(num_noticia) + ".txt"
	
	condicion = os.path.isfile(fname) 
	while(condicion):
		corpus_de_una_noticia = []
		with open(fname) as f:
			for line in f:
				line = line[:-1]
				if line[0] != '[':
					palabras_oracion = line.split(" ")
					for palabra in palabras_oracion:
						corpus_de_una_noticia.append(palabra)

		listado_noticias.append(corpus_de_una_noticia)
		num_noticia = num_noticia + 1
		fname = carpeta_actual +"Noticia_" + str(num_noticia) + ".txt"
		condicion = os.path.isfile(fname) 
	
#Creacion de una lista con una palabra por indice
#Creacion de un mapeo inverso: lista de palabras con su numero de indice
mapeo_inverso = {}
lista_indexable_terminos = []
nro_palabra =0
for palabra in conjunto_terminos:
    lista_indexable_terminos.append(palabra)
    mapeo_inverso[palabra] = nro_palabra
    nro_palabra = nro_palabra + 1

#Creacion de matriz tf de terminos / noticias: tf se calcula aqui.
matriz_tf = numpy.zeros((len(listado_noticias), len(lista_indexable_terminos)))
indice_noticia = 0

for noticia in listado_noticias:
    for palabra in set(noticia):
    	if palabra in conjunto_terminos:
    		count = noticia.count(palabra)
    		indice_palabra = mapeo_inverso[palabra]
    		matriz_tf[indice_noticia][indice_palabra] = float(count)
    indice_noticia += 1

#Creacion de matriz_tf normalizada para el calculo de la matriz de similitud por coseno entre noticias
matriz_tf_norm = numpy.zeros((len(listado_noticias), len(lista_indexable_terminos)))

index = 0
for line in matriz_tf:
	denominador = math.sqrt(sum(math.pow(x,2) for x in line))
	matriz_tf_norm[index] = [elemento/denominador for elemento in line]
	index = index + 1

#Creacion de matriz de similitud por coseno entre tweets usando matriz tfidf normalizada
matriz_tf_norm_T = numpy.transpose(matriz_tf_norm)
matriz_simcos = numpy.dot(matriz_tf_norm,matriz_tf_norm_T)

#Creacion a mano de archivo arff dense para similitud por coseno entre tweets
writer = codecs.open(SIMCOS_ARFF_DENSE, "w",encoding='utf8')
writer.write("%similitud por coseno aplicado sobre un conjunto de noticias"+"\n")
writer.write("@RELATION noticias-simcosdense"+"\n\n")
index = 0
for noticia in listado_noticias:
	s = "noticia_" + str(index)
	writer.write("@ATTRIBUTE " + s + " numeric" + "\n")
	index = index + 1

writer.write("\n\n" + "@DATA" + "\n")
index = 0
for line in matriz_simcos:
	s = ""
	for n in range(0, len(matriz_simcos[0])):
		s = s + str(matriz_simcos[index][n]) + ", "
	s = s[:-2] + "\n"
	writer.write(s)
	index = index + 1

writer.close()