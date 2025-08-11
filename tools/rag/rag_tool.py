import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

def ingest_bible(file_path: str) -> PineconeVectorStore:
    """Ingest the Bible text for RAG indexing."""
    loader = TextLoader(file_path)
    document = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(document)

    # Initialize embeddings with the correct dimension
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))

    # Ensure the Pinecone index is created with the correct dimension
    vector_store = PineconeVectorStore.from_documents(
        texts, embeddings, index_name=os.environ["INDEX_NAME"]
    )

    return vector_store