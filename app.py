from altair import Detail
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap

st.title("Bonjour, Streamlit !")
st.write("Ceci est une application Streamlit maximale.")


# Chargement du fichier CSV
data = pd.read_csv('details.csv')
st.write("Contenu du fichier details.csv :")
st.dataframe(data)

# Customize the background color to blue
st.markdown(
    """
    <style>
    .stApp {
        background-color: #add8e6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Création de carte
m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)
# Ajout des marqueurs pour chaque endroit
for index, row in data.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"Nom: {row['Nom']}<br>Adresse: {row['Adresse']}<br>Telephone: {row['Telephone']}",
        tooltip=row['Nom']
    ).add_to(m)
# Affichage de la carte
st.write("Carte des emplacements :")
st_folium(m, width=1000, height=1000)

# Carte de chaleur
heat_data = [[row['Latitude'], row['Longitude']] for index, row in data.iterrows()]
HeatMap(heat_data).add_to(m)
st.write("Carte de chaleur des emplacements :")
st_folium(m, width=1000, height=1000)

# Ajout d'une fonction de recherche
st.write("Recherche par nom :")
search_query = st.text_input("Entrez un nom à rechercher :")

if search_query:
    filtered_data = data[data['Nom'].str.contains(search_query, case=False, na=False)]
    if not filtered_data.empty:
        st.write("Résultats:")
        st.dataframe(filtered_data)
        
        # Mettre à jour la carte avec les résultats de la recherche
        search_map = folium.Map(location=[48.8566, 2.3522], zoom_start=12)
        for index, row in filtered_data.iterrows():
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=f"Nom: {row['Nom']}<br>Adresse: {row['Adresse']}<br>Telephone: {row['Telephone']}",
                tooltip=row['Nom']
            ).add_to(search_map)
        st.write("Carte des résultats de la recherche :")
        st_folium(search_map, width=1000, height=1000)
    else:
        st.write("Rien")

# Ajout d'un bouton pour télécharger le fichier CSV.
csv_file = 'details.csv'
with open(csv_file, 'rb') as f:
    st.download_button(
        label="Télécharger le fichier CSV",
        data=f,
        file_name=csv_file,
        mime='text/csv'
    )
# Ajout d'un bouton pour télécharger la carte en html.
html_file = 'map.html'
m.save(html_file)
with open(html_file, 'rb') as f:
    st.download_button(
        label="Télécharger la carte",
        data=f,
        file_name=html_file,
        mime='text/html'
    )
