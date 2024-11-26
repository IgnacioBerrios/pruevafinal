import streamlit as st
import base64
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

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
    </style>
    """,
    unsafe_allow_html=True
)

# Función para cargar datos con cache
@st.cache_data
def datos_cargados():
    ruta = 'spotify_songs_dataset.csv'
    data = pd.read_csv(ruta, sep=';')
    data['release_date'] = pd.to_datetime(data['release_date'], errors='coerce') 
    return data

# Dataset para nuevos módulos
data_modulo = datos_cargados()
data_modulo = data_modulo.dropna(subset=['release_date'])
data_modulo['year'] = data_modulo['release_date'].dt.year

# Configuración inicial de páginas
if "page" not in st.session_state:
    st.session_state.page = "inicio"

if "subpage" not in st.session_state:
    st.session_state.subpage = None

# Funciones para navegación
def cambiar_pagina(nueva_pagina):
    st.session_state.page = nueva_pagina
    if nueva_pagina != "categoría_2":
        st.session_state.subpage = None

def cambiar_subpagina(nueva_subpagina):
    st.session_state.subpage = nueva_subpagina

# Título de la aplicación
st.title("Aplicación Genérica")

# Página principal
if st.session_state.page == "inicio":
    st.header("Seleccione una opción")
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

# Categoría 1
elif st.session_state.page == "categoría_1":
    opciones = ["Todo"] + pf.columns.tolist()
    seleccion = st.selectbox("Selecciona una columna para ver", opciones)

    if seleccion == "Todo":
        st.dataframe(pf)
    else:
        st.write(f"Columna seleccionada: {seleccion}")
        st.write(pf[seleccion])
    if st.button("Volver atrás"):
        cambiar_pagina("inicio")

# Categoría 2 y subcategorías
elif st.session_state.page == "categoría_2":
    if st.session_state.subpage is None:
        st.header("Seleccione una subcategoría")
        if st.button("Gráfico de Contenido Explícito"):
            cambiar_subpagina("subcategoria_a")
        if st.button("Distribución de Idioma de Canciones"):
            cambiar_subpagina("subcategoria_b")
        if st.button("Tendencia de Lanzamiento de Canciones"):
            cambiar_subpagina("subcategoria_c")
        if st.button("Duración Promedio por Género"):
            cambiar_subpagina("subcategoria_d")
        if st.button("Reproducciones según Fecha de Publicación"):
            cambiar_subpagina("subcategoria_e")
        if st.button("Distribución de Idiomas por Género"):
            cambiar_subpagina("subcategoria_f")
        if st.button("Volver atrás"):
            cambiar_pagina("inicio")

    else:
        if st.session_state.subpage == "subcategoria_a":
            st.header("Subcategoría A: Contenido Explícito")
            contenido_explicito = pf.groupby(['genre', 'explicit_content']).size().unstack(fill_value=0)
            fig, ax = plt.subplots(figsize=(12, 8))
            contenido_explicito.plot(kind='bar', stacked=True, ax=ax)
            ax.set_title('Proporción de Canciones con Contenido Explícito por Género')
            st.pyplot(fig)

        elif st.session_state.subpage == "subcategoria_b":
            st.header("Subcategoría B: Distribución de Idioma")
            contador_lenguaje = pf["language"].value_counts()
            fig, ax = plt.subplots(figsize=(10, 8))
            ax.pie(contador_lenguaje, labels=contador_lenguaje.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.tab20.colors)
            st.pyplot(fig)

        elif st.session_state.subpage == "subcategoria_c":
            st.header("Subcategoría C: Tendencia de Lanzamiento")
            pf['release_date'] = pd.to_datetime(pf['release_date'], errors='coerce')
            pf_filtrado = pf.dropna(subset=['release_date'])
            pf_filtrado['year'] = pf_filtrado['release_date'].dt.year
            generos = pf_filtrado['genre'].unique()
            genero_seleccionado = st.selectbox('Selecciona un género:', options=generos)
            rango_años = st.slider('Selecciona el rango:', int(pf_filtrado['year'].min()), int(pf_filtrado['year'].max()))
            releases = pf_filtrado[pf_filtrado['year'].between(rango_años[0], rango_años[1])].groupby('year').size()
            fig, ax = plt.subplots()
            ax.plot(releases.index, releases.values)
            st.pyplot(fig)

        elif st.session_state.subpage == "subcategoria_e":
            st.header("Reproducciones según Fecha")
            selected_genre = st.selectbox("Selecciona un género:", options=data_modulo['genre'].dropna().unique())
            rango_años = st.slider("Selecciona el rango:", int(data_modulo['year'].min()), int(data_modulo['year'].max()))
            filtered_data = data_modulo[
                (data_modulo['genre'] == selected_genre) &
                (data_modulo['year'].between(rango_años[0], rango_años[1]))
            ]
            fig = px.scatter(
                filtered_data, x='release_date', y='stream', color='genre',
                title=f"Fecha vs Reproducciones ({selected_genre})"
            )
            st.plotly_chart(fig)

        elif st.session_state.subpage == "subcategoria_f":
            st.header("Distribución de Idiomas por Género")
            selected_genres = st.multiselect(
                "Selecciona géneros:", options=data_modulo['genre'].dropna().unique())
            filtered_data = data_modulo[data_modulo['genre'].isin(selected_genres)] if selected_genres else data_modulo
            if not filtered_data.empty:
                language_counts = filtered_data['language'].value_counts().reset_index()
                language_counts.columns = ['language', 'count']
                fig = px.pie(
                    language_counts, names='language', values='count', title="Distribución de Idiomas"
                )
                st.plotly_chart(fig)

        if st.button("Volver atrás"):
            cambiar_subpagina(None)

elif st.session_state.page == "categoría_3":
    st.header("Contenido de Opción 3")
    st.write("Aquí se mostrarán los datos relacionados con la Opción 3.")
    if st.button("Volver atrás"):
        cambiar_pagina("inicio")
