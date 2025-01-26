import pandas as pd

from backend.app import config
from backend.app.comet_predictor.generator import (
    generate_possible_wishes,
    create_wish_list_data_files,
)

create_wish_list_data_files()


def test_generate_possible_wishes():
    """
    Tests that from a standard profile, the correct wishes are fetched and discarded.
        - possible_wishes bear "pass" in the wish name
        - impossible_wishes bear "fail" in the wish name
    """

    profile_df = pd.read_csv(config.TEST_PROFILE_WISH_LIST_DATA_PATH)
    profile = {
        key: value[0]
        for key, value in profile_df.to_dict().items()
        if f"{value[0]}" not in "profile"
    }

    possible_wishes, impossible_wishes = generate_possible_wishes(
        profile, requirement_file_path=config.TEST_WISH_LIST_DATA_PATH
    )

    for wish in possible_wishes:
        assert (
            "pass" in wish["wish name"]
        ), "Error with incorrect parsing of possible wishes."

    for wish in impossible_wishes:
        assert (
            "fail" in wish["wish name"]
        ), "Error with incorrect parsing of impossible wishes."


def test_test_data_wish_list():
    test_df = pd.read_csv(config.TEST_WISH_LIST_DATA_PATH)
    prod_df = pd.read_csv(config.WISH_LIST_DATA_PATH)

    # Check for column equality (ignoring order)
    assert set(test_df.columns) == set(
        prod_df.columns
    ), "Error likely due to outdated test data or column mismatch."

    # Optionally, check column order if required
    assert list(test_df.columns) == list(
        prod_df.columns
    ), "Column order mismatch in test data."
