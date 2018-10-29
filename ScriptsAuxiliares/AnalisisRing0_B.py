import re
import codecs
import math
import os.path
from collections import defaultdict


#AnalisisRing0_B.py
#Analisis de corpus ring 0 para cada portal (parte 2)

#Descriptores de archivos para corpus de palabras
CORPUS_RING_0_TN = "ScriptsAuxiliares/Corpus/Ring0/TodoNoticias.txt"
CORPUS_RING_0_CLARIN = "ScriptsAuxiliares/Corpus/Ring0/Clarin.txt"
CORPUS_RING_0_LA_NACION = "ScriptsAuxiliares/Corpus/Ring0/LaNacion.txt"
CORPUS_RING_0_PAGINA_DOCE = "ScriptsAuxiliares/Corpus/Ring0/PaginaDoce.txt"
CORPUS_RING_0_LA_IZQUIERDA = "ScriptsAuxiliares/Corpus/Ring0/LaIzquierda.txt"

RESULTADOS = "Resultados.txt"

TERMINOS_X = []

with open(TERMINOSX) as f:
	TERMINOS_X = f.read().split(',')

def obtener_valor_promedio(desc_archivo):

	dic_terminos_valor = defaultdict(float)
	dic_terminos_cant = defaultdict(int)
	with open(desc_archivo) as f:
		for line in f:
			linea = line[:-1]
			linea = re.split('[\;\:\'\"\ \[\]\(\)\,]', linea)
			listita = []
			for elem in linea:
				if len(elem)>0:
					listita.append(elem)
			#Buscamos, para cada termino x, el puntaje asociado por noticia
			puntaje_terminos = []
			for termino in TERMINOS_X:
				if termino in linea:
					valor = listita[listita.index(termino) + 1]
					dic_terminos_valor[termino]+=float(valor)
					if(float(valor) != 0):
						dic_terminos_cant[termino]+=1

	return (dic_terminos_valor,dic_terminos_cant)
#....------------------------------------------------------------------------------------------------------------------....
#-------------------------------------------------------------------------------------------------------------------------
#....------------------------------------------------------------------------------------------------------------------....	
	
if __name__ == '__main__':

	lista_de_medios = (CORPUS_RING_0_TN, CORPUS_RING_0_CLARIN, CORPUS_RING_0_LA_NACION, CORPUS_RING_0_LA_IZQUIERDA, CORPUS_RING_0_PAGINA_DOCE)
	
	writer = codecs.open(RESULTADOS, "a",encoding='utf8')
	
	writer.write("\n-------------------------------------------------------------------------------------------------\n");
	writer.write("Corpus Ring 0: Analisis de polaridad de cada medio sobre terminos seleccionados\n");
	writer.write("-------------------------------------------------------------------------------------------------\n\n");
	

	for medio in lista_de_medios:
		resultados = obtener_valor_promedio(medio)
		dic_terminos_valor = resultados[0]
		dic_terminos_cant = resultados[1]

		
		nombre_medio = medio.split('/')[-1][:-4]
		writer.write("\n" + nombre_medio + ":\n")
		for termino in dic_terminos_valor:
			valor = dic_terminos_valor[termino]
			if termino in dic_terminos_cant:
				cant = dic_terminos_cant[termino]
				valor = valor / cant
			writer.write("\n \"" + termino + "\" : " + str(valor))
	
		writer.write("\n")
		
	writer.close()