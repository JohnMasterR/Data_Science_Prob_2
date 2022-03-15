# python3 Prob_2.py


import numpy as np
import pandas as pd
import collections as coll
import matplotlib.pyplot as pl


filename = 'Data_2018.csv'
Total_data = pd.read_csv(filename, header=0)
N = len(Total_data)

	# Indica el número de veces que aparece un partido en la lista completa de votos:
	# En la columna 0 aparece el nombre del partido y en la columna 1 el número de veces que aparece dicho partido.
Conteo_por_Partido = np.array(list(dict(coll.Counter(Total_data['Ganador Circunscripción Nacional'])).items()))

sorted(Conteo_por_Partido[:][0])

n = len(Conteo_por_Partido)

N_Vot = 0
for i in range(n):
	Name_Partido = Conteo_por_Partido[i][0]
	Dep_name = []
	Vot_Dept = []
	for j in range(N):
		Partido_Ganador = Total_data['Ganador Circunscripción Nacional'][j]
		Votos_Municipio_Partido = Total_data[ str(Name_Partido) ][j]
		Depto_Partido = Total_data['Depto'][j]
		if Partido_Ganador == Name_Partido:
			N_Vot = N_Vot+Votos_Municipio_Partido
			Dep_name.append( Depto_Partido )
			Vot_Dept.append( [Depto_Partido, Votos_Municipio_Partido])
	Count_Dep_name = np.array(list(dict(coll.Counter(Dep_name)).items()))
	Vot_Dept = np.array(list(Vot_Dept))
	N_Deps = len(Count_Dep_name)
	print(Name_Partido, N_Deps, N_Vot, Count_Dep_name)
	#print( Count_Dep_name.size, len(Count_Dep_name), Count_Dep_name.ndim )
	print( np.sum(  Count_Dep_name[:,1].astype(int)  ) )
	N_Vot = 0



#print(Conteo_por_Partido, len(Conteo_por_Partido))

#aux=0
#for i in range(len(Conteo_por_Partido)):
	#aux=aux+int(Conteo_por_Partido[i][1])
#print(aux)


