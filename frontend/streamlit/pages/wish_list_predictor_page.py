import pandas as pd
import streamlit as st

from backend.app import config

config.ANCHOR

from backend.app.comet_predictor.generator import generate_possible_wishes


st.markdown("# Wish list predictor")
st.sidebar.markdown("# Wish list predictor")


def streamlit_user_input():
    # Dictionary to store the user responses
    responses = {
        "section 1": "error - no response",
        "section 2": "error - no response",
        "subjects 1": "error - no response",
        "subjects 2": "[]",
        "subjects 3": "[]",
        "international": "error - no response",
        "relative overall average": "error - no response",
        "absolute value overall average": "error - no response",
        "french grade": "error - no response",
    }

    # Filière 1 and Filière 2
    filiere_1_options = [
        "DROIT",
        "SC. POLITIQUES RI",
        "HISTOIRE",
        "HUMANITES",
        "ECONOMIE",
        "ECONOMIE GESTION",
        "MATHEMATIQUES",
        "COMMERCE",
        "None",
    ]

    filiere_2_options = [
        "SC. POLITIQUES RI",
        "SCIENCES SOCIALES",
        "PHILOSOPHIE",
        "HISTOIRE",
        "LANGUES",
        "None",  # In place of 0
        "HUMANITES",
        "ECONOMIE",
        "GESTION",
        "MATHEMATIQUES",
        "DROIT",
        "INFO. - DATA SCIENCE - IA",
        "MNGT GENERAL",
        "LUXE MODE",
        "DIGITAL E-BUSINESS",
        "INGENIEUR",
    ]

    responses["section 1"] = st.selectbox("Filière 1", filiere_1_options)
    responses["section 2"] = st.selectbox("Filière 2", filiere_2_options)

    # Question about International Option
    responses["international"] = st.radio(
        "Veux-tu suivre un cursus international?", ("Oui", "non")
    )
    responses["international"] = [1 if responses["international"] == "Yes" else 0][0]

    # Subject options to be selected with multi-select
    subject_options = [
        "Maths",
        "PC",
        "SVT",
        "NSI",
        "HLP",
        "LLCE",
        "AMC",
        "HGGSP",
        "SES",
        "ARTS PLASTIQUES",
        "DROIT ET GRANDS ENJEUX",
        "MATHS COMPLEMENTAIRES",
        "MATHS EXPERTES",
        "STMG",
    ]

    # Multi-select box to allow users to select up to 3 subjects
    responses["subjects 1"] = st.multiselect(
        "Indique tes options:",
        options=subject_options,
        default=None,
        max_selections=3,
    )

    st.subheader("Tes notes:")
    responses["absolute value overall average"] = st.slider(
        "Moyenne générale en valeur absolue", 1, 5, value=3
    )
    responses["relative overall average"] = st.slider(
        "Moyenne générale par rapport à la classe", 1, 5, value=3
    )
    responses["french grade"] = st.slider("Notes de Français", 1, 5, value=3)

    # Select box for math level
    responses["math level"] = st.selectbox(
        "Math Level",
        options=[0, 1, 2, 3],
        format_func=lambda x: {
            0: "0 (Pas de Maths)",
            1: "1 (Option: Maths complémentaires)",
            2: "2 (Spé Maths)",
            3: "3 (Spé Maths et option maths expertes)",
        }.get(x, "Unknown"),
    )

    # Submit button
    if st.button("Submit"):
        print(len(responses))
        print(type(responses))
        print(responses)
        return responses


profile_dict = streamlit_user_input()


if profile_dict:

    possible_wishes, impossible_wishes = generate_possible_wishes(
        profile_dict, requirement_file_path=config.WISH_LIST_DATA_PATH
    )

    f"Number of possible wishes: {len(possible_wishes)}"
    f"Number of impossible wishes: {len(impossible_wishes)}"
    st.dataframe(pd.DataFrame(possible_wishes))
