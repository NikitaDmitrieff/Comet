import os
import sys
from enum import Enum
from pathlib import Path
from typing import Any, Dict

OPENAI_API_VERSION = "2024-05-01-preview"
OPENAI_API_TYPE = "azure"

AZURE_OPENAI_ENDPOINT = "https://chatbot-helper.openai.azure.com/"
EMBEDDINGS_MODEL = "text-embedding-ada-002"

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

WISH_LIST_DATA_PATH = APP_ROOT / "comet_predictor/data_wish_list/parsed_wish_list.csv"
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


class AzureOpenAiRegions(str, Enum):
    FRC = "francecentral"
    EUS = "eastus"
    SEC = "swedencentral"
    WUS = "westus"


class DeploymentName(str, Enum):
    GPT_35_TURBO = "gpt-35-turbo"


OPENAI_ENDPOINT_BY_MODEL = {
    DeploymentName.GPT_35_TURBO: {
        AzureOpenAiRegions.EUS: "https://nikit-m6hyvogj-eastus2.cognitiveservices.azure.com/openai/deployments/gpt-35-turbo/chat/completions?api-version=2024-08-01-preview",
    }
}


DEFAULT_REQUEST_TIMEOUT_S_BY_DEPLOYMENT = {
    DeploymentName.GPT_35_TURBO: 120,
}


def _get_api_kwargs_by_model_and_region(
    model: DeploymentName, region: AzureOpenAiRegions
) -> dict[str, str]:
    return {
        "openai_api_version": OPENAI_API_VERSION,
        "openai_api_key": credentials.AZURE_OPENAI_API_KEY,
        "azure_endpoint": OPENAI_ENDPOINT_BY_MODEL[model][region],
    }


def _get_embeddings_api_kwargs(
    model: DeploymentName, region: AzureOpenAiRegions
) -> Dict[str, Any]:
    return {
        **_get_api_kwargs_by_model_and_region(model=model, region=region),
        "model": EMBEDDINGS_MODEL,
        "openai_api_type": OPENAI_API_TYPE,
    }


def _get_chat_kwargs(
    model: DeploymentName, region: AzureOpenAiRegions
) -> list[dict[str, Any]]:

    chat_kwargs = {
        **_get_api_kwargs_by_model_and_region(model=model, region=region),
        "temperature": 0,
        "max_tokens": None,
        "max_retries": 2,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "model": model.value,
        "deployment_name": model.value,
        "request_timeout": DEFAULT_REQUEST_TIMEOUT_S_BY_DEPLOYMENT[model],
    }
    return chat_kwargs


DEFAULT_EMBEDDING_KWARGS = _get_embeddings_api_kwargs(
    model=DeploymentName.GPT_35_TURBO, region=AzureOpenAiRegions.EUS
)
DEFAULT_CHATGPT_KWARGS = _get_chat_kwargs(
    model=DeploymentName.GPT_35_TURBO, region=AzureOpenAiRegions.EUS
)
GPT35_TURBO_KWARGS = _get_chat_kwargs(
    model=DeploymentName.GPT_35_TURBO, region=AzureOpenAiRegions.EUS
)
