import os
import pickle
from tqdm import tqdm
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document

EMBEDDING_CACHE_PATH = "embedding_cache.pkl"

def create_vectorstore(docs, index_path="faiss_index"):
    """
    Create or load a FAISS vectorstore using HuggingFace embeddings with caching.

    Args:
        docs (List[Document]): List of LangChain Document objects.
        index_path (str): Directory path for saving or loading FAISS index.

    Returns:
        FAISS: The vectorstore instance for retrieval.
    """
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    if os.path.exists(index_path):
        print("Loading existing FAISS index from:", index_path)
        return FAISS.load_local(index_path, embedding_model, allow_dangerous_deserialization=True)


    if os.path.exists(EMBEDDING_CACHE_PATH):
        print("Loading cached document embeddings from:", EMBEDDING_CACHE_PATH)
        with open(EMBEDDING_CACHE_PATH, "rb") as f:
            embedded_docs = pickle.load(f)
    else:
        print("Generating embeddings using HuggingFace model...")
        texts = [doc.page_content for doc in docs]
        metadatas = [doc.metadata for doc in docs]

        embedded_docs = []
        for i in tqdm(range(len(texts)), desc="Embedding documents"):
            embedded_docs.append(
                Document(
                    page_content=texts[i],
                    metadata=metadatas[i]
                )
            )

        with open(EMBEDDING_CACHE_PATH, "wb") as f:
            pickle.dump(embedded_docs, f)
        print("Embeddings cached to:", EMBEDDING_CACHE_PATH)

    print("Creating FAISS index from embedded documents...")
    vectorstore = FAISS.from_documents(embedded_docs, embedding_model)
    vectorstore.save_local(index_path)
    print("FAISS index saved at:", index_path)
    return vectorstore
