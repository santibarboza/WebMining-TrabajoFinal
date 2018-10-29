import os
#PROGRAMA PRINCIPAL:

#Constantes de programa utilizadas
CARPETA_SCRIPTS_AUXILIARES = "ScriptsAuxiliares/"

PASO6 = "Analisis_Clustering_EM3.py"
PASO7 = "Analisis_Clustering_EM5.py"

S = "U.py"

#PASO 6: Clusters EM 3
fname = CARPETA_SCRIPTS_AUXILIARES + S
execfile(fname)

t = {"Macri","Massa","Vido","Cristina","Randazzo","Boudou","Carrio","Kirchner","trabajadores","fueros"}
print(str(t))
