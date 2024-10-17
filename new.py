import streamlit as st
from streamlit import session_state
import time
import base64
import os
from vectors import FinancialDocumentProcessor
from chatbot import FinancialChatbotManager

def displayPDF(file):
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

if 'temp_pdf_path' not in st.session_state:
    st.session_state['temp_pdf_path'] = None

if 'chatbot_manager' not in st.session_state:
    st.session_state['chatbot_manager'] = None

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

st.set_page_config(
    page_title="FinDocs Analyzer",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for finance theme
st.markdown("""
<style>
    .stApp {
        background-color: #f0f3f6;
    }
    .stButton>button {
        color: #ffffff;
        background-color: #1e3a8a;
        border-radius: 5px;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    h1, h2, h3 {
        color: #1e3a8a;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("finance.png", use_column_width=True)
    st.markdown("### 📊 FinDocs Analyzer")
    st.markdown("---")
    
    menu = ["📈 Dashboard", "🤖 AI Assistant", "📞 Support"]
    choice = st.selectbox("Navigate", menu)

if choice == "📈 Dashboard":
    st.title("📄 FinDocs Analyzer Dashboard")
    st.markdown("""
    Welcome to **FinDocs Analyzer**! 🚀

    **Powered by Advanced AI and Natural Language Processing**

    - **Upload Financial Documents**: Securely upload your PDF financial reports.
    - **Analyze**: Get in-depth analysis and insights from your documents.
    - **Interact**: Engage with our AI assistant for detailed financial queries.

    Enhance your financial document analysis with FinDocs Analyzer! 💼
    """)

elif choice == "🤖 AI Assistant":
    st.title("🤖 Financial AI Assistant")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        st.header("📂 Upload Financial Document")
        uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
        if uploaded_file is not None:
            st.success("📄 Financial Document Uploaded")
            st.markdown(f"**Document:** {uploaded_file.name}")
            st.markdown(f"**Size:** {uploaded_file.size/1000:.2f} KB")
            
            temp_pdf_path = "temp_financial_doc.pdf"
            with open(temp_pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.session_state['temp_pdf_path'] = temp_pdf_path

    with col2:
        st.header("🧠 Document Processing")
        process_doc = st.button("🔍 Analyze Document")
        if process_doc:
            if st.session_state['temp_pdf_path'] is None:
                st.warning("⚠️ Please upload a financial document first.")
            else:
                try:
                    financial_processor = FinancialDocumentProcessor(
                        model_name="BAAI/bge-small-en",
                        device="cpu",
                        encode_kwargs={"normalize_embeddings": True},
                        qdrant_url="http://localhost:6333",
                        collection_name="financial_docs_db"
                    )
                    
                    with st.spinner("🔄 Processing financial data..."):
                        result = financial_processor.process_financial_document(st.session_state['temp_pdf_path'])
                        time.sleep(1)
                    st.success(result)
                    
                    if st.session_state['chatbot_manager'] is None:
                        st.session_state['chatbot_manager'] = FinancialChatbotManager(
                            model_name="BAAI/bge-small-en",
                            device="cpu",
                            encode_kwargs={"normalize_embeddings": True},
                            llm_model="llama3.2:3b",
                            llm_temperature=0.7,
                            qdrant_url="http://localhost:6333",
                            collection_name="financial_docs_db"
                        )
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    with col3:
        st.header("💬 Financial Document Q&A")
        
        if st.session_state['chatbot_manager'] is None:
            st.info("🤖 Please upload and analyze a financial document to start querying.")
        else:
            for msg in st.session_state['messages']:
                st.chat_message(msg['role']).markdown(msg['content'])

            if user_input := st.chat_input("Ask about the financial document..."):
                st.chat_message("user").markdown(user_input)
                st.session_state['messages'].append({"role": "user", "content": user_input})

                with st.spinner("🤖 Analyzing..."):
                    try:
                        answer = st.session_state['chatbot_manager'].get_response(user_input)
                        time.sleep(1)
                    except Exception as e:
                        answer = f"⚠️ An error occurred during analysis: {e}"
                
                st.chat_message("assistant").markdown(answer)
                st.session_state['messages'].append({"role": "assistant", "content": answer})

elif choice == "📞 Support":
    st.title("📬 Contact FinDocs Support")
    st.markdown("""
    For any inquiries or assistance with FinDocs Analyzer:

    - **Email:** [support@findocsanalyzer.com](mailto:support@findocsanalyzer.com) ✉️
    - **Phone:** +1 (555) 123-4567 ☎️
    - **Hours:** Monday to Friday, 9 AM - 5 PM EST

    For technical support or to report issues, please visit our [Support Portal](https://support.findocsanalyzer.com).
    """)

st.markdown("---")
st.markdown("© 2024 FinDocs Analyzer. All rights reserved. | [Privacy Policy](https://www.findocsanalyzer.com/privacy) | [Terms of Service](https://www.findocsanalyzer.com/terms)")