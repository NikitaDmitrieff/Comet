import os
from typing import Optional

from langchain.chat_models import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langsmith import traceable

import config


@traceable()
def load_model(model_type: Optional[str] = None) -> ChatOpenAI:

    if not model_type:
        model_type = "gpt-4o-mini"

    model = ChatOpenAI(model=model_type)
    return model


@traceable()
def load_embedding(embedding_type=None):

    if not embedding_type:
        embedding_type = "gpt-4o-mini"

    model = OpenAIEmbeddings(model=embedding_type)

    return model


@traceable()
def basic_inquiry(
    system_prompt: str = "Translate the following from English into Italian",
    user_prompt: str = "hi!",
    model_type: str = None,
    model: ChatOpenAI =None,
):
    # TODO: Remove and switch to ChatManager organization. Waiting on Azure clearance.

    if not model:
        model = load_model(model_type=model_type)

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]

    result = model.invoke(messages).content

    return result


def prompt_template_generator(
    system_template="Please translate the following text into {language}.",
    user_template="{text}",
):

    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", user_template)]
    )

    return prompt_template


def load_pdf_documents(
    pdf_directory=config.COMET_HELPER_DATA_PATH,
):
    # TODO: Get a better database management thing

    # Load all PDF files from the directory
    pdf_loaders = []
    for filename in os.listdir(pdf_directory):
        if filename.endswith(".pdf"):
            pdf_loaders.append(PyPDFLoader(os.path.join(pdf_directory, filename)))

    # Load and split documents
    docs = []
    for loader in pdf_loaders:
        docs.extend(loader.load())

    return docs
