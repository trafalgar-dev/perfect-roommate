import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import streamlit as st

# FUNCION PARA GENERAR LA GRAFICA DE COMPATIBILIDAD
def compatibilidad(compatib):
    compatib /= 100  # Escalar de 1 a 0
    fig, ax = plt.subplots(figsize=(5, 4))  # Crear una figura y un eje para la gráfica
    sns.barplot(x=compatib.index, y=compatib.values, ax=ax, color='blue')  # Crear gráfica de barras
    sns.despine(top=True, right=True, left=True, bottom=True)  # Eliminar las líneas del gráfico
    
    # Configuración de etiquetas
    ax.set_xlabel('ID roomie', fontsize=10)  # Etiqueta del eje X
    ax.set_ylabel('Compatibility (%)', fontsize=10)  # Etiqueta del eje Y
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)  # Rotación de las etiquetas del eje X
    
    # Ajustar etiqueta y con porcentajes
    ax.set_yticklabels(['{:.1f}%'.format(y * 100) for y in ax.get_yticks()], fontsize=9)
    
    # Etiquetas en cada barra
    for p in ax.patches:
        height = p.get_height()
        ax.annotate('{:.1f}%'.format(height * 100),
                    (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='center',
                    xytext=(0, 5),
                    textcoords='offset points', fontsize=8)
    return fig

# FUNCION PARA GENERAR LA TABLA DE COMPATIBILIDAD
def tabla_compatibilidad(resultado):
    resultado_0_with_index = resultado[0].reset_index()  # Convierte el índice en una columna
    resultado_0_with_index.rename(columns={'index': 'Atributo'}, inplace=True)  # Renombrar la columna
    
    # Configuración gráfica
    fig_table = go.Figure(data=[go.Table(
        columnwidth=[20] + [10] * (len(resultado_0_with_index.columns) - 1),  # Ancho de las columnas
        header=dict(values=list(resultado_0_with_index.columns),  # Nombres de las columnas
                    fill_color='paleturquoise',  # Color de relleno
                    align='left'),  # Alineamiento y tipo de letra                 
        cells=dict(values=[resultado_0_with_index[col] for col in resultado_0_with_index.columns],
                   fill_color='lavender',
                   align='left'))
    ])
    
    # Configuración de la tabla
    fig_table.update_layout(
        width=700, height=320,  # Ancho y alto de la tabla
        margin=dict(l=0, r=0, t=0, b=0)  # Márgenes
    )
    return fig_table

# FUNCION PARA VALIDAR Y DEVOLVER IDs DE ROOMIES
def roomies_seed(roomies1, roomies2, roomies3, topn):
    # Crear lista de identificadores de inquilinos ingresados a INT
    id_roomies = []
    for roomie in [roomies1, roomies2, roomies3]:
        try:
            if roomie:
                id_roomies.append(int(roomie))
        except ValueError:
            st.error(f'Se requiere que `{roomie}` sea un número válido')
            id_roomies = []  # Reiniciar lista en caso de error
    return id_roomies
