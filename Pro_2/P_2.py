# python3 P_2.py


import numpy as np
import pandas as pd
import collections as coll
import matplotlib as mpl
import matplotlib.pyplot as pl
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from matplotlib import ticker
from matplotlib import cm


def Plots(TBD_Partido, year, fig_name):

		# Asigna a cada partido politico presente en los datos de TBD un número entre 0 y 1:
	Part_Presentes = TBD_Partido.groupby(['Partido']).size()
	k = 0
	for i in Part_Presentes.index:
		Part_Presentes[i]=k/len(Part_Presentes)
		k = k+1
	
	Colores = pd.DataFrame()
	for i in TBD_Partido.index:
		Partido = TBD_Partido['Partido'][i]
		for j in Part_Presentes.index:
			if j == Partido:
				color_Part = Part_Presentes[j]
				Colores_aux = pd.DataFrame([color_Part], index=[i], columns=['Color_Part'])
				Colores = pd.concat([ Colores, Colores_aux ])
	TBD_Partido = TBD_Partido.merge( Colores, how='inner', left_index=True, right_index=True )
	
	cmap = cm.get_cmap('tab10')
	normalize = mcolors.Normalize(vmin = 0.0, vmax = 1.0)
	pl.rcParams['figure.figsize'] = [13, 10]
	
	TBD_Part = pl.figure()
	Part_Names = Part_Presentes.index.tolist()
	pl.title('Total Votos Partidos Dominantes por Depto vs TBD'+str(year), fontsize = 25, pad = 15)
	pl.ticklabel_format( axis='y', style='sci', scilimits=(0,0) )
	pl.ylabel('Total Votos', fontsize=18)
	pl.xlabel('TBD (%)', fontsize=18)
	pl.xticks(fontsize = 16)
	pl.yticks(fontsize = 16)
	
	AUX = TBD_Partido[[ year, 'Vot_Max', 'Prob_Part_Gan', 'Partido', 'Color_Part' ]]
	AUX1 = AUX.sort_values(year)
	x = AUX1[year].tolist()
	y = AUX1['Vot_Max'].tolist()
	Size_Points = AUX1['Prob_Part_Gan']*200
	Cols_Points = AUX1['Color_Part']
	Lab = year
	Scat_1 = pl.scatter( x, y, s=Size_Points,	alpha=0.5, label=Lab, c=Cols_Points, cmap=cmap)
	annotations = AUX1.index.tolist()
	for i, lab in enumerate(annotations):
		pl.annotate(lab, (x[i], y[i]), rotation=90)
	
	pl.legend(handles=Scat_1.legend_elements()[0], title='Partido', labels=Part_Names,
						bbox_to_anchor=(0., -0.18, 1, 0.5),	loc='lower right', ncol=3, mode='expand', borderaxespad=0.)
	pl.subplots_adjust(left = 0.075, bottom = 0.18, right = 0.95, top = 0.925)
	#pl.legend()#bbox_to_anchor=(0., -0.55, 1, 0.5), loc='lower right', ncol=3, mode='expand', borderaxespad=0.)
	
	TBD_Part.savefig(fig_name)
	pl.close(TBD_Part)




	# Archivo con los datos de las votaciones:
filename0 = 'Data_2018.csv'
Total_data = pd.read_csv(filename0, header=0)
N_Data = len(Total_data)

	# Archivo con los datos de desempleo por departamentos:
filename1 = 'Tasa_Bruta_Desempleo.csv'
Total_data1 = pd.read_csv(filename1, index_col='Depto', header=0)
N_Data1 = len(Total_data1)

	# Indica el número de veces que aparece un partido en la lista completa de votos:
	# En la columna 0 aparece el nombre del partido y en la columna 1 el número de veces que aparece dicho partido.
Partidos_Ganador = np.array(list(dict(coll.Counter(Total_data['Ganador_Circunscripción_Nacional'])).items()))
N_Parts = len(Partidos_Ganador)

	# Departamentos votantes:
	# En la columna 0 aparece el nombre del departamento y en la columna 1 el número de muncipios votantes.
Deptos = np.array(list(dict(coll.Counter(Total_data['Depto'])).items()))
N_Deps = len(Deptos)

	# Organizamos por orden alfabético los partidos y los departamentos:
sorted(Partidos_Ganador[:][0])
sorted(Deptos[:][0])

	# Creamos una tabla con el número de votos totales que los partidos ganadores obtuvieron por departamento:
Vot_Partidos_Depto = pd.DataFrame()
for i in range(N_Parts):
		# Nombre del partido ganador:
	P_Name = Partidos_Ganador[i][0]
		# Filtramos los datos para cada partido y vemos los municipios donde ganaron:
	Mun_por_Part = Total_data[ Total_data.Ganador_Circunscripción_Nacional == str( P_Name ) ]
	Vot_por_Part = pd.DataFrame()
	for j in range(N_Deps):
			# Nombre del departamento:
		Dep_Name = Deptos[j][0]
			# Filtramos los departamentos de acuerdo a los municipios donde el partido ganó:
		Vot_por_Municipio = Mun_por_Part[ Mun_por_Part.Depto == str( Dep_Name ) ]
		if not Vot_por_Municipio.empty:
				# Contamos los votos totales en el departamento para el partido que ganó:
			N_votos_Dep = np.sum( Vot_por_Municipio[ P_Name ] )
			Vot_por_Dept_aux = pd.DataFrame( [ N_votos_Dep ], index=[ str( Dep_Name ) ], columns=[ str( P_Name ) ] )
			Vot_por_Part = pd.concat( [ Vot_por_Part, Vot_por_Dept_aux ] )
	Vot_Partidos_Depto = Vot_Partidos_Depto.merge( Vot_por_Part, how='outer', left_index=True, right_index=True )

	# Reemplazar valores tipo NaN por 0
Vot_Partidos_Depto = Vot_Partidos_Depto.fillna(0)

	# Encuentra el partido con mayor votación por departamento y el total de votos obtenido:
Part_Gan_Depto = pd.DataFrame()
for i in Vot_Partidos_Depto.index:
		# Encuentra la mayor votación:
	maxim = np.max(Vot_Partidos_Depto.loc[i])
		# Votos totales en el departamento i:
	N_Votos = np.sum(Vot_Partidos_Depto.loc[i])
		# Probabilidad de tener el partido con mayor votación:
	Prob = maxim/N_Votos
		# Encuentra el partido con la mayor votación:
	Part_Gan = Vot_Partidos_Depto.loc[i].idxmax()
	Part_Gan_Depto_aux = pd.DataFrame([[ maxim, Prob, Part_Gan ]], index=[ i ], columns=[ 'Vot_Max', 'Prob_Part_Gan', 'Partido' ] )
	Part_Gan_Depto = pd.concat([ Part_Gan_Depto, Part_Gan_Depto_aux ])
TBD_Partido = Total_data1.merge( Part_Gan_Depto, how='inner', left_index=True, right_index=True )

 # Probabilidad de tener determinado partido politico por departamento:
Prob_Part_Depto = pd.DataFrame( index=Part_Gan_Depto.index, columns=Vot_Partidos_Depto.columns )
for j in Part_Gan_Depto.index:
	suma = np.sum( Vot_Partidos_Depto.loc[ j ] )
	for i in Vot_Partidos_Depto:
		Prob_Part_Depto.loc[ j ][ i ] = Vot_Partidos_Depto.loc[ j ][ i ]/suma

	# Guardamos los datos relevantes en un archivo csv:
#Vot_Partidos_Depto.to_csv('Votos_por_Departamento.csv')
#TBD_Partido.to_csv('TBD_Partido.csv')
#Prob_Part_Depto.to_csv('Prob_Part_Depto.csv')

year = 'Indice_2018'
fig_name = 'TBD_Part_2018.png'
Plots(TBD_Partido, year, fig_name)


year = 'Indice_2019'
fig_name = 'TBD_Part_2019.png'
Plots(TBD_Partido, year, fig_name)

year = 'Indice_2020'
fig_name = 'TBD_Part_2020.png'
Plots(TBD_Partido, year, fig_name)





























'''
pl.rcParams["figure.figsize"] = [13, 10]

Vot_por_Deptos = pl.figure()
pl.title('Votos Totales por Departamento', fontsize = 25, pad = 15)
pl.ticklabel_format( axis='y', style='sci', scilimits=(0,0) )
pl.ylabel('Total Votos', fontsize=18)
pl.xticks(rotation = 90)
pl.yticks(fontsize = 16)

for i in range(N_Parts):
		# Nombre del partido ganador:
	P_Name = str(Partidos_Ganador[i][0])
	lab = P_Name
	pl.plot(Vot_Partidos_Depto.index, Vot_Partidos_Depto[ P_Name ], '-o', label=lab)
	pl.subplots_adjust(left = 0.075, bottom = 0.35, right = 0.95, top = 0.925)
	pl.legend(bbox_to_anchor=(0., -0.55, 1, 0.5), loc='lower right', ncol=3, mode='expand', borderaxespad=0.)

Vot_por_Deptos.savefig('Votos_por_Depto.png', dpi = 500)
pl.close(Vot_por_Deptos)
'''




















