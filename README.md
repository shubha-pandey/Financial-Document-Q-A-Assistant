# Financial Document Q&A Assistant

A web application that processes financial documents (PDF and Excel) and provides an interactive question-answering system using natural language processing with Ollama and local Small Language Models (SLMs).

## 🚀 Features

- **Document Processing**: Upload and process PDF and Excel financial documents
- **Smart Extraction**: Automatically extract financial metrics and data
- **Natural Language Q&A**: Ask questions about your financial data in plain English
- **Interactive Interface**: Clean, intuitive web interface built with Streamlit
- **Local Processing**: Uses Ollama for privacy-focused local AI processing
- **Multiple Formats**: Supports PDF financial statements and Excel spreadsheets

## 📋 Requirements

### System Requirements
- Python 3.8 or higher
- Ollama installed and running locally
- At least one Ollama model downloaded

### Supported Document Types
- PDF files (Income statements, Balance sheets, Cash flow statements)
- Excel files (XLSX, XLS with financial data)

## 🛠️ Installation & Setup

### 1. Install Ollama

First, install Ollama on your system:

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
Download from [ollama.ai](https://ollama.ai)

### 2. Download an Ollama Model

Start Ollama and download a model:
```bash
# Start Ollama service
ollama serve

# In another terminal, download a model (recommended)
ollama pull llama3.2
# or
ollama pull mistral
# or
ollama pull codellama
```

### 3. Clone and Setup the Project

```bash
# Clone the repository
git clone https://github.com/yourusername/financial-document-qa
cd financial-document-qa

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Usage

### 1. Start Ollama Service
Make sure Ollama is running:
```bash
ollama serve
```

### 2. Run the Application
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### 3. Using the Application

1. **Upload Document**: Use the sidebar to upload a PDF or Excel financial document
2. **Select Model**: Choose an available Ollama model from the dropdown
3. **Review Extracted Data**: View automatically extracted financial metrics
4. **Ask Questions**: Use the chat interface to ask questions about your data

### Example Questions
- "What is the total revenue for this period?"
- "How much did we spend on operating expenses?"
- "What is our net profit margin?"
- "Compare current assets to current liabilities"
- "Show me the cash flow from operations"

## 🏗️ Project Structure

```
financial-document-qa/
├── Assignment Problem Statemnt.pdf   # problem statement
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── test_setup.py.txt      # Setup verification script
├── run_app.sh             # Automated deployment script
├── generate_sample_docs.py             # Script to generate sample documents
└── sample_documents/     # Sample financial documents for testing
    ├── sample_financial_statements.xlsx   # Sample excel workbook
    └── sample_income_statement.pdf.xlsx   # Sample PDF report
```


## 📊 Sample Documents

To test the application, generate sample financial documents:

```bash
python generate_sample_documents.py
```

This creates:
- **sample_financial_statements.xlsx**: Multi-sheet Excel workbook containing:
  - Income Statement (quarterly data)
  - Balance Sheet (3 periods)
  - Cash Flow Statement (quarterly)
  - Key Metrics Summary
- **sample_income_statement.pdf**: Professional income statement report

The sample documents contain realistic financial data for a fictional company "TechCorp Industries Inc." with quarterly financial results.



## 🔧 Configuration

### Ollama Configuration
- Default URL: `http://localhost:11434`
- Modify the `OllamaClient` base_url if running on a different port

### Model Selection
The application automatically detects available Ollama models. Popular models for financial analysis:
- `llama3.2`: Good general-purpose model
- `mistral`: Fast and efficient
- `codellama`: Good for structured data analysis

## 🎯 Key Components

### DocumentProcessor Class
- Extracts text from PDF files using PyPDF2
- Processes Excel files and converts to readable format
- Identifies common financial metrics using regex patterns

### OllamaClient Class
- Manages connection to local Ollama API
- Handles model selection and response generation
- Implements proper error handling and timeouts

### Financial Metrics Extraction
Automatically identifies common financial terms:
- Revenue/Sales
- Net Income
- Total Assets
- Total Liabilities
- Cash and Equivalents
- Operating Expenses

## 🐛 Troubleshooting

### Common Issues

**"Cannot connect to Ollama"**
- Ensure Ollama is installed and running (`ollama serve`)
- Check if port 11434 is available
- Verify firewall settings

**"No Ollama models available"**
- Download a model: `ollama pull llama3.2`
- Wait for the model to fully download
- Refresh the application

**PDF processing errors**
- Ensure PDF is not password protected
- Try with a different PDF file
- Check if PDF contains readable text (not just images)

**Excel processing errors**
- Ensure Excel file is not corrupted
- Try saving Excel file in xlsx format
- Check if file contains numeric data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai) for local AI model serving
- [Streamlit](https://streamlit.io) for the web application framework
- [PyPDF2](https://pypdf2.readthedocs.io/) for PDF processing
- [Pandas](https://pandas.pydata.org/) for data manipulation

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Open an issue on GitHub
3. Make sure you're using the latest versions of all dependencies

---

**Note**: This application processes documents locally on your machine. No data is sent to external servers, ensuring privacy and security of your financial information.
