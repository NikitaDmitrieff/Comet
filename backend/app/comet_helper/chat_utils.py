import asyncio
import os
from typing import Any, Dict, List, Optional, Tuple, Type, Union

import config
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_openai import AzureChatOpenAI, ChatOpenAI, OpenAIEmbeddings
from langsmith import traceable


def load_embedding(embedding_type=None):

    if not embedding_type:
        embedding_type = "gpt-4o-mini"

    model = OpenAIEmbeddings(model=embedding_type)

    return model


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


def create_chat_instance(
    chat_kwargs: List[Dict[str, Any]],
) -> AzureChatOpenAI:
    chat = AzureChatOpenAI(**chat_kwargs)
    return chat


def _convert_prompts_to_langchain_messages(
    system_prompt: Optional[str] = None,
    user_prompt: Optional[str] = None,
    images: Optional[List[Dict[str, str]]] = None,
) -> List[BaseMessage]:
    """Converts system and user prompts, along with optional image URLs, to a list of langchain messages."""
    if not system_prompt and not user_prompt and not images:
        raise ValueError(
            "At least one of system_prompt, user_prompt, or images must be provided."
        )

    messages = []
    if system_prompt is not None:
        messages.append(SystemMessage(content=system_prompt))

    user_content = []
    if user_prompt is not None:
        user_content.append({"type": "text", "text": user_prompt})
    if images is not None:
        for i, image_dict in enumerate(images):
            image_prefix = image_dict.get("image_prefix")
            image_url = image_dict.get("image_url")

            if image_url is not None:
                if image_prefix is not None:
                    user_content.append({"type": "text", "text": image_prefix})

                user_content.append(
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url, "detail": "low"},
                    }
                )

    if len(user_content) > 0:
        messages.append(HumanMessage(content=user_content))

    return messages


class ChatManager:
    def __init__(
        self,
        chat_kwargs: Optional[Dict[str, Union[str, int]]] = None,
    ):
        """
        Interface to call Azure OpenAI. Three main methods:
        * ainvoke_prompt: Invokes chat using a PromptTemplate.
        * ainvoke_message: Invokes chat using individual message prompts (user_prompt, system_prompt).

        :param chat_kwargs: A list of dictionaries containing the kwargs for the main chat instance and any fallbacks.
        """
        self.chat_kwargs = chat_kwargs or config.DEFAULT_CHATGPT_KWARGS
        self.chat_instance = create_chat_instance(self.chat_kwargs)

    async def ainvoke_prompt(
        self, prompt: PromptTemplate, inputs: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Invokes chat using prompt inputs.
            prompt: PromptTemplate
        """
        if inputs is None:
            inputs = {}
        chain = prompt | self.chat_instance
        response = await chain.ainvoke(inputs)
        return response.content

    async def ainvoke_message(
        self,
        user_prompt: Optional[str] = None,
        system_prompt: Optional[str] = None,
        images: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """
        Invokes chat using individual message prompts.
            user_prompt: str
            system_prompt: str
            images: [str, str]
        """
        message = _convert_prompts_to_langchain_messages(
            system_prompt, user_prompt, images
        )
        response = await self.chat_instance.ainvoke(message)
        return response.content


if __name__ == "__main__":
    chatbot = ChatManager(config.kwargs)
    response = asyncio.run(chatbot.ainvoke_message(user_prompt="say hi"))
    print(response)
