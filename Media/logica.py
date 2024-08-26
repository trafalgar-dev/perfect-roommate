import numpy as np
import pandas as pd
from sklearn.preprocessing  import OneHotEncoder 

#Leemos la base de datos
df=pd.read_csv('C:/Users/PC HOME/Desktop/PROGRAMACION/WORKSPACE/perfect-roommate/Media/dataset_inquilinos.csv', index_col='id_inquilino')

#Definimos las columnas
df.columns=['horario','bioritmo','nivel_educativo','leer','animacion','cine','mascotas','cocinar','deporte','dieta','fumador','viistas','orden','musica_tipo','musica_alta','plan_perfecto','ínstrumento']

#ONE HOT ENCODING
encoder= OneHotEncoder(sparse_output=False) #Creamos el encoder
df_encoder= encoder.fit_transform(df) #Aplicamos el encoder
encoded_features_names= encoder.get_feature_names_out() #Obtenemos las columnas codificadas

#MATRIZ DE SEMEJANZA
matriz_s= np.dot(df_encoder,df_encoder.T)

#Rango de destino
rango_min=-100
rango_max=100

#Rangos matriz
min_original=np.min(matriz_s)
max_original=np.max(matriz_s)

#Reescalamos la matriz
matriz_s_rees=(matriz_s-min_original)/(max_original-min_original)*(rango_max-rango_min)+rango_min

#Pasar a Pandas
df_semejanza=pd.DataFrame(matriz_s_rees, index=df.index, columns=df.index)


#COMPARACION DE INQUILINOS
def roomies_compatibles(id_roomies,topn):
   
   #Validaciones de ID de los roomies
   for id_roomie in id_roomies:
     if id_roomie not in df_semejanza.index:
       return 'Al menos uno de los roomies no encontrados'
   
   #Obtención de las filas de los inquilinos
   filas_roomies=df_semejanza.loc[id_roomies] 
   
   #Cálculo de la semejanza promedio
   semejanza_promedio= filas_roomies.mean(axis=0)  
   
   #Ordenamiento de las semejanzas de manera descendente
   roomies_similares=semejanza_promedio.sort_values(ascending=False)  
   
   #Eliminación de los inquilinos de referencia
   roomies_similares=roomies_similares.drop(id_roomies) 
   
   #Obtención de los top N roomies más similares
   topn_roomies= roomies_similares.head(topn) 
   
   #Obtención de los registros de los roomies similares
   registros_similares= df.loc[topn_roomies.index]  
   
   #Obtención de los registros de los inquilinos de referencia
   registros_buscados=  df.loc[id_roomies]  
   
   #Concatenación de los inquilinos de referencia y los similares
   resultado = pd.concat([registros_buscados.T,registros_similares.T], axis=1) 
   
   #Creación de una serie con las semejanzas
   similares_series= pd.Series(data=topn_roomies.values, index=topn_roomies.index, name='Semejanza') 
   
   return (resultado, similares_series)