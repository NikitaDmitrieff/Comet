from typing import List, Tuple

import pandas as pd

import config


def create_wish_list_data_files():
    """
    1. The main csv file is loaded inside config.RAW_WISH_LIST_DATA_PATH
        (as of today: "comet_predictor/data_wish_list/raw_parsed_wish_list.csv")

    2. This function parses this raw csv file from the google sheet into:
        - test_profile_data_wish_list.csv: test profiles for checking rules are correctly enforced
        - parsed_wish_list.csv: production csv gathering all schools and their respective requirements
        - test_data_wish_list.csv: test csv gathering all test schools and their respective requirements
    """

    raw_schools_and_profiles_df = pd.read_csv(config.RAW_WISH_LIST_DATA_PATH)
    raw_schools_and_profiles_df = raw_schools_and_profiles_df.loc[:, ~raw_schools_and_profiles_df.columns.str.contains("^Unnamed")]

    # Fetch the top-rows which are in fact test profiles to make sure rules are enforced
    profiles_df = raw_schools_and_profiles_df[raw_schools_and_profiles_df["place"].str.contains("profile", case=False, na=False)]
    profiles_df.to_csv(config.TEST_PROFILE_WISH_LIST_DATA_PATH)

    # Fetch all other rows (that are not profiles, cf. "~")
    raw_schools_df = raw_schools_and_profiles_df[~raw_schools_and_profiles_df["place"].str.contains("profile", case=False, na=False)]

    # Fetch all non-test school rows
    prod_schools_df = raw_schools_df[~raw_schools_df["place"].str.contains("test", case=False, na=False)]
    prod_schools_df.to_csv(config.WISH_LIST_DATA_PATH)

    # Fetch all test school rows
    test_schools_df = raw_schools_df[raw_schools_df["place"].str.contains("test", case=False, na=False)]
    test_schools_df.to_csv(config.TEST_WISH_LIST_DATA_PATH)

    return


create_wish_list_data_files()


def _hard_requirement_parser(
    requirements_df: pd.DataFrame, profile: dict
) -> List[dict]:
    possible_wishes = []
    impossible_wishes = []

    for index, row in requirements_df.iterrows():

        can_apply = True
        for requirement_name, requirement_value in row.to_dict().items():

            # Profile must exceed grade requirements
            if requirement_name in [
                "relative overall average",
                "absolute value overall average",
                "french grade",
                "math level",
            ]:
                if profile[requirement_name] < requirement_value:
                    can_apply = False
                    break

            # Profile must match subjects 1 requirements
            elif requirement_name in ["subjects 1"]:

                if profile["subjects 1"] not in row["subjects 1"]:
                    can_apply = False
                    break

            # Profile must match one of the two sections
            elif requirement_name in ["section 1"]:
                section_match = any(
                    section in [profile["section 1"], profile["section 2"]]
                    for section in [row["section 1"], row["section 2"]]
                )

                if not section_match:
                    can_apply = False
                    break

        if can_apply:
            possible_wishes.append(row.to_dict())
        else:
            impossible_wishes.append(row.to_dict())

    return possible_wishes, impossible_wishes


def generate_possible_wishes(
    profile: dict, requirement_file_path: str = "data_wish_list/parsed_wish_list.csv"
) -> Tuple[List[dict], List[dict]]:
    """
    Main function for retrieving the possible wishes for a certain profile:
        Calls hard_requirement parser

    Args:
        profile: dict with the user's grades and sections
        requirement_file_path: str leading to the requirement csv file
    returns:
        possible_wishes: List
        impossible_wishes: List
    """

    requirements_df = pd.read_csv(requirement_file_path)

    # Parse though hard grade requirements
    possible_wishes, impossible_wishes = _hard_requirement_parser(
        requirements_df=requirements_df, profile=profile
    )

    return possible_wishes, impossible_wishes
