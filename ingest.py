from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os


#STEP 1: PDF LOADING PROCESS
print("PDF loading...")
loader = PDFPlumberLoader("documents/DETAIL-AND-POLICY-OF-KIPMCET.pdf")
documents = loader.load()


#STEP 2: CHUNKING

print("Chunks...")
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = splitter.split_documents(documents)

# STEP 3: Embeddings 
print("Embeddings...")
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

#STEP 4: SAVE DATA IN VECTORDB
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="vectorstore"
)

print("Done! ✅")