# -*- coding: utf-8 -*-
"""evaluacion.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1u9pUZuQYwGyxzp8Ld3m3YU9UA1tck2Xt
"""

#Montar el drive
from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min

df = pd.read_csv('/content/drive/MyDrive/2- Unilibre/7moSemestre/programacionAvanzada/segundoCorte/data/analisis.csv')
df

print(df.info())

"""# 1) Cuantos usuarios hay por cada Categoría"""

df.groupby("categoria").size()

counts = df["categoria"].value_counts()
counts

fig, ax = plt.subplots(figsize=(40, 5))

frecuencias = df['categoria'].value_counts()
frecuencias.plot(kind='bar', color = 'blue')
plt.xticks(rotation=0)
plt.xlabel('Categoria')
plt.ylabel('Frecuencia')
plt.title('Diagrama de Frecuencia de las Categorias', fontweight = 'bold', fontsize=30, color = 'orange')

#Cuadricula
ax.grid(linestyle = '--', alpha = 0.3)

#Quitar unas margenes
ax.spines['top'].set_alpha(0.0)
ax.spines['right'].set_alpha(0.0)

plt.show()

"""# 2) Visualizar en histograma cada de unas las variables (op, co, ex, ag, ne, WorCount, Categoria)"""

df.drop(['categoria'],1).hist()
plt.show()

for col in df.columns:
  if df[col].dtype == int or df[col].dtype == float:
    #Grafica fid = todo, axes = rectangulo
    fig, ax = plt.subplots(figsize=(20, 4))
    
    #Cuantos datos sin repetirse existen en la columna
    num_bins = df[col].nunique()

    #Cuadricula
    ax.grid(linestyle = '--', alpha = 0.3)

    #Quitar unas margenes
    ax.spines['top'].set_alpha(0.0)
    ax.spines['right'].set_alpha(0.0)

    plt.hist(df[col], bins=num_bins, color='b', rwidth=0.75)
    plt.xlabel(col)
    plt.ylabel('Frecuencia')
    plt.title('Histograma de ' + col, fontweight = 'bold', fontsize=30, color = 'orange')
    plt.show()

fig, ax = plt.subplots(figsize=(10, 4))
df["op"].hist(bins=10, color="red")
plt.xlabel('variable op')
plt.ylabel('Frecuencia')
plt.title('Histograma de la variable op', fontweight = 'bold', fontsize=10, color = 'orange')
plt.show()

fig, ax = plt.subplots(figsize=(10, 4))
df["co"].hist(bins=10, color="red")
plt.xlabel('variable co')
plt.ylabel('Frecuencia')
plt.title('Histograma de la variable co', fontweight = 'bold', fontsize=10, color = 'orange')
plt.show()

fig, ax = plt.subplots(figsize=(10, 4))
df["ex"].hist(bins=10, color="red")
plt.xlabel('variable ex')
plt.ylabel('Frecuencia')
plt.title('Histograma de la variable ex', fontweight = 'bold', fontsize=10, color = 'orange')
plt.show()

fig, ax = plt.subplots(figsize=(10, 4))
df["ag"].hist(bins=10, color="red")
plt.xlabel('variable ag')
plt.ylabel('Frecuencia')
plt.title('Histograma de la variable ag', fontweight = 'bold', fontsize=10, color = 'orange')
plt.show()

fig, ax = plt.subplots(figsize=(10, 4))
df["ne"].hist(bins=10, color="red")
plt.xlabel('variable ne')
plt.ylabel('Frecuencia')
plt.title('Histograma de la variable ne', fontweight = 'bold', fontsize=10, color = 'orange')
plt.show()

fig, ax = plt.subplots(figsize=(10, 4))
df["wordcount"].hist(bins=10, color="red")
plt.xlabel('variable wordcountop')
plt.ylabel('Frecuencia')
plt.title('Histograma de la variable wordcount', fontweight = 'bold', fontsize=10, color = 'orange')
plt.show()

fig, ax = plt.subplots(figsize=(10, 4))
df["categoria"].hist(bins=10, color="red")
plt.xlabel('variable categoria')
plt.ylabel('Frecuencia')
plt.title('Histograma de la variable categoria', fontweight = 'bold', fontsize=10, color = 'orange')
plt.show()

"""# 3) Encuentre el número de cluster (K) mediante código"""

df

#Se selecionan unos datos al azar para posteriormente verificar el clúster 
#al que pertenecen
indices = [4, 50, 136]
muestras = pd.DataFrame(df.loc[indices], columns = df.keys()).reset_index(drop = True)
df = df.drop(indices, axis = 0)
nuevo_df = pd.DataFrame(df[['usuario', 'op', 'co', 'ex', 'ag', 'ne', 'wordcount']])
nuevo_muestras = pd.DataFrame(muestras[['usuario', 'op', 'co', 'ex', 'ag', 'ne', 'wordcount']])
df

#Eliminamos la columna de usuario y categoria
df = df.drop(['usuario', 'categoria'], axis = 1)
muestras = muestras.drop(['usuario', 'categoria'], axis = 1)

#Se realiza el escalamiento de los datos
from sklearn import preprocessing

data_escalada = preprocessing.Normalizer().fit_transform(df)
muestras_escalada = preprocessing.Normalizer().fit_transform(muestras)

print(muestras)

print(muestras_escalada)

# Hallar el valor óptimo de K
#Se aplicará el método de codo para hallar K
#Se calcula el algoritmo de agrupación para diferentes valores de K
from sklearn.cluster import KMeans

X = data_escalada.copy()
inercia = [] 
for i in range(1, 15):
    algoritmo = KMeans(n_clusters = i, init = 'k-means++', 
                       max_iter = 300, n_init = 10)
    algoritmo.fit(X)
    #Para cada K, se calcula la suma total del cuadrado dentro del clúster
    inercia.append(algoritmo.inertia_)

#Se traza la curva de la suma de errores cuadráticos 
plt.figure(figsize=[10,6])
plt.title('Método del Codo')
plt.xlabel('No. de clusters')
plt.ylabel('Inercia')
plt.plot(list(range(1, 15)), inercia, marker='o')
plt.show()

"""# 4) Realice un clustering (KMeans) de dicha data (Debe generar una gráfica como resultado final de las seis variables – no incluya categoría)"""

## Se aplica el algoritmo de clustering ##
#Se define el algoritmo junto con el valor de K
algoritmo = KMeans(n_clusters = 5, init = 'k-means++', max_iter = 300, n_init = 10)
#Se entrena el algoritmo
algoritmo.fit(X)

#Se obtiene los datos de los centroides y las etiquetas
centroides, etiquetas = algoritmo.cluster_centers_, algoritmo.labels_
print(centroides)

print(etiquetas)

#Utilicemos los datos de muestras y verifiquemos en que cluster se encuentran
muestra_prediccion = algoritmo.predict(muestras_escalada)
for i, pred in enumerate(muestra_prediccion):
    print("Muestra", i, "se encuentra en el clúster:", pred)

### GRAFICAR LOS DATOS JUNTO A LOS RESULTADOS ###
# Se aplica la reducción de dimensionalidad a los datos
from sklearn.decomposition import PCA
modelo_pca = PCA(n_components = 2)
modelo_pca.fit(X)
pca = modelo_pca.transform(X) 
#Se aplicar la reducción de dimsensionalidad a los centroides
centroides_pca = modelo_pca.transform(centroides)

# Se define los colores de cada clúster
colores = ['blue', 'red', 'green', 'orange', 'gray']

#Se asignan los colores a cada clústeres
colores_cluster = [colores[etiquetas[i]] for i in range(len(pca))]

"""# a. Imprima los centroides"""

#Se grafica los componentes PCA
fig = plt.figure(figsize=(10,6))
#Se grafican los centroides
plt.scatter(centroides_pca[:, 0], centroides_pca[:, 1], marker = 'x', s = 150, linewidths = 2, c = colores)

#Se grafica los componentes PCA
fig = plt.figure(figsize=(10,6))
plt.scatter(pca[:, 0], pca[:, 1], c = colores_cluster, marker = 'o', alpha = 0.5)
#Se grafican los centroides
plt.scatter(centroides_pca[:, 0], centroides_pca[:, 1], marker = 'x', s = 150, linewidths = 2, c = colores)

"""# b. Imprima las etiquetas"""

#Se grafica los componentes PCA
fig = plt.figure(figsize=(10,6))
plt.scatter(pca[:, 0], pca[:, 1], c = colores_cluster, marker = 'o', alpha = 0.5)
#Se grafican los centroides
plt.scatter(centroides_pca[:, 0], centroides_pca[:, 1], marker = 'x', s = 150, linewidths = 2, c = colores)
for i, txt in enumerate(centroides_pca):
    plt.annotate("Centroide", (centroides_pca[i, 0], centroides_pca[i, 1]), xytext=(10,10), textcoords='offset points')

#Se guadan los datos en una variable para que sea fácil escribir el código
xvector = modelo_pca.components_[0] * max(pca[:,0])
yvector = modelo_pca.components_[1] * max(pca[:,1])
columnas = df.columns

print(xvector)

print(yvector)

print(columnas)

#Se repite esta primera parte
fig = plt.figure(figsize=(10,6))
plt.scatter(pca[:, 0], pca[:, 1], c = colores_cluster, marker = 'o', alpha = 0.5)
#Se grafican los centroides
plt.scatter(centroides_pca[:, 0], centroides_pca[:, 1], marker = 'x', s = 100, linewidths = 3, c = colores)

for i in range(len(columnas)):
    #Se grafican los vectores
    plt.arrow(0, 0, xvector[i], yvector[i], color = 'blue', 
              width = 0.0005, head_width = 0.02, alpha = 0.75)
    #Se colocan los nombres
    plt.text(xvector[i], yvector[i], list(columnas)[i], color='black', 
             alpha=0.85)
plt.show()

"""# c. Imprima cuantos usuarios hay por cada grupo"""

repeticiones = {}

for nombre in colores_cluster:
    repeticiones[nombre] = colores_cluster.count(nombre)

for categoria in repeticiones.keys():
  print("La categoria\t" + str(categoria) + "\ttiene\t" + str(repeticiones.get(categoria)) + "\tusuarios")

"""# d. Imprima los usuarios de un cluster específico"""

#Este DataFrame "nuevo_df" fue creado antes de eliminar la columna nombre y categoria iniciando el punto 3
#A cada usuario de le asigna su correspondiente categoria
nuevo_df['categoria_cluster'] = colores_cluster

#Se selecciona el color de la categoria que se quiere imprimir
usuarios_categoria = nuevo_df.loc[nuevo_df['categoria_cluster'] == 'green']
print(len(usuarios_categoria))
usuarios_categoria

"""# e. Imprima el representante de cada grupo"""

cercanos, _ = pairwise_distances_argmin_min(algoritmo.cluster_centers_, X)
cercanos
users = df['usuario'].values
for fila in cercanos:
  print(users[fila])

"""# f. Clasifique ahora un nuevo usuario (registro)"""

nuevo_muestras

new_labels= algoritmo.predict(muestras_escalada)
print(new_labels)