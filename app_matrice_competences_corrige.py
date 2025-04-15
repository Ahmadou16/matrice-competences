import pandas as pd
import streamlit as st

st.title("🧠 Matrice de Compétences - Équipe TMA")

uploaded_file = st.file_uploader("📤 Importer le fichier Excel de compétences", type=["xlsx"])

if uploaded_file:
    try:
        # Lecture à partir de la 4e ligne (ligne 4 Excel = index 3)
        df = pd.read_excel(uploaded_file, header=3)

        # Supposons que la première colonne est "Consultant" ou équivalent
        first_col = df.columns[0]
        competence_columns = df.columns[1:]

        # Cast toutes les colonnes de compétences en numériques (au cas où elles seraient str)
        df[competence_columns] = df[competence_columns].apply(pd.to_numeric, errors="coerce")

        st.success("Fichier chargé avec succès !")
        if st.checkbox("👁️ Aperçu du fichier Excel"):
            st.dataframe(df.head())

        selected_competences = st.multiselect("🔍 Choisir les compétences à filtrer :", competence_columns)

        if selected_competences:
            selected_level = st.slider("📊 Niveau minimum requis :", 0, 4, 2)

            filtres = df[[first_col] + list(selected_competences)]
            filtres = filtres[filtres[selected_competences].ge(selected_level).all(axis=1)]

            st.subheader("📋 Résultats du filtre")
            st.write(f"{len(filtres)} consultant(s) trouvé(s) avec un niveau ≥ {selected_level}.")
            st.dataframe(filtres)

            output_file = "resultats_filtrés.xlsx"
            filtres.to_excel(output_file, index=False)
            with open(output_file, "rb") as f:
                st.download_button("💾 Télécharger les résultats", f, file_name=output_file)

        else:
            st.info("Veuillez sélectionner au moins une compétence.")

    except Exception as e:
        st.error(f"Erreur : {e}")
else:
    st.warning("Veuillez importer un fichier Excel.")
