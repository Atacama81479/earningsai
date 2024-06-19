import os
import json
import pygsheets
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.runnables import RunnablePassthrough


def Createsummary(settings, query_set):

    load_dotenv()
    gsheetnr = int(settings.gsheetno)
    gsheetname = settings.gsheetname
    indexname = settings.indexname
    companyname = settings.companyname
    rag_promt = settings.rag_prompt
    embeddingmodell = settings.embedding
    llmmodell = settings.llm


    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)


    print("Retrieving...")

    embeddings = OpenAIEmbeddings(model= embeddingmodell)
    llm = ChatOpenAI(model= llmmodell)

    print(settings)
    
    
    print(gsheetname) 

    print("Testing LLM...")
    query = "how was q1 of alfen?"
    chain = PromptTemplate.from_template(template=query) | llm
    result = chain.invoke(input = {})


    print("setting up Vectorstore...")
    vectorstore = PineconeVectorStore(index_name= indexname, embedding=embeddings)

    print("connect with google...")
    gc = pygsheets.authorize(service_file='app/Gcredentials.json')
    sheet= gc.open(gsheetname)


    wks = sheet[gsheetnr]
    

    print("creating rag_chain...")
                
    template =  """
    """+ rag_promt+"""

    {context}

    Question: {question}

    Helpful Answer:
    """
    custom_rag_prompt = PromptTemplate.from_template(template)

    rag_chain = ( 
        {"context": vectorstore.as_retriever() | format_docs, "question": RunnablePassthrough()} 
        | custom_rag_prompt
        | llm
    )



    
    print("creating Summary...")

    #Ausblick

    for x in query_set:
        query= x.content
        gsheetcell = x.gsheetcell
        res = rag_chain.invoke(query)
        wks.update_value( gsheetcell, res.content)

    return "Summary created"

    #Incomestatement



