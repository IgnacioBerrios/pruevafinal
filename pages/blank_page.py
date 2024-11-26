import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import base64

# Función para cargar y verificar el dataset
@st.cache_data
def cargar_datos():
    ruta = "spotify_songs_dataset.csv"
    try:
        data = pd.read_csv(ruta, delimiter=';')
        return data
    except FileNotFoundError:
        st.error("El archivo 'spotify_songs_dataset.csv' no fue encontrado.")
        return None

# Cargar el dataset
pf = cargar_datos()

# Verificar y ajustar columnas
if pf is not None:
    st.write("Columnas disponibles en el dataset:", pf.columns.tolist())

    if 'release_date' not in pf.columns:
        posibles_nombres = ['ReleaseDate', 'releaseDate', 'release_date']
        for col in posibles_nombres:
            if col in pf.columns:
                pf.rename(columns={col: 'release_date'}, inplace=True)
                break

    if 'release_date' not in pf.columns:
        st.error("La columna 'release_date' no se encuentra en el dataset.")
    else:
        pf['release_date'] = pd.to_datetime(pf['release_date'], errors='coerce')
        pf = pf.dropna(subset=['release_date'])  # Eliminar filas sin fecha válida
        pf['year'] = pf['release_date'].dt.year  # Extraer el año

# Codificar la imagen de fondo
image_path = "pages/Necesarios/fondo_morado.png"
with open(image_path, "rb") as img_file:
    base64_image = base64.b64encode(img_file.read()).decode()

# Aplicar estilo de fondo
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
    </style>
    """,
    unsafe_allow_html=True
)

# Navegación entre páginas
if "page" not in st.session_state:
    st.session_state.page = "inicio"

def cambiar_pagina(nueva_pagina):
    st.session_state.page = nueva_pagina

# Página principal
if st.session_state.page == "inicio":
    st.title("Exploración de Canciones de Spotify")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Visualizaciones Generales"):
            cambiar_pagina("visualizaciones")
    with col2:
        if st.button("Análisis por Género"):
            cambiar_pagina("genero")

# Visualizaciones generales
elif st.session_state.page == "visualizaciones":
    st.title("Visualizaciones Generales")
    st.subheader("Distribución de Idiomas")
    if 'language' not in pf.columns:
        st.error("La columna 'language' no se encuentra en el dataset.")
    else:
        selected_genres = st.multiselect(
            "Selecciona los géneros que deseas analizar:",
            options=pf['genre'].dropna().unique()
        )
        filtered_data = pf[pf['genre'].isin(selected_genres)] if selected_genres else pf
        if filtered_data.empty:
            st.warning("No hay datos para los géneros seleccionados.")
        else:
            language_counts = filtered_data['language'].dropna().value_counts().reset_index()
            language_counts.columns = ['language', 'count']
            fig = px.pie(
                language_counts,
                names='language',
                values='count',
                title='Distribución de Idiomas',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig)
    if st.button("Volver al inicio"):
        cambiar_pagina("inicio")

# Análisis por género
elif st.session_state.page == "genero":
    st.title("Análisis por Género")
    if 'genre' not in pf.columns or 'stream' not in pf.columns:
        st.error("Las columnas necesarias no están en el dataset.")
    else:
        genres = pf['genre'].dropna().unique()
        selected_genre = st.selectbox("Selecciona un género:", options=genres)

        filtered_data = pf[pf['genre'] == selected_genre]
        min_year = int(filtered_data['year'].min())
        max_year = int(filtered_data['year'].max())
        rango_años = st.slider(
            'Selecciona el rango de años:', min_year, max_year, (min_year, max_year)
        )

        filtered_data = filtered_data[
            (filtered_data['year'] >= rango_años[0]) & (filtered_data['year'] <= rango_años[1])
        ]

        color_map = {
            "R&B": "red", "Electronic": "yellow", "Pop": "blue", "Folk": "green",
            "Hip-Hop": "purple", "Jazz": "orange", "Classical": "brown",
            "Country": "skyblue", "Reggae": "white",
        }

        fig = px.scatter(
            filtered_data,
            x='release_date', y='stream', color='genre',
            color_discrete_map=color_map,
            title=f"Fecha de Publicación vs Reproducciones ({selected_genre}, {rango_años[0]}-{rango_años[1]})",
            labels={"release_date": "Fecha de Publicación", "stream": "Reproducciones", "genre": "Género"},
            template="plotly_white",
            opacity=0.7
        )

        fig.update_layout(
            xaxis=dict(title="Fecha de Publicación"),
            yaxis=dict(title="Reproducciones"),
            title_font_size=16,
        )
        st.plotly_chart(fig)

    if st.button("Volver al inicio"):
        cambiar_pagina("inicio")
