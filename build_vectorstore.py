from utils.data_utils import build_vectorstore_from_local_docs

if __name__ == "__main__":
    build_vectorstore_from_local_docs()
    print("✅ Vectorstore successfully built and saved in data/vectorstore/")