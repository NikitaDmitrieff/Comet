import os
import sys
from pathlib import Path

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, parent_dir)

# Now you can import the file
import credentials

APP_ROOT = Path(__file__).resolve().parent
BACKEND_ROOT = Path(__file__).resolve().parent.parent

sys.path.append(APP_ROOT)
sys.path.append(BACKEND_ROOT)

RAW_WISH_LIST_DATA_PATH = (
    APP_ROOT / "comet_predictor/data_wish_list/raw_parsed_wish_list.csv"
)

WISH_LIST_DATA_PATH = (
    APP_ROOT / "comet_predictor/data_wish_list/parsed_wish_list.csv"
)
TEST_WISH_LIST_DATA_PATH = (
    BACKEND_ROOT / "tests/comet_predictor/test_data/test_data_wish_list.csv"
)

TEST_PROFILE_WISH_LIST_DATA_PATH = (
    BACKEND_ROOT / "tests/comet_predictor/test_data/test_profile_data_wish_list.csv"
)

COMET_HELPER_DATA_PATH = APP_ROOT / "comet_helper/data"

os.environ["OPENAI_API_KEY"] = credentials.OPENAI_API_KEY
os.environ["COMET_HELPER_DATA_PATH"] = str(COMET_HELPER_DATA_PATH)
os.environ["TEST_WISH_LIST_DATA_PATH"] = str(TEST_WISH_LIST_DATA_PATH)
os.environ["WISH_LIST_DATA_PATH"] = str(WISH_LIST_DATA_PATH)
os.environ["RAW_WISH_LIST_DATA_PATH"] = str(RAW_WISH_LIST_DATA_PATH)


ANCHOR = True
