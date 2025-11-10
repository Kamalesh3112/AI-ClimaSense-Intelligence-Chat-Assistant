# chains/rag_chain.py
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from services.llm_client import get_llm
from utils.data_utils import build_vectorstore_from_local_docs

# Load environment variables (ensures OpenAI/Groq API key is available)
load_dotenv()

def load_vectorstore():
    """Loads or rebuilds the FAISS vectorstore from local documents."""
    try:
        print("🔍 Loading vectorstore from local data...")
        return build_vectorstore_from_local_docs()
    except Exception as e:
        print(f"⚠️ Error loading vectorstore: {e}")
        raise

def get_rag_response(query: str):
    """
    Retrieves a contextual answer from the local FAISS vector database.
    Uses HuggingFace sentence transformer embeddings and Llama/Groq LLM.
    """

    # --- 1️. Load FAISS vector store
    vectorstore_path = os.path.join("data", "vectorstore")
    if not os.path.exists(vectorstore_path):
        return "[RAG Error] Vector store not found. Please run your data ingestion first."

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=True)

    # --- 2. Retrieve top relevant documents
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    docs = retriever._get_relevant_documents(query, run_manager=None)
    context = "\n\n".join([d.page_content for d in docs]) if docs else "No relevant documents found."

    # --- 3️. Prepare prompt for LLM
    prompt = PromptTemplate(
        input_variables=["context", "query"],
        template=(
            "You are a domain expert in agriculture, environment, and sustainability.\n\n"
            "CONTEXT:\n{context}\n\n"
            "USER QUESTION:\n{query}\n\n"
            "Provide a structured, concise, and fact-based answer based only on the context provided. Always do factcheck and groundness for avoiding hallucinations"
        ),
    )

    llm = get_llm()
    chain = prompt | llm | StrOutputParser()

    # --- 4️. Run and return response
    try:
        return chain.invoke({"context": context, "query": query})
    except Exception as e:
        return f"[RAG Error] {e}"