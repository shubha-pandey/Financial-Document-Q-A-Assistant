# import required libraries
import streamlit as st
import pandas as pd
import PyPDF2
import io
import requests
import json
import re
from typing import Dict, List, Any, Optional
import numpy as np
import openpyxl
from openpyxl import load_workbook
import plotly.express as px
import plotly.graph_objects as go


# Configure Streamlit page
st.set_page_config(
    page_title="Financial Document Q&A Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Ollama Client : Handles communication with Ollama API for LLM responses
class OllamaClient:
    """Client for interacting with Ollama API"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.available_models = []
        self.check_connection()    # Check if Ollama is running and fetch models
    
    def check_connection(self):
        """Check if Ollama is running and get available models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models_data = response.json()
                self.available_models = [model['name'] for model in models_data.get('models', [])]
                return True
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to Ollama. Please ensure Ollama is running on localhost:11434")
            return False
        except Exception as e:
            st.error(f"❌ Error connecting to Ollama: {str(e)}")
            return False
    
    def generate_response(self, model: str, prompt: str, context: str = "") -> str:
        """Generate response using Ollama model"""
        """Send user question + document content to Ollama and return response"""
        try:
            # Build full prompt with context + question
            full_prompt = f"""You are a financial document analysis assistant. Based on the following financial document content, answer the user's question accurately and concisely.

Document Content:
{context}

User Question: {prompt}

Please provide a clear, accurate answer based only on the information in the document. If the information is not available in the document, please state that clearly."""

            # Request payload
            payload = {
                "model": model,
                "prompt": full_prompt,
                "stream": False
            }
            
            # Call Ollama API
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json().get('response', 'No response generated')
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except requests.exceptions.Timeout:
            return "Request timed out. Please try again."
        except Exception as e:
            return f"Error generating response: {str(e)}"


# Document Processor : Extracts text/data from PDFs and Excel sheets
class DocumentProcessor:
    """Handles processing of PDF and Excel financial documents"""
    
    @staticmethod
    def extract_pdf_text(uploaded_file) -> str:
        """Read PDF and return extracted text"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            st.error(f"Error reading PDF: {str(e)}")
            return ""
    
    @staticmethod
    def extract_excel_data(uploaded_file) -> tuple[str, Dict[str, pd.DataFrame]]:
        """Extract data from Excel file"""
        """Read all Excel sheets → return text summary + DataFrames"""
        try:
            # Read all sheets
            excel_file = pd.ExcelFile(io.BytesIO(uploaded_file.read()))
            sheets_data = {}
            text_summary = ""
            
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                sheets_data[sheet_name] = df
                
                # Create text summary of the sheet
                text_summary += f"\n=== Sheet: {sheet_name} ===\n"
                text_summary += f"Shape: {df.shape[0]} rows, {df.shape[1]} columns\n"
                text_summary += f"Columns: {', '.join(df.columns.astype(str))}\n"
                
                # Add numeric data summary
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    text_summary += "\nNumeric Data Summary:\n"
                    for col in numeric_cols:
                        if df[col].notna().sum() > 0:
                            text_summary += f"{col}: Min={df[col].min():.2f}, Max={df[col].max():.2f}, Mean={df[col].mean():.2f}\n"
                
                # Add first few rows as text
                text_summary += "\nSample Data:\n"
                text_summary += df.head(10).to_string() + "\n"
            
            return text_summary, sheets_data
            
        except Exception as e:
            st.error(f"Error reading Excel file: {str(e)}")
            return "", {}
    
    @staticmethod
    def extract_financial_metrics(text: str) -> Dict[str, Any]:
        """Extract common key financial metrics from text using regex"""
        metrics = {}
        
        # Common financial terms to look for
        patterns = {
            'revenue': r'revenue[s]?\s*:?\s*\$?(\d+(?:,\d{3})*(?:\.\d{2})?)',
            'net_income': r'net\s+income\s*:?\s*\$?(\d+(?:,\d{3})*(?:\.\d{2})?)',
            'total_assets': r'total\s+assets\s*:?\s*\$?(\d+(?:,\d{3})*(?:\.\d{2})?)',
            'total_liabilities': r'total\s+liabilities\s*:?\s*\$?(\d+(?:,\d{3})*(?:\.\d{2})?)',
            'cash': r'cash\s*(?:and\s+equivalents)?\s*:?\s*\$?(\d+(?:,\d{3})*(?:\.\d{2})?)',
            'expenses': r'(?:total\s+)?expenses?\s*:?\s*\$?(\d+(?:,\d{3})*(?:\.\d{2})?)',
        }
        
        for metric, pattern in patterns.items():
            matches = re.findall(pattern, text.lower(), re.IGNORECASE)
            if matches:
                # Convert to float, removing commas
                values = [float(match.replace(',', '')) for match in matches]
                metrics[metric] = values[0] if len(values) == 1 else values
        
        return metrics


# Streamlit Helper Functions
def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []    # chat history
    if 'document_content' not in st.session_state:
        st.session_state.document_content = ""    # raw extracted text
    if 'excel_data' not in st.session_state:
        st.session_state.excel_data = {}    # excel DataFrames
    if 'financial_metrics' not in st.session_state:
        st.session_state.financial_metrics = {}    # extracted metrics
    if 'ollama_client' not in st.session_state:
        st.session_state.ollama_client = OllamaClient()

def display_financial_metrics(metrics: Dict[str, Any]):
    """Display extracted financial metrics"""
    if not metrics:
        return
    
    st.subheader("📈 Extracted Financial Metrics")
    
    cols = st.columns(3)
    col_idx = 0
    
    for metric, value in metrics.items():
        with cols[col_idx % 3]:
            if isinstance(value, list):
                st.metric(metric.replace('_', ' ').title(), f"${value[0]:,.2f}")
            else:
                st.metric(metric.replace('_', ' ').title(), f"${value:,.2f}")
        col_idx += 1

def display_excel_data(excel_data: Dict[str, pd.DataFrame]):
    """Show each Excel sheet in a tab with stats"""
    if not excel_data:
        return
    
    st.subheader("📋 Excel Data")
    
    tabs = st.tabs(list(excel_data.keys()))
    
    for idx, (sheet_name, df) in enumerate(excel_data.items()):
        with tabs[idx]:
            st.write(f"**Sheet: {sheet_name}**")
            st.write(f"Dimensions: {df.shape[0]} rows × {df.shape[1]} columns")
            
            # Display dataframe
            st.dataframe(df, use_container_width=True)
            
            # Show basic statistics for numeric columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                st.write("**Numeric Columns Summary:**")
                st.dataframe(df[numeric_cols].describe(), use_container_width=True)


# Main App
def main():
    """Main application function"""
    initialize_session_state()
    
    # Header
    st.title("📊 Financial Document Q&A Assistant")
    st.markdown("Upload financial documents (PDF or Excel) and ask questions about the data using natural language.")
    
    # Sidebar for model selection and document upload
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Model selection
        if st.session_state.ollama_client.available_models:
            selected_model = st.selectbox(
                "Select Ollama Model",
                st.session_state.ollama_client.available_models,
                help="Choose the language model for answering questions"
            )
        else:
            st.error("No Ollama models available. Please install and run a model.")
            selected_model = None
        
        st.divider()
        
        # Document upload
        st.header("📄 Document Upload")
        uploaded_file = st.file_uploader(
            "Upload Financial Document",
            type=['pdf', 'xlsx', 'xls'],
            help="Upload PDF or Excel files containing financial statements"
        )
        
        if uploaded_file is not None:
            with st.spinner("Processing document..."):
                processor = DocumentProcessor()
                
                if uploaded_file.type == "application/pdf":
                    # Extract PDF
                    content = processor.extract_pdf_text(uploaded_file)
                    st.session_state.document_content = content
                    st.session_state.excel_data = {}
                    
                elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
                                           "application/vnd.ms-excel"]:
                    # Extract Excel
                    content, excel_data = processor.extract_excel_data(uploaded_file)
                    st.session_state.document_content = content
                    st.session_state.excel_data = excel_data
                
                # Extract key financial metrics
                st.session_state.financial_metrics = processor.extract_financial_metrics(content)
                
                st.success(f"✅ Document processed successfully!")
                st.write(f"**File:** {uploaded_file.name}")
                st.write(f"**Type:** {uploaded_file.type}")
                st.write(f"**Size:** {uploaded_file.size / 1024:.1f} KB")
    
    # Main content area
    if st.session_state.document_content:
        # Display financial metrics
        display_financial_metrics(st.session_state.financial_metrics)
        
        # Display Excel data if available
        if st.session_state.excel_data:
            display_excel_data(st.session_state.excel_data)
        
        st.divider()
        
        # Q&A Interface
        st.subheader("💬 Ask Questions About Your Financial Document")
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # User input
        if prompt := st.chat_input("Ask a question about your financial document..."):
            if selected_model is None:
                st.error("Please select an Ollama model first.")
                return
            
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate assistant response
            with st.chat_message("assistant"):
                with st.spinner("Analyzing document and generating response..."):
                    response = st.session_state.ollama_client.generate_response(
                        selected_model,
                        prompt,
                        st.session_state.document_content
                    )
                    st.markdown(response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Quick question buttons
        st.subheader("🚀 Quick Questions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("What is the total revenue?"):
                if selected_model:
                    st.session_state.messages.append({"role": "user", "content": "What is the total revenue?"})
                    with st.spinner("Generating response..."):
                        response = st.session_state.ollama_client.generate_response(
                            selected_model,
                            "What is the total revenue?",
                            st.session_state.document_content
                        )
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.rerun()
        
        with col2:
            if st.button("What are the main expenses?"):
                if selected_model:
                    st.session_state.messages.append({"role": "user", "content": "What are the main expenses?"})
                    with st.spinner("Generating response..."):
                        response = st.session_state.ollama_client.generate_response(
                            selected_model,
                            "What are the main expenses?",
                            st.session_state.document_content
                        )
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.rerun()
        
        with col3:
            if st.button("What is the net income?"):
                if selected_model:
                    st.session_state.messages.append({"role": "user", "content": "What is the net income?"})
                    with st.spinner("Generating response..."):
                        response = st.session_state.ollama_client.generate_response(
                            selected_model,
                            "What is the net income?",
                            st.session_state.document_content
                        )
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.rerun()
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
    
    else:
        # Welcome screen
        st.info("👈 Please upload a financial document from the sidebar to get started.")
        
        # Instructions
        st.subheader("📖 How to Use")
        st.markdown("""
        1. **Install Ollama**: Make sure Ollama is installed and running locally
        2. **Download a Model**: Install a language model (e.g., `ollama pull llama3.2`)
        3. **Upload Document**: Use the sidebar to upload a PDF or Excel financial document
        4. **Ask Questions**: Use natural language to query your financial data
        
        ### Supported Document Types:
        - 📄 **PDF**: Income statements, balance sheets, cash flow statements
        - 📊 **Excel**: Financial spreadsheets with numeric data
        
        ### Example Questions:
        - "What is the total revenue for this period?"
        - "How much did we spend on marketing?"
        - "What is our net profit margin?"
        - "Compare revenue to expenses"
        """)

    # Footer
    st.markdown("---")
    st.markdown("© Financial Document Q&A Assistant | Created by Shubha Pandey")

# Entry point
if __name__ == "__main__":
    main()