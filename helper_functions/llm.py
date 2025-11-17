import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import tiktoken
from langchain_chroma import Chroma
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
import streamlit as st

# Pass the API Key to the OpenAI Client
if load_dotenv(find_dotenv()):
   # for local development
   OPENAI_KEY = os.getenv('OPENAI_API_KEY')
else:
   OPENAI_KEY = st.secrets['OPENAI_API_KEY']

client = OpenAI(OPENAI_KEY)
embeddings_model = OpenAIEmbeddings(model='text-embedding-3-small')
llm = ChatOpenAI(model='gpt-4o-mini', temperature=0, seed=42)

def get_embedding(input, model='text-embedding-3-small'):
    response = client.embeddings.create(
        input=input,
        model=model
    )
    return [x.embedding for x in response.data]

# This is the "Updated" helper function for calling LLM
def get_completion(prompt, model="gpt-4o-mini", temperature=0, top_p=1.0, max_tokens=1024, n=1, json_output=False):
    if json_output == True:
      output_json_structure = {"type": "json_object"}
    else:
      output_json_structure = None

    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create( #originally was openai.chat.completions
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        n=1,
        response_format=output_json_structure,
    )
    return response.choices[0].message.content

# Note that this function directly take in "messages" as the parameter.
def get_completion_from_messages(messages, model="gpt-4o-mini", temperature=0, top_p=1.0, max_tokens=1024, n=1):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        n=1
    )
    return response.choices[0].message.content

# This function is for calculating the tokens given the "message"
# ⚠️ This is simplified implementation that is good enough for a rough estimation

def count_tokens(text):
    encoding = tiktoken.encoding_for_model('gpt-4o-mini')
    return len(encoding.encode(text))


def count_tokens_from_message(messages):
    encoding = tiktoken.encoding_for_model('gpt-4o-mini')
    value = ' '.join([x.get('content') for x in messages])
    return len(encoding.encode(value))

def naive_rag(user_query):
    vector_store = Chroma(
        collection_name="skillsfuture",
        embedding_function=embeddings_model,
        persist_directory="./vector_db",
    )
    rag_chain = RetrievalQA.from_llm(
       retriever=vector_store.as_retriever(), llm=llm
    )
    response = rag_chain.invoke(user_query)
    return response

def qa_chain_prompt(user_query):
    vector_store = Chroma(
        collection_name="skillsfuture",
        embedding_function=embeddings_model,
        persist_directory="./vector_db",
    )
    # Build prompt
    template = """
    Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Return all relevant responses in point form.
    {context}
    Question: {question}
    Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

    # Run chain
    qa_chain = RetrievalQA.from_chain_type(
        ChatOpenAI(model='gpt-4o-mini'),
        retriever=vector_store.as_retriever(
            search_type='mmr',),
        return_source_documents=True, # Make inspection of document possible
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    response = qa_chain.invoke(user_query)
    return response["result"]

if __name__ == "__main__":
    query = "Are there courses that are relevant to drawing?"
    # print(naive_rag(query)["result"])
    response = qa_chain_prompt(query)
    print(response)

