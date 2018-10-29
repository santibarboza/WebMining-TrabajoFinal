import re
import codecs
import math
import os.path


#AnalisisRing0.py
#Analisis de corpus ring 0 para cada portal

#Descriptores de archivos para corpus de palabras
CORPUS_RING_0_TN = "ScriptsAuxiliares/Corpus/Ring0/TodoNoticias.txt"
CORPUS_RING_0_CLARIN = "ScriptsAuxiliares/Corpus/Ring0/Clarin.txt"
CORPUS_RING_0_LA_NACION = "ScriptsAuxiliares/Corpus/Ring0/LaNacion.txt"
CORPUS_RING_0_PAGINA_DOCE = "ScriptsAuxiliares/Corpus/Ring0/PaginaDoce.txt"
CORPUS_RING_0_LA_IZQUIERDA = "ScriptsAuxiliares/Corpus/Ring0/LaIzquierda.txt"

#Descriptores de archivos: librerias de analisis de sentimientos
POSITIVE = "ScriptsAuxiliares/positivas.txt"
NEGATIVE = "ScriptsAuxiliares/negativas.txt"

#Constante de peso por aparicion en diccionario de sentimiento
CONSTANTE_PESO_POSITIVO = 0.5
CONSTANTE_PESO_NEGATIVO = 0.7
TERMINOS_X = []

with open(TERMINOSX) as f:
	TERMINOS_X = f.read().split(',')

#Variables globales
#creacion de conjuntos de`palabras positivas y negativas
set_positivas = set()
set_negativas = set()

with open(POSITIVE) as f:
	set_positivas = f.read().splitlines()
	set_positivas = [re.sub("[\s]","",w) for w in set_positivas ]

with open(NEGATIVE) as f:
	set_negativas = f.read().splitlines()
	set_negativas = [re.sub("[\s]","",w) for w in set_negativas ]

def analizar(desc_archivo):

	lista_oraciones = []
	lista_terminos_noticia = []
	
	with open(desc_archivo) as f:
		for line in f:
			linea = line[:-1]
			linea = linea.split(" ")
			lista_oraciones.append(linea)

			#agrego cada termino a una lista de terminos de esa noticia
			for elem in linea:
				lista_terminos_noticia.append(elem)

	#Creacion de un conjunto (sin repeticiones) de palabras del texto
	conjunto_terminos = set();

	for word in lista_terminos_noticia:
		conjunto_terminos.add(word)	

	#Generacion de lista ordenada con pesos tf de palabras del texto
	mapeo_inverso = {}
	nro_palabra =0
	lista_tf = []
	for termino in TERMINOS_X:
		c = lista_terminos_noticia.count(termino)
		lista_tf.append((termino,c))
		mapeo_inverso[termino] = nro_palabra
		nro_palabra = nro_palabra+1

	#Buscamos, para cada termino x, en que oraciones aparece
	puntaje_terminos = []
	for termino in TERMINOS_X:
		puntaje_noticia = 0
		for oracion in lista_oraciones:
			if termino in oracion:

				#Iniciamos busqueda de terminos positivos y negativos en la oracion
				lista_positivos = []
				lista_negativos = []
				
				for palabra in oracion:
					if palabra in set_positivas:
						lista_positivos.append(palabra)
					if palabra in set_negativas:
						lista_negativos.append(palabra)
	
				#Calculamos el peso positivo y negativo considerando la cantidad de apariciones
				#del termino X buscado
				peso_positivo = 0
				cant_positivas = len(lista_positivos)
				tf = lista_tf[mapeo_inverso[termino]][1]
				peso_positivo = tf * CONSTANTE_PESO_POSITIVO * cant_positivas

				peso_negativo = 0
				cant_negativas = len(lista_negativos)
				tf = lista_tf[mapeo_inverso[termino]][1]
				peso_negativo = tf * CONSTANTE_PESO_NEGATIVO * cant_negativas * -1

				puntaje_oracion = peso_positivo + peso_negativo
				puntaje_noticia = puntaje_noticia + puntaje_oracion
				#print(desc_archivo + " " + termino + " " + str(cant_positivas) + " "  + str(cant_negativas) + " " + str(puntaje_noticia))
		puntaje_terminos.append((termino,puntaje_noticia))


	return(puntaje_terminos)
	
#....------------------------------------------------------------------------------------------------------------------....
#-------------------------------------------------------------------------------------------------------------------------
#....------------------------------------------------------------------------------------------------------------------....	
	
if __name__ == '__main__':

	#TN
	num_noticia = 1
	fname = "ScriptsAuxiliares/Noticias/TN/Noticia_" + str(num_noticia) + ".txt"
	
	condicion = os.path.isfile(fname) 
	writer = codecs.open(CORPUS_RING_0_TN, "w",encoding='utf8')

	while(condicion):
		puntaje_terminos = analizar(fname)
		writer.write("Noticia " + str(num_noticia) + " -> " + str(puntaje_terminos) + "\n")
		num_noticia = num_noticia + 1
		fname = "ScriptsAuxiliares/Noticias/TN/Noticia_" + str(num_noticia) + ".txt"
		condicion = os.path.isfile(fname) 
	
	writer.close()

	#LaNacion
	num_noticia = 1
	fname = "ScriptsAuxiliares/Noticias/LaNacion/Noticia_" + str(num_noticia) + ".txt"
	
	condicion = os.path.isfile(fname) 
	writer = codecs.open(CORPUS_RING_0_LA_NACION, "w",encoding='utf8')

	while(condicion):
		puntaje_terminos = analizar(fname)
		writer.write("Noticia " + str(num_noticia) + " -> " + str(puntaje_terminos) + "\n")
		num_noticia = num_noticia + 1
		fname = "ScriptsAuxiliares/Noticias/LaNacion/Noticia_" + str(num_noticia) + ".txt"
		condicion = os.path.isfile(fname) 
	
	writer.close()

	#Clarin
	num_noticia = 1
	fname = "ScriptsAuxiliares/Noticias/Clarin/Noticia_" + str(num_noticia) + ".txt"
	
	condicion = os.path.isfile(fname) 
	writer = codecs.open(CORPUS_RING_0_CLARIN, "w",encoding='utf8')

	while(condicion):
		puntaje_terminos = analizar(fname)
		writer.write("Noticia " + str(num_noticia) + " -> " + str(puntaje_terminos) + "\n")
		num_noticia = num_noticia + 1
		fname = "ScriptsAuxiliares/Noticias/Clarin/Noticia_" + str(num_noticia) + ".txt"
		condicion = os.path.isfile(fname) 
	
	writer.close()

	#PaginaDoce
	num_noticia = 1
	fname = "ScriptsAuxiliares/Noticias/PaginaDoce/Noticia_" + str(num_noticia) + ".txt"
	
	condicion = os.path.isfile(fname) 
	writer = codecs.open(CORPUS_RING_0_PAGINA_DOCE, "w",encoding='utf8')

	while(condicion):
		puntaje_terminos = analizar(fname)
		writer.write("Noticia " + str(num_noticia) + " -> " + str(puntaje_terminos) + "\n")
		num_noticia = num_noticia + 1
		fname = "ScriptsAuxiliares/Noticias/PaginaDoce/Noticia_" + str(num_noticia) + ".txt"
		condicion = os.path.isfile(fname) 
	
	writer.close()

	#LaIzquierda
	num_noticia = 1
	fname = "ScriptsAuxiliares/Noticias/LaIzquierda/Noticia_" + str(num_noticia) + ".txt"
	
	condicion = os.path.isfile(fname) 
	writer = codecs.open(CORPUS_RING_0_LA_IZQUIERDA, "w",encoding='utf8')

	while(condicion):
		puntaje_terminos = analizar(fname)
		writer.write("Noticia " + str(num_noticia) + " -> " + str(puntaje_terminos) + "\n")
		num_noticia = num_noticia + 1
		fname = "ScriptsAuxiliares/Noticias/LaIzquierda/Noticia_" + str(num_noticia) + ".txt"
		condicion = os.path.isfile(fname) 
	
	writer.close()