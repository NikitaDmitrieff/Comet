import os
from functools import reduce

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langsmith import traceable

import config
from comet_helper.rag_pipeline import get_context


@traceable()
def load_model(model_type=None):

    if not model_type:
        model_type = "gpt-4o-mini"

    model = ChatOpenAI(model=model_type)

    return model


@traceable()
def load_embedding(embedding_type=None):

    if not embedding_type:
        embedding_type = "gpt-4o-mini"

    model = OpenAIEmbeddings()

    return model


@traceable()
def basic_inquiry(
    system_prompt: str = "Translate the following from English into Italian",
    user_prompt: str = "hi!",
    model_type: str = None,
    model=None,
):

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


def retrieve_parser():
    return StrOutputParser()


def form_chain_from_links(*args):
    return reduce(lambda x, y: x | y, args)


def create_full_chain(
    system_template: str = "You are a guidance counselor, be informative and encouraging.",
    user_template: str = "{text}",
    pdf_directory: str = config.COMET_HELPER_DATA_PATH,
    model_type: str = None,
):
    context_link = get_context(
        pdf_directory=pdf_directory, embedding_model=load_embedding()
    )
    prompt_template = prompt_template_generator(
        system_template=system_template, user_template=user_template
    )
    model = load_model(model_type=model_type)
    parser = retrieve_parser()
    return context_link | prompt_template | model | parser


def load_pdf_documents(
    pdf_directory=config.COMET_HELPER_DATA_PATH,
):

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
