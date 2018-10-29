import re
import codecs
import math


#AnalisisRing1.py
#Analisis de corpus ring 1 para cada portal

#Descriptores de archivos para corpus de palabras
CORPUS_RING_1_TN = "ScriptsAuxiliares/Corpus/Ring1/TodoNoticias.txt"
CORPUS_RING_1_CLARIN = "ScriptsAuxiliares/Corpus/Ring1/Clarin.txt"
CORPUS_RING_1_LA_NACION = "ScriptsAuxiliares/Corpus/Ring1/LaNacion.txt"
CORPUS_RING_1_PAGINA_DOCE = "ScriptsAuxiliares/Corpus/Ring1/PaginaDoce.txt"
CORPUS_RING_1_LA_IZQUIERDA = "ScriptsAuxiliares/Corpus/Ring1/LaIzquierda.txt"

#Descriptores de archivos: librerias de analisis de sentimientos
POSITIVE = "ScriptsAuxiliares/positivas.txt"
NEGATIVE = "ScriptsAuxiliares/negativas.txt"

#Descriptor de archivo para resultados ring1
RESULTADOS = "Resultados.txt"

#Constante de peso por aparicion en diccionario de sentimiento
CONSTANTE_PESO_POSITIVO = 0.5
CONSTANTE_PESO_NEGATIVO = 0.7

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
	lista_terminos = []
	
	with open(desc_archivo) as f:
		for line in f:
			lista_terminos.append(line[:-1])
	
	#Creacion de un conjunto (sin repeticiones) de palabras del texto
	conjunto_terminos = set();

	for elem in lista_terminos:
		conjunto_terminos.add(elem)	
	
	#Generacion de lista ordenada con pesos tf de palabras del contexto
	mapeo_inverso = {}
	nro_palabra =0
	lista_tf = []
	for palabra in conjunto_terminos:
		c = lista_terminos.count(palabra)
		lista_tf.append((palabra,c))
		mapeo_inverso[palabra] = nro_palabra
		nro_palabra = nro_palabra+1
	
	#Ordenamos la lista tf segun apariciones
	#lista_tf.sort(key=lambda tupla: tupla[1], reverse=True)

	#Iniciamos busqueda de terminos positivos y negativos
	lista_positivos = []
	lista_negativos = []
	
	for palabra in conjunto_terminos:
		if palabra in set_positivas:
			lista_positivos.append(palabra)
		if palabra in set_negativas:
			lista_negativos.append(palabra)
	
	#Calculamos el peso positivo y negativo considerando la cantidad de apariciones
	peso_positivo = 0
	for termino in lista_positivos:
		tf = lista_tf[mapeo_inverso[termino]][1]
		peso_positivo = peso_positivo + math.log(tf,2) * CONSTANTE_PESO_POSITIVO

	peso_negativo = 0
	for termino in lista_negativos:
		tf = lista_tf[mapeo_inverso[termino]][1]
		peso_negativo = peso_negativo + math.log(tf,0.5) * CONSTANTE_PESO_NEGATIVO

	return(peso_positivo, peso_negativo)
	
#....------------------------------------------------------------------------------------------------------------------....
#-------------------------------------------------------------------------------------------------------------------------
#....------------------------------------------------------------------------------------------------------------------....	
	
if __name__ == '__main__':

	rtn= analizar(CORPUS_RING_1_TN)
	rcl= analizar(CORPUS_RING_1_CLARIN)
	rln= analizar(CORPUS_RING_1_LA_NACION)
	rli= analizar(CORPUS_RING_1_LA_IZQUIERDA)
	rpd= analizar(CORPUS_RING_1_PAGINA_DOCE)
	
	writer = codecs.open(RESULTADOS, "w",encoding='utf8')
	writer.write("******************************************************************************************************\n");
	writer.write("********************************************  RESULTADOS  ********************************************\n");
	writer.write("******************************************************************************************************\n\n");
	
	writer.write("-------------------------------------------------------------------------------------------------\n");
	writer.write("Corpus Ring 1: Analisis de utilizacion de terminos positivos y negativos en redaccion de noticias\n");
	writer.write("-------------------------------------------------------------------------------------------------\n\n");
	
	writer.write("TN -> positivo: " + str(rtn[0]) + " | negativo: " + str(rtn[1]) + " | TOTAL: " + str(rtn[0] + rtn[1]) +"\n")
	writer.write("CLARIN -> positivo: " + str(rcl[0]) + " | negativo: " + str(rcl[1]) + " | TOTAL: " + str(rcl[0] + rcl[1]) +"\n")
	writer.write("LANACION -> positivo: " + str(rln[0]) + " | negativo: " + str(rln[1]) + " | TOTAL: " + str(rln[0] + rln[1]) +"\n")
	writer.write("LAIZQUIERDA -> positivo: " + str(rli[0]) + " | negativo: " + str(rli[1]) + " | TOTAL: " + str(rli[0] + rli[1]) +"\n")
	writer.write("PAGINADOCE -> positivo: " + str(rpd[0]) + " | negativo: " + str(rpd[1]) + " | TOTAL: " + str(rpd[0] + rpd[1]) +"\n")

	writer.close()