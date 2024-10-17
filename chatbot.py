import os
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain_ollama import ChatOllama
from qdrant_client import QdrantClient
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
import streamlit as st

class FinancialChatbotManager:
    def __init__(
        self,
        model_name: str = "BAAI/bge-small-en",
        device: str = "cpu",
        encode_kwargs: dict = {"normalize_embeddings": True},
        llm_model: str = "llama3.2:3b",
        llm_temperature: float = 0.7,
        qdrant_url: str = "http://localhost:6333",
        collection_name: str = "financial_docs_db",
    ):
        self.model_name = model_name
        self.device = device
        self.encode_kwargs = encode_kwargs
        self.llm_model = llm_model
        self.llm_temperature = llm_temperature
        self.qdrant_url = qdrant_url
        self.collection_name = collection_name

        self.embeddings = HuggingFaceBgeEmbeddings(
            model_name=self.model_name,
            model_kwargs={"device": self.device},
            encode_kwargs=self.encode_kwargs,
        )

        self.llm = ChatOllama(
            model=self.llm_model,
            temperature=self.llm_temperature,
        )

        self.prompt_template = """You are a financial analyst AI assistant. Use the following information to answer the user's question about the financial document.
If you don't know the answer, state that you don't have enough information to provide an accurate response.

Context: {context}
Question: {question}

Provide a detailed and well-explained answer, focusing on financial insights and implications:
"""

        self.client = QdrantClient(
            url=self.qdrant_url, prefer_grpc=False
        )

        self.db = Qdrant(
            client=self.client,
            embeddings=self.embeddings,
            collection_name=self.collection_name
        )

        self.prompt = PromptTemplate(
            template=self.prompt_template,
            input_variables=['context', 'question']
        )

        self.retriever = self.db.as_retriever(search_kwargs={"k": 3})

        self.chain_type_kwargs = {"prompt": self.prompt}

        self.qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=False,
            chain_type_kwargs=self.chain_type_kwargs,
            verbose=False
        )

    def get_response(self, query: str) -> str:
        try:
            response = self.qa.run(query)
            return response
        except Exception as e:
            st.error(f"⚠️ An error occurred while analyzing the financial data: {e}")
            return "⚠️ I apologize, but I encountered an issue while processing your financial query. Please try again or rephrase your question."