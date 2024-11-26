import streamlit as st
import base64
import pandas as pd
import matplotlib.pyplot as plt

# Cargar el dataset
pf = pd.read_csv("spotify_songs_dataset.csv")
image_path = "pages/Necesarios/fondo_morado.png"

# Codificar la imagen en base64
with open(image_path, "rb") as img_file:
    base64_image = base64.b64encode(img_file.read()).decode()

# Aplicar estilo de fondo a la aplicación
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{base64_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        color: #f0f0f0;
    }}
    
    .stButton > button {{
        background-color: #6a0dad;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        border: none;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: background-color 0.3s ease;
    }}

    .stButton > button:hover {{
        background-color: #9b4de1;
    }}
    
    .stHeader {{
        color: #ffffff;
    }}
    
    .stTitle {{
        font-size: 32px;
        font-weight: bold;
        color: #ffffff;
    }}
    
    .stText {{
        font-size: 16px;
        color: #d1d1d1;
    }}
    
    .stMarkdown {{
        color: #d1d1d1;
    }}
    
    table {{
        width: 100%;
        margin-top: 20px;
        border-collapse: collapse;
    }}
    
    table, th, td {{
        border: 1px solid #d1d1d1;
        text-align: left;
    }}
    
    th {{
        background-color: #9b4de1;
        color: white;
        padding: 10px;
    }}
    
    td {{
        background-color: #3c2a5e;
        color: white;
        padding: 8px;
    }}
    
    .stSelectbox, .stSlider {{
        background-color: #9b4de1;
        color: white;
        border-radius: 5px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Configuración inicial para la página y subpágina actual
if "page" not in st.session_state:
    st.session_state.page = "inicio"

if "subpage" not in st.session_state:
    st.session_state.subpage = None

# Función para cambiar la página principal
def cambiar_pagina(nueva_pagina):
    st.session_state.page = nueva_pagina
    if nueva_pagina != "categoría_2":
        st.session_state.subpage = None  # Resetear la subpágina solo si no estamos en "categoría_2"

# Función para cambiar la subpágina dentro de "Tipos"
def cambiar_subpagina(nueva_subpagina):
    st.session_state.subpage = nueva_subpagina

# Título de la aplicación
st.title("Aplicación Genérica")

# Mostrar botones solo si estamos en la página de inicio
if st.session_state.page == "inicio":
    st.header("Seleccione una opción")
    
    # Utilizar columnas para alinear los botones horizontalmente
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Opción 1"):
            cambiar_pagina("categoría_1")
    with col2:
        if st.button("Opción 2"):
            cambiar_pagina("categoría_2")
    
    with col3:
        if st.button("Opción 3"):
            cambiar_pagina("categoría_3")

# Mostrar contenido según la página seleccionada
elif st.session_state.page == "categoría_1":
    opciones = ["Todo"] + pf.columns.tolist()  # Agregar "Todo" a las opciones
    seleccion = st.selectbox("Selecciona una columna para ver", opciones)

    # Mostrar el DataFrame completo o la columna seleccionada
    if seleccion == "Todo":
        st.write("Base de datos completa:")
        st.dataframe(pf)  # Muestra todo el DataFrame
    else:
        st.write(f"Columna seleccionada: {seleccion}")
        st.write(pf[seleccion])
    if st.button("Volver atrás"):
        cambiar_pagina("inicio")

elif st.session_state.page == "categoría_2":
    # Manejar las subpáginas de la categoría "Opción 2"
    if st.session_state.subpage is None:
        st.header("Seleccione una subcategoría")
        # Mostrar botones para las subcategorías
        if st.button("Gráfico de Contenido Explícito"):
            cambiar_subpagina("subcategoria_a")
        if st.button("Distribución de Idioma de Canciones"):
            cambiar_subpagina("subcategoria_b")
        if st.button("Tendencia de Lanzamiento de Canciones"):
            cambiar_subpagina("subcategoria_c")
        if st.button("Duración Promedio por Género"):
            cambiar_subpagina("subcategoria_d")
        if st.button("Subcategoría E"):
            cambiar_subpagina("subcategoria_e")
        
        if st.button("Volver atrás"):
            cambiar_pagina("inicio")
    
    # Manejo de subpáginas específicas
    else:
        if st.session_state.subpage == "subcategoria_a":
            st.header("Subcategoría A: Contenido Explícito")
            st.write("Aquí se mostrarán los datos de la Subcategoría A.")
            pf_filtrado_2 = pf.dropna(subset=['genre', 'explicit_content'])
            contenido_filtrado = pf
            opcion_contenido = st.selectbox('Selecciona el tipo de contenido:', 
                                ['Todos', 'Contenido Explícito', 'Sin Contenido Explícito'])
            if opcion_contenido == 'Contenido Explícito':
                data_filtrada = pf[pf['explicit_content'] == 'Yes']
            elif opcion_contenido == 'Sin Contenido Explícito':
                data_filtrada = pf[pf['explicit_content'] == 'No']
            else:
                data_filtrada = pf
            contenido_explicito = data_filtrada.groupby(['genre', 'explicit_content']).size().unstack(fill_value=0)

            fig, ax = plt.subplots(figsize=(12, 8))
            contenido_explicito.plot(kind='bar', stacked=True, ax=ax)
            ax.set_title('Proporción de Canciones con Contenido Explícito por Género')
            ax.set_xlabel('Género')
            ax.set_ylabel('Número de Canciones')
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
            plt.tight_layout()

            st.pyplot(fig)
            
        elif st.session_state.subpage == "subcategoria_b":
            st.header("Subcategoría B: Distribución de Idioma")
            st.write("Aquí se mostrarán los datos de la Subcategoría B.")
            contador_lenguaje = pf["language"].value_counts()
            fig, ax = plt.subplots(figsize=(10, 8))
            ax.pie(contador_lenguaje, labels=contador_lenguaje.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.tab20.colors)
            ax.set_title('Distribución de Canciones por Idioma')
            st.pyplot(fig)
        
        elif st.session_state.subpage == "subcategoria_c":
            st.header("Subcategoría C: Tendencia de Lanzamiento de Canciones")
            st.write("Aquí se mostrarán los datos de la Subcategoría C.")
            pf['release_date'] = pd.to_datetime(pf['release_date'], errors='coerce')
            pf_filtrado = pf.dropna(subset=['release_date'])
            pf_filtrado['year'] = pf_filtrado['release_date'].dt.year

            generos = pf_filtrado['genre'].dropna().unique()
            genero_seleccionado = st.selectbox('Selecciona un género musical:', options=generos)
            pf_filtrado_genero = pf_filtrado[pf_filtrado['genre'] == genero_seleccionado]

            min_year = int(pf_filtrado_genero['year'].min())
            max_year = int(pf_filtrado_genero['year'].max())
            rango_años = st.slider('Selecciona el rango de años:', min_year, max_year, (min_year, max_year))

            pf_filtrado_rango = pf_filtrado_genero[(pf_filtrado_genero['year'] >= rango_años[0]) & (pf_filtrado_genero['year'] <= rango_años[1])]

            releases_by_year = pf_filtrado_rango.groupby('year').size()
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(releases_by_year.index, releases_by_year.values, marker='o')
            ax.set_title(f"Tendencia de Lanzamientos de Canciones en {genero_seleccionado} ({rango_años[0]}-{rango_años[1]})")
            ax.set_xlabel("Año")
            ax.set_ylabel("Número de Canciones")
            ax.grid(True)
            st.pyplot(fig)

        elif st.session_state.subpage == "subcategoria_d":
            st.header("Subcategoría D: Duración Promedio de Canciones por Género") 
            genero_filtrado = pf[['genre', 'duration']]
            genero_filtrado = genero_filtrado.dropna(subset=['genre', 'duration'])
            
            st.title("Duración de Canciones por Género")
            genero_unico = genero_filtrado['genre'].unique()
            seleccionar_genero = st.selectbox("Selecciona un género de música:", options=['Todos'] + list(genero_unico))
            fig, ax = plt.subplots(figsize=(10, 6))
            if seleccionar_genero == 'Todos':
                # Calcular la duración promedio por género y mostrarlo
                duracion_por_genero = genero_filtrado.groupby('genre')['duration'].mean().sort_values()
                
                duracion_por_genero.plot(kind='barh', ax=ax, color='skyblue')
                ax.set_title('Duración Promedio de Canciones por Género')
                ax.set_xlabel('Duración Promedio (segundos)')
                ax.set_ylabel('Género')
            else:
                # Filtrar datos solo para el género seleccionado
                canciones_genero = genero_filtrado[genero_filtrado['genre'] == seleccionar_genero]
                
                # Graficar las duraciones individuales para el género seleccionado
                ax.barh(canciones_genero.index, canciones_genero['duration'], color='red')
                ax.set_title(f'Duración de Canciones en Género: {seleccionar_genero}')
                ax.set_xlabel('Duración (segundos)')
                ax.set_ylabel('Canción')
            plt.tight_layout()
            st.pyplot(fig)

        if st.button("Volver atrás"):
            cambiar_pagina("inicio")

elif st.session_state.page == "categoría_3":
    st.header("Contenido de Opción 3")
    st.write("Aquí se mostrarán los datos relacionados con la Opción 3.")
    
    if st.button("Volver atrás"):
        cambiar_pagina("inicio")
