import os

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter


def get_context(
    pdf_directory=os.getenv("COMET_HELPER_DATA_PATH"),
    embedding_model=None,
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

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(documents=splits, embedding=embedding_model)

    # Retrieve and generate using the relevant snippets of the blog.
    retriever = vectorstore.as_retriever()

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_link = {
        "context": retriever | format_docs,
        "question": RunnablePassthrough(),
    }

    return rag_link
