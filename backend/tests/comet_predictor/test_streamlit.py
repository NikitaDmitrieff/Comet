from unittest.mock import patch

from backend.app import config
from backend.app.comet_predictor.generator import generate_possible_wishes
from frontend.streamlit.pages.wish_list_predictor_page import streamlit_user_input


# Test function to simulate Streamlit user input
def test_streamlit_user_input():
    with patch("streamlit.selectbox") as mock_selectbox, patch(
        "streamlit.multiselect"
    ) as mock_multiselect, patch("streamlit.slider") as mock_slider, patch(
        "streamlit.radio"
    ) as mock_radio, patch(
        "streamlit.button"
    ) as mock_button:

        # Define the simulated responses for each input component
        mock_selectbox.side_effect = ["DROIT", "SC. POLITIQUES RI"]
        mock_multiselect.return_value = PARSED_PROFILE["subjects 1"]
        mock_slider.side_effect = [
            PARSED_PROFILE["absolute value overall average"],
            PARSED_PROFILE["relative overall average"],
            PARSED_PROFILE["french grade"],
        ]
        mock_radio.return_value = "No"
        mock_button.return_value = True  # Simulate button click

        # Call the function to get the responses dictionary
        responses = streamlit_user_input()

        # Assertion to ensure responses match expected output
        assert (
            responses == PARSED_PROFILE
        ), f"Test failed! Expected {PARSED_PROFILE}, but got {responses}"

        possible_wishes, impossible_wishes = generate_possible_wishes(
            responses, requirement_file_path=config.WISH_LIST_DATA_PATH
        )

        for wish in POSSIBLE_WISHES:
            assert (
                wish in possible_wishes
            ), "Error with incorrect parsing of possible wishes."

        for wish in IMPOSSIBLE_WISHES:
            assert (
                wish in impossible_wishes
            ), "Error with incorrect parsing of impossible wishes. "
