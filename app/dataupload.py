import os
import re
import openai
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import tempfile
from pinecone import Pinecone, ServerlessSpec

    


def companyfileupload(path,settings,isin,company_name):
    load_dotenv()
    indexname = settings.indexname
    embeddingmodell = settings.embedding
    llmmodell = settings.llm
    
    # Initialize OpenAI
    openai.api_key = os.getenv('OPENAI_API_KEY')
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
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        documents = text_splitter.split_documents(data)
        # Convert Document objects into strings
        texts = [str(doc) for doc in documents]
        return texts

    # Define a function to create embeddings
    def create_embeddings(texts):
        embeddings_list = []
        for text in texts:
            res = openai.Embedding.create(input=[text], engine=MODEL)
            embeddings_list.append(res['data'][0]['embedding'])
        return embeddings_list

    # Define a function to upsert embeddings to Pinecone
    def upsert_embeddings_to_pinecone(index, embeddings, ids):
        index.upsert(vectors=[(id, embedding) for id, embedding in zip(ids, embeddings)])

    # Process a PDF and create embeddings
    file_path = path # Replace with your actual file path
    texts = process_pdf(file_path)
    embeddings = create_embeddings(texts)

    # Upsert the embeddings to Pinecone
    upsert_embeddings_to_pinecone(index, embeddings, [file_path])

def store_pdf_from_variable(filestorage):
    # Create a temporary file to store the PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        pdf_content = filestorage.read()
        temp_file.write(pdf_content)  
        temp_file_path = temp_file.name 

    return(temp_file_path)
    
    # Use the temporary file as needed
    # ...

    # Clean up the temporary file when done
#  os.remove(temp_file_path)
#  print(f'Temporary PDF deleted: {temp_file_path}')

# Example usage

