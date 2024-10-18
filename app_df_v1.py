import streamlit as st
import pandas as pd
from DJIGTFLM import DJIGTFLM  # Importa tu clase desde el archivo DJIGTFLM.py

# Título de la aplicación
st.title('Verificación de juegos para las DJs - IGT')

# Agregar el logo de IGT
st.image('igt_logo.png', width=200)  # Asegúrate de que el logo esté en el directorio del proyecto

# Descripción de la aplicación
st.write("""
Esta aplicación te permite analizar los nuevos juegos disponibles y determinar si se pueden añadir, actualizar o 
si ya están presentes en el servidor del cliente. Carga los archivos requeridos para realizar el análisis.
""")

# Subir archivos Excel
zjam_file = st.file_uploader("Subir archivo zjam.xlsx", type="xlsx")
lista_actual_file = st.file_uploader("Subir lista_actual.xlsx", type="xlsx")
df_new_games_file = st.file_uploader("Subir juegos_nuevos.xlsx", type="xlsx")

# Verificar si los tres archivos han sido cargados
if zjam_file and lista_actual_file and df_new_games_file:
    # Convertir los archivos subidos en DataFrames de pandas
    zjam = pd.read_excel(zjam_file)
    lista_actual = pd.read_excel(lista_actual_file)
    df_new_games = pd.read_excel(df_new_games_file)
    
    # Crear una instancia de la clase DJIGTFLM
    resultado = DJIGTFLM(zjam, lista_actual, df_new_games)
    
    # Obtener el DataFrame con los resultados
    df_resultado = resultado.df_newGames()

    # Mostrar los resultados en la aplicación web
    st.write("Resultados del análisis de nuevos juegos:")
    st.dataframe(df_resultado[["Material", "GameTitle", "Them ID", "Version", "Type Cabinet", "Status", "label"]])

    # Exportar el DataFrame a un archivo Excel
    df_resultado[["Material", "GameTitle", "Them ID", "Version", "Type Cabinet", "Status", "label"]].to_excel("export.xlsx", index=False)
    
    # Botón para descargar el archivo exportado
    with open("export.xlsx", "rb") as file:
        st.download_button(
            label="Descargar el archivo Excel",
            data=file,
            file_name="resultados_juegos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

else:
    st.warning('Por favor, sube los tres archivos Excel para ejecutar el análisis.')
