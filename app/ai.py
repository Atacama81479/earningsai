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
    Gcredentialpath = os.getenv('PATH_TO_CREDENTIALS') 
    gsheetnr = int(settings.gsheetno)
    gsheetname = settings.gsheetname
    indexname = settings.indexname
    companyname = settings.companyname
    rag_promt = settings.rag_prompt
    embeddingmodell = settings.embedding
    llmmodell = settings.llm


    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)


    
    ##OpenAI Setup
    embeddings = OpenAIEmbeddings(model= embeddingmodell)
    llm = ChatOpenAI(model= llmmodell)


    ##Vectorstore Setup
    vectorstore = PineconeVectorStore(index_name= indexname, embedding=embeddings, namespace=companyname)

    ##GSheet Setup
    gc = pygsheets.authorize(service_file= Gcredentialpath)
    sheet= gc.open(gsheetname)
    wks = sheet[gsheetnr]
    

    
    ##RAG Chain creation            
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

    for x in query_set:
        company = companyname
        query= str(x.content)
        query = query.format(company)
    

        gsheetcell = x.gsheetcell
        res = rag_chain.invoke(query)
        print(res)
        wks.update_value( gsheetcell, res.content)

    return "Summary created"


## function to query openAI per chat input
def askchat(settings, query):
    load_dotenv()
    indexname = settings.indexname
    companyname = settings.companyname
    rag_promt = settings.rag_prompt
    embeddingmodell = settings.embedding
    llmmodell = settings.llm

    query= str(query)
    query = query.format(companyname)


    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)




    embeddings = OpenAIEmbeddings(model= embeddingmodell)
    llm = ChatOpenAI(model= llmmodell)

    print(settings.companyname)


    vectorstore = PineconeVectorStore(index_name= indexname, embedding=embeddings, namespace=companyname)



                
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


    print(rag_chain)
    print(query)

    res = rag_chain.invoke(query)

    print(res)

    return res


## function to query openAI per chat input without RAG
def askchat2(settings, query):
    load_dotenv()
    indexname = settings.indexname
    companyname = settings.companyname
    embeddingmodell = settings.embedding
    llmmodell = settings.llm
    query= str(query)
    query = query.format(companyname)

    llm = ChatOpenAI(model= llmmodell)   
    
             
    fullquery = query+""" Helpful answer: """
    chain = PromptTemplate.from_template(template=fullquery) | llm
    res = chain.invoke(input = {})

    return res