"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""
import pandas as pd
import numpy as np
import os
import re  

def pregunta_01():
    df = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";", encoding='utf-8')
    
    
    # borrar columnas innecesarias
    df= df.drop('Unnamed: 0', axis=1)
    
    # poner en formato fecha (normalizar antes)
    def normalizar_fecha(texto):
        try:
            if re.match(r'^\d{4}/\d{1,2}/\d{1,2}$', str(texto)):
                partes = texto.split('/')
                año = partes[0]
                mes = partes[1].zfill(2)
                dia = partes[2].zfill(2)
                return f"{dia}/{mes}/{año}"
            else:
                return texto
        except:
            return texto

    df['fecha_de_beneficio'] = df['fecha_de_beneficio'].apply(normalizar_fecha)
    df['fecha_de_beneficio'] = pd.to_datetime(df['fecha_de_beneficio'], errors='coerce', dayfirst=True)

    # Reemplazar valores nulos solo en columnas que lo necesitan
    columnas_con_na = ['sexo', 'idea_negocio', 'línea_credito', 'estrato', 'barrio']
    df[columnas_con_na] = df[columnas_con_na].replace(["", " ", "NA", "N/A", "nan", "NaN"], np.nan)

    # poner en minúscula los valores de las columnas categóricas
    for col in ['sexo', 'tipo_de_emprendimiento', 'idea_negocio', 'línea_credito', 'estrato', 'barrio']:
        df[col] = df[col].apply(lambda x: x.lower() if isinstance(x, str) else x)
    
    # Arreglar columna idea_negocio
    df['idea_negocio'] = df['idea_negocio'].str.replace('_', ' ').str.replace('-', ' ')
    df['idea_negocio'] = df['idea_negocio'].str.strip()

    # Arreglar columna barrio
    df['barrio'] = df['barrio'].str.replace('_', ' ').str.replace('-', ' ')

    
    # Arreglar columna monto
    df['monto_del_credito'] = df['monto_del_credito'].str.replace('$', '').str.replace('_', ' ').str.replace('-', ' ')
    df['monto_del_credito'] = df['monto_del_credito'].str.replace(' ', '') 
    df['monto_del_credito'] = df['monto_del_credito'].str.replace(',', '') 
    df['monto_del_credito'] = df['monto_del_credito'].astype(float)

    # Arreglar columna línea_credito
    df['línea_credito'] = df['línea_credito'].str.replace('_', ' ').str.replace('-', ' ')
    df['línea_credito'] = df['línea_credito'].str.strip()

    
    # Eliminar filas con nulos en columnas
    df = df.dropna()

    # Eliminar filas duplicadas
    df = df.drop_duplicates()

    #creo la carpeta de salida si no existe
    if not os.path.exists("files/output"):
        os.makedirs("files/output")
    # Guardar el DataFrame limpio en un archivo CSV
    df.to_csv("files/output/solicitudes_de_credito.csv",sep=";", index=False)

    return df

if __name__ == "__main__":
    df=pregunta_01()
    print(df.head())
    print(df.columns)
    print(df.info())
    print(df.sexo.value_counts())
    print(df.sexo.value_counts().to_list())
    #print(f"Valores unicos: {df['barrio'].unique()}")
    #print(df.index.value_counts())
    #print(df.tipo_de_emprendimiento.value_counts())
    #print(df.idea_negocio.value_counts())
    #print(df.barrio.value_counts())
    #print(df.estrato.value_counts())
    #print(df.comuna_ciudadano.value_counts())
    #print(df.fecha_de_beneficio.value_counts())
    #print(df.línea_credito.value_counts())
    #df.monto_del_credito.value_counts().to_csv("files/input/monto_frecuencia.csv")
    #df.fecha_de_beneficio.value_counts().to_csv("files/input/fechas_frecuencia.csv")
    #df.barrio.value_counts().to_csv("files/input/barrios_frecuencia.csv")
    #duplicadas = df[df.duplicated()]
    #print(duplicadas)
    #df.to_csv("files/input/df.csv", index=False)
    #num_duplicadas = df.duplicated().sum()
    #print(f"Número de filas duplicadas: {num_duplicadas}")
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
