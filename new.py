import streamlit as st
from streamlit import session_state
import time
import base64
import os
from vectors import EmbeddingsManager
from chatbot import ChatbotManager

# Function to display the PDF of a given file
def displayPDF(file):
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# Initialize session_state variables
if 'temp_pdf_path' not in st.session_state:
    st.session_state['temp_pdf_path'] = None
if 'chatbot_manager' not in st.session_state:
    st.session_state['chatbot_manager'] = None
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Set page configuration
st.set_page_config(
    page_title="FinDoc Analyzer",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for finance theme
st.markdown("""
    <style>
    .main {
        background-color: #f0f5f9;
    }
    .stButton>button {
        background-color: #1e3a8a;
        color: white;
    }
    .stTextInput>div>div>input {
        background-color: #ffffff;
    }
    h1, h2, h3 {
        color: #1e3a8a;
    }
    .stSidebar {
        background-color: #1e3a8a;
        color: white;
    }
    .stSidebar .stSelectbox label {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("finance.pngb", use_column_width=True)
    st.markdown("### FinDoc Analyzer")
    st.markdown("Your AI-powered financial document assistant")
    st.markdown("---")
    menu = ["Dashboard", "Document Analysis", "Chat Assistant", "About"]
    choice = st.selectbox("Navigate", menu)

# Dashboard
if choice == "Dashboard":
    st.title("FinDoc Analyzer Dashboard")
    st.markdown("""
    Welcome to **FinDoc Analyzer**!

    Harness the power of AI to analyze and interact with your financial documents:

    - 📊 **Document Upload**: Securely upload your financial PDFs
    - 🔍 **Intelligent Analysis**: Get instant insights and summaries
    - 💬 **AI Chat**: Ask questions about your documents in natural language

    Start by navigating to the Document Analysis section to upload your first document.
    """)

    # Add some dummy metrics for visual appeal
    col1, col2, col3 = st.columns(3)
    col1.metric("Documents Analyzed", "27", "+3")
    col2.metric("Time Saved", "89 hours", "+12%")
    col3.metric("Accuracy Rate", "99.7%", "+0.2%")

# Document Analysis Page
elif choice == "Document Analysis":
    st.title("Document Analysis")
    
    uploaded_file = st.file_uploader("Upload a financial document (PDF)", type=["pdf"])
    if uploaded_file is not None:
        st.success("File Uploaded Successfully!")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Document Preview")
            displayPDF(uploaded_file)
        
        with col2:
            st.markdown("### Document Info")
            st.markdown(f"**Filename:** {uploaded_file.name}")
            st.markdown(f"**File Size:** {uploaded_file.size} bytes")
            
            st.markdown("### Actions")
            if st.button("Create Embeddings"):
                # Your embedding creation logic here
                st.info("Embeddings created successfully!")
            
            if st.button("Generate Summary"):
                # Your summary generation logic here
                st.info("Summary generated. View in the Chat Assistant.")

# Chat Assistant Page
elif choice == "Chat Assistant":
    st.title("AI Chat Assistant")
    
    if st.session_state['chatbot_manager'] is None:
        st.info("Please upload a document and create embeddings in the Document Analysis section first.")
    else:
        st.markdown("Ask questions about your financial documents:")
        
        # Display chat messages
        for msg in st.session_state['messages']:
            st.chat_message(msg['role']).markdown(msg['content'])
        
        # User input
        user_input = st.chat_input("Type your financial question here...")
        if user_input:
            st.session_state['messages'].append({"role": "user", "content": user_input})
            st.chat_message("user").markdown(user_input)
            
            with st.spinner("Analyzing..."):
                # Your chatbot logic here
                response = "This is a placeholder response. Implement your chatbot logic here."
            
            st.session_state['messages'].append({"role": "assistant", "content": response})
            st.chat_message("assistant").markdown(response)

# About Page
elif choice == "About":
    st.title("About FinDoc Analyzer")
    st.markdown("""
    FinDoc Analyzer is an AI-powered tool designed to revolutionize how financial professionals interact with documents.

    **Key Features:**
    - 🧠 Powered by Llama 3.2 and BGE Embeddings
    - 🔒 Secure local processing with Docker
    - 🚀 Fast and accurate document analysis
    - 💬 Interactive AI chat assistant

    **Tech Stack:**
    - Llama 3.2 for natural language processing
    - BGE Embeddings for document representation
    - Qdrant for vector storage
    - Streamlit for the user interface

    For support or inquiries, contact: support@findocanalyzer.com
    """)

# Footer
st.markdown("---")
st.markdown("© 2024 FinDoc Analyzer | Powered by AI")