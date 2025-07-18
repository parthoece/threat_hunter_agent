from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

def build_qa_chain(retriever):
    llm = Ollama(model="mistral")
    template = PromptTemplate(
        input_variables=["context", "question"],
        template="""
        You are an ICS Incident Response Assistant.
        Based on the following incidents:

        {context}

        Answer the user's question: {question}
        """
    )
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": template}
    )
