import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Matrice de Compétences", layout="wide")

st.title("🔍 Outil de recherche de compétences")

# Upload ou utilisation d'un fichier par défaut
uploaded_file = st.file_uploader("Téléverser le fichier Excel", type=["xlsx"])
default_file = "Matrice_Competences_MODELE.xlsx"

# Charger les données
@st.cache_data
def load_data(file):
    return pd.read_excel(file)

if uploaded_file:
    df = load_data(uploaded_file)
else:
    df = load_data(default_file)
    st.info("Aucun fichier téléversé. Utilisation du fichier exemple par défaut.")

# Afficher les données brutes si demandé
with st.expander("📊 Voir les données brutes"):
    st.dataframe(df)

# Sélection de la compétence
competences = list(df.columns[1:])
competence_choisie = st.selectbox("Choisir une compétence à rechercher", competences)

# Choix du niveau minimum
niveau_min = st.slider("Choisir le niveau minimum requis", min_value=0, max_value=4, value=3)

# Filtrage
filtres = df[df[competence_choisie] >= niveau_min]

st.markdown(f"### ✅ Résultats ({len(filtres)} consultant(s) trouvé(s))")
st.dataframe(filtres[["Consultant", competence_choisie]])

# Export des résultats
if not filtres.empty:
    output = BytesIO()
    filtres.to_excel(output, index=False, engine="openpyxl")
    output.seek(0)

    st.download_button(
        label="📥 Télécharger les résultats",
        data=output,
        file_name="resultats_filtrés.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
