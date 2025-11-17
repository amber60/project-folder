import os
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import tiktoken
from langchain_core.documents import Document
import pandas as pd
from langchain_chroma import Chroma
import chromadb
from uuid import uuid4
from more_itertools import chunked

def count_tokens(text):
    encoding = tiktoken.encoding_for_model('gpt-4o-mini')
    return len(encoding.encode(text))

def count_tokens_from_message_rough(messages):
    encoding = tiktoken.encoding_for_model('gpt-4o-mini')
    value = ' '.join([x.get('content') for x in messages])
    return len(encoding.encode(value))

load_dotenv(find_dotenv())

# Pass the API Key to the OpenAI Client
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

# embedding model that we will use for the session
embeddings_model = OpenAIEmbeddings(model='text-embedding-3-small')

# llm to be used in RAG pipeplines in this notebook
llm = ChatOpenAI(model='gpt-4o-mini', temperature=0, seed=42)

def load_documents(document_pdf):
    text_list = list(document_pdf["full_course_desc"])
    metadata_list = (
        document_pdf[[
            "course_title", 
            "course_provider",
            "course_url",
            "course_duration",
            "course_mode_of_training",
            "full_course_fee",
            "subsidised_course_fee",
            "course_number_of_hours",
            "course_language"
            ]]
        .to_dict(orient='records')
    )

    # Create a list of Document objects using a loop or list comprehension
    document_objects = []
    for i in range(len(text_list)):
        new_doc = Document(
            page_content=text_list[i],
            metadata=metadata_list[i]
        )
        document_objects.append(new_doc)
    return document_objects

def split_documents(list_of_documents_loaded):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1100, chunk_overlap=10, length_function=count_tokens)
    # Split the documents into smaller chunks
    splitted_documents = text_splitter.split_documents(list_of_documents_loaded)
    return splitted_documents

def load_into_database(splitted_documents, collection_name):
    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings_model,
        persist_directory="./vector_db",
    )
    vector_store.reset_collection()
    # print(vector_store._collection.count())
    uuids = [str(uuid4()) for _ in range(len(splitted_documents))]

    chunk_size = 500
    for _document_id_tuple_list in chunked(zip(splitted_documents, uuids), chunk_size):
        _document_list = [x for x,y in _document_id_tuple_list]
        _uuid_list = [y for x,y in _document_id_tuple_list]
        vector_store.add_documents(documents=_document_list, ids=_uuid_list)
    # print(vector_store._collection.count())

if __name__ == "__main__":
    data_dir = r"data"
    documents_pdf = pd.read_csv(rf"{data_dir}/skillsfuture_full.csv")
    documents_list = load_documents(documents_pdf)
    split_documents_list = split_documents(documents_list)
    load_into_database(split_documents_list, "skillsfuture")