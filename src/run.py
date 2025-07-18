from src.extract_ics import extract_ics_incidents
from src.preprocess import preprocess_for_langchain
from src.vector_store import create_vectorstore
from src.qa_chain import build_qa_chain

def main():
    data_path = "data/vcdb"
    ics_data = extract_ics_incidents(data_path)
    documents = preprocess_for_langchain(ics_data)
    vectorstore = create_vectorstore(documents)
    retriever = vectorstore.as_retriever()

    qa = build_qa_chain(retriever)
    while True:
        query = input("Ask about ICS incidents: ")
        if query.lower() in ["exit", "quit"]:
            break
        answer = qa.run(query)
        print("\nAssistant:", answer, "\n")

if __name__ == "__main__":
    main()
