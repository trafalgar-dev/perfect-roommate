import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import streamlit as st

# TABLA DE COMPATIBILIDAD
def compatibilidad(compatib):
  compatib /= 100                         #Escala 1 a 0
  fig, ax = plt.subplots(figsize=(5,4))   #Datos para la grafica
  sns.barplot(x=compatib.index, y=compatib.values, ax=ax, color='blue')   #Grafica de barras
  sns.despine(top=True,right=True,left=True,bottom=True)     #Elimina las lineas del grafico
  
  # Etiquetas configuracion 
  ax.set_xlabel('ID roomie', fontsize=10) #Etiqueta eje X
  ax.set_ylabel('Compatibility(%)', fontsize=10) # Etiqueta eje Y
  ax.set_xticklabels(ax.get_xticklabels(), rotation=45) #Rotacion de las etiquetas
  # Ajustar etiqueta y con porcentajes
  ax.set_yticklabels(['{:.1f}%'.format(y*100) for y in ax.get_yticks()], fontsize=9)  
  # Etiqueta de cada barra
  for p in ax.patches:
    height = p.get_height()
    ax.annotate('{:.1f}%'.format(height*100),
                (p.get_x()+p.get_width()/2., height),
                ha='center', va='center', 
                xytext=(0, 5),
                textcoords='offset points', fontsize=8)
  return (fig)

#GENERAR TABLA DE ROOMIES
def tabla_compatibilidad(resultado):
  resultado_0_with_index=resultado[0].reset_index()  #Convierte el indice en una columna
  resultado_0_with_index.rename(columns={'index':'Atributo'}, inplace=True) #Renombra la columna
  
  #Configuracion grafica
  fig_table=go.Figure(data=[go.Table(
    columnwidth=[20]+[10]*(len(resultado_0_with_index.columns)-1), #Ancho de las columnas
    header=dict(values=list(resultado_0_with_index.columns), #Nombres de las columnas
                fill_color='paleturquoise',#Color de relleno
                align='left'),  #Alineamiento y tipo de letra                 
          cells=dict(values=[resultado_0_with_index[col] for col in resultado_0_with_index.columns],
                   fill_color='lavender',
                   align='left'))
  ])
  
 #Configuracion grafica
  fig_table.update_layout(
    width=700, height=320,  #Ancho y alto de la grafica
    margin=dict(l=0, r=0, t=0, b=0)
  )
  return(fig_table)

#ROOMIES SEMILLA
def roomies_seed(roomies1,roomies2,roomies3,topn):
  #Crear lista de identificadores  inquilinos ingresados a INT
  id_roomies =[]
  for roomie in [roomies1,roomies2,roomies3]:
    try :
      if roomie:
        id_roomies.append(int(roomie))
    
    except ValueError:
      st.error(f'Se requieren `{roomie}`no es un numero valido')
      id_roomies=[]
  return (id_roomies)