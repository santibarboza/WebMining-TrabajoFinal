import os
#PROGRAMA PRINCIPAL:

#Constantes de programa utilizadas
CARPETA_SCRIPTS_AUXILIARES = "ScriptsAuxiliares/"

PASO1 = "ObtenerEnlaces.py"
PASO2 = "ObtenerCuerpoNoticias.py"
PASO3 = "AnalisisRing1.py"
PASO4_A = "AnalisisRing0_A.py"
PASO4_B = "AnalisisRing0_B.py"
PASO5 = "AnalisisRing2.py"

#setup (PASO 0)
path_Archivos = CARPETA_SCRIPTS_AUXILIARES + "Archivos"
path_Corpus = CARPETA_SCRIPTS_AUXILIARES + "Corpus/"
path_Ring0 = path_Corpus + "Ring0"
path_Ring1 = path_Corpus + "Ring1"
path_Ring2 = path_Corpus + "Ring2"
path_Noticias = CARPETA_SCRIPTS_AUXILIARES + "Noticias/"
path_TN = path_Noticias + "TN"
path_Cl = path_Noticias + "Clarin"
path_LN = path_Noticias + "LaNacion"
path_LI = path_Noticias + "LaIzquierda"
path_PD = path_Noticias + "PaginaDoce"
path_Weka = CARPETA_SCRIPTS_AUXILIARES + "ResultadosWeka"

#Creacion de carpetas de trabajo
if not os.path.exists(path_Archivos):
    os.makedirs(path_Archivos)

if not os.path.exists(path_Ring0):
    os.makedirs(path_Ring0)
if not os.path.exists(path_Ring1):
    os.makedirs(path_Ring1)
if not os.path.exists(path_Ring2):
    os.makedirs(path_Ring2)

if not os.path.exists(path_TN):
    os.makedirs(path_TN)
if not os.path.exists(path_Cl):
    os.makedirs(path_Cl)
if not os.path.exists(path_LN):
    os.makedirs(path_LN)
if not os.path.exists(path_LI):
	os.makedirs(path_LI)
if not os.path.exists(path_PD):
    os.makedirs(path_PD)

if not os.path.exists(path_Weka):
    os.makedirs(path_Weka)

#PASO 1: Recuperacion automatica de enlaces a noticias por medio de feeds RSS
fname = CARPETA_SCRIPTS_AUXILIARES + PASO1
execfile(fname)

#PASO 2: Recuperacion de cuerpo de texto de las noticias recolectadas
#Generacion de corpus global y corpus para cada portal
#Filtrado sintactico, aplicacion de Das-Chen
fname = CARPETA_SCRIPTS_AUXILIARES + PASO2
execfile(fname)

#PASO 3: Analisis nivel Ring1 (naive): contempla cuantos terminos no neutrales
#utiliza en redaccion cada portal
fname = CARPETA_SCRIPTS_AUXILIARES + PASO3
execfile(fname)

#PASO 4: Analisis nivel Ring0: estudio de sentimientos por oracion en torno
#a lista de terminos X (hardcodeados) previamente seleccionados
fname = CARPETA_SCRIPTS_AUXILIARES + PASO4_A
execfile(fname)

fname = CARPETA_SCRIPTS_AUXILIARES + PASO4_B
execfile(fname)

#PASO 5: Analisis nivel Ring2: estimacion de similaridad entre noticias; generacion
#de matriz de similitud por coseno entre noticias de todos los portales
fname = CARPETA_SCRIPTS_AUXILIARES + PASO5
execfile(fname)