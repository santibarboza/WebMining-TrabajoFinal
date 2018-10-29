#ObtenerEnlaces.py - Obtiene enlaces delos canales RSS de distintos medios

import feedparser
import time
from subprocess import check_output
import codecs
import requests
import sys

# Descriptores de archivos de contenidos
TN = "ScriptsAuxiliares/Archivos/TodoNoticias.txt"
CLARIN = "ScriptsAuxiliares/Archivos/Clarin.txt"
LA_NACION = "ScriptsAuxiliares/Archivos/LaNacion.txt"
PAGINA_DOCE = "ScriptsAuxiliares/Archivos/PaginaDoce.txt"
LA_IZQUIERDA = "ScriptsAuxiliares/Archivos/LaIzquierda.txt"

# URLs de canales RSS de cada medio
TN_RSS = "http://tn.com.ar/feed/politica"
CLARIN_RSS = "https://www.clarin.com/rss/politica"
LA_NACION_RSS = "http://contenidos.lanacion.com.ar/herramientas/rss/categoria_id=30"
PAGINA_DOCE_RSS = "https://www.pagina12.com.ar/rss/secciones/el-pais/notas"
LA_IZQUIERDA_RSS = "http://www.laizquierdadiario.com/spip.php?page=backend&id_mot=12"
#AMBITO_FINANCIERO_RSS = "http://www.ambito.com/rss/noticias.asp?s=Pol%C3%ADtica"
#TELAM_RSS = "http://www.telam.com.ar/rss2/politica.xml"

lista_archivos = (TN, CLARIN, LA_NACION, PAGINA_DOCE, LA_IZQUIERDA)

lista_rss = (TN_RSS, CLARIN_RSS, LA_NACION_RSS, PAGINA_DOCE_RSS, LA_IZQUIERDA_RSS)

numero_item = 0
for item in lista_archivos:
	d = feedparser.parse(lista_rss[numero_item])
	writer = codecs.open(lista_archivos[numero_item], "a",encoding='utf8')
	for post in d.entries:
		l = post.link
		writer.write(l + "\n")
	writer.close()
	numero_item = numero_item + 1

