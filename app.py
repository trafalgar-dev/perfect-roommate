import streamlit as st
import pandas as pd
from logica import roomies_compatibles
from componentes import  compatibilidad,roomies_seed, tabla_compatibilidad

st.set_page_config(layout="wide")
resultado=None

st.markdown(f'<div style="margin-top: 60px;"></div>', unsafe_allow_html=True)
with st.sidebar:
  st.header("PERFECT ROOMMATE")
  roomies1 = st.text_input('Roomie 1')
  roomies2 = st.text_input('Roomie 2')
  roomies3 = st.text_input('Roomie 3')
  
  num_companeros = st.text_input("Cuantos inquilinos son?")
  
  
  if st.button('Buscar nuevos companeros'):
    try:
      topn=int(num_companeros)
    except ValueError:
      st.error('Ingrese valor valido')
      topn=None
      
    id_roomies = roomies_seed(roomies1,roomies2,roomies3,topn)
    if id_roomies and topn is not None:
      resultado= roomies_compatibles(id_roomies,topn)
if isinstance(resultado,str):
  st.error(resultado)
elif resultado is not None:
  cols = st.columns((1,2))
  
  with cols[0]:
    st.write("Nivel de compatibilida de cada compañero nuevo")
    fig_grafico=compatibilidad(resultado[1])
    st.pyplot(fig_grafico)
  with cols[1]:
    st.write("Comparativa entre compañeros")
    fig_tabla=tabla_compatibilidad(resultado)
    st.plotly_chart(fig_tabla,use_container_width=True)
   