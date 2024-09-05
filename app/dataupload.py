import os
import re
from openai import OpenAI
import uuid

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import tempfile
from pinecone import Pinecone, ServerlessSpec




def companyfileupload(path,settings,isin,company_name):
    load_dotenv()
    indexname = settings.indexname
    embeddingmodell = settings.embedding
    llmmodell = settings.llm
    name = company_name
    # Initialize OpenAI
    MODEL = embeddingmodell



    # Initialize Pinecone
    pc = Pinecone(
        api_key=os.environ.get("PINECONE_API_KEY")
    )

    # Define the index name
    index_name = indexname

    # Instantiate the index
    index = pc.Index(index_name)

    # Define a function to preprocess text
    def preprocess_text(text):
        # Replace consecutive spaces, newlines and tabs
        text = re.sub(r'\s+', ' ', text)
        return text

    def process_pdf(file_path):
        # create a loader
        loader = PyPDFLoader(file_path)
        # load your data
        data = loader.load()
        # Split your data up into smaller documents with Chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1800, chunk_overlap=50)
        documents = text_splitter.split_documents(data)
        # Convert Document objects into strings
        texts = [str(doc) for doc in documents]
        print(f"Number of text chunks created: {len(texts)}") 
        return texts

    # Define a function to create embeddings
    def create_embeddings(texts):
        embeddings_list = []
        for text in texts:
            res = client.embeddings.create(input=[text], model=MODEL)
            embeddings_list.append(res.data[0].embedding)
        return embeddings_list

    # Define a function to upsert embeddings to Pinecone
    def upsert_embeddings_to_pinecone(index, embeddings, name):
        unique_id = str(uuid.uuid4())
        ids = [f"{name}_{unique_id}_{i}" for i in range(len(embeddings))]
        index.upsert(vectors=[(id, embedding) for id, embedding in zip(ids, embeddings)], namespace=name )

    # Process a PDF and create embeddings
    file_path = path # Replace with your actual file path
    texts = process_pdf(file_path)
    embeddings = create_embeddings(texts)

    # Upsert the embeddings to Pinecone
    upsert_embeddings_to_pinecone(index, embeddings, name)
    print(f"Number of text chunks upserted: {len(embeddings)}") 

    os.remove(path)
    print(f'Temporary PDF deleted: {path}')

def store_pdf_from_variable(filestorage):
    # Create a temporary file to store the PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        pdf_content = filestorage.read()
        temp_file.write(pdf_content)  
        temp_file_path = temp_file.name 

    return(temp_file_path)

