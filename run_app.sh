#!/bin/bash

# Financial Document Q&A Assistant - Deployment Script
#   -->
# This script sets up and runs the application
# It:
#   --> Checks Python installation
#   --> Verifies Ollama is running and models available
#   --> Sets up a virtual environment
#   --> Installs dependencies
#   --> Runs the setup test
#   --> Starts the Streamlit app if everything passes


set -e  # Exit on any error

echo "🚀 Financial Document Q&A Assistant Setup"
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check if Ollama is running
echo "🔍 Checking Ollama connection..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama is running"
    
    # Check available models
    models=$(curl -s http://localhost:11434/api/tags | python3 -c "import json, sys; data=json.load(sys.stdin); print(len(data.get('models', [])))")
    if [ "$models" -eq 0 ]; then
        echo "⚠️  No Ollama models found. Downloading llama3.2..."
        ollama pull llama3.2
    else
        echo "✅ Found $models Ollama model(s)"
    fi
else
    echo "❌ Ollama is not running. Please start it with: ollama serve"
    echo "   If not installed, get it from: https://ollama.ai"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Run setup test
echo "🧪 Running setup test..."
python3 test_setup.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Setup completed successfully!"
    echo "🌐 Starting the application..."
    echo "   The app will open at: http://localhost:8501"
    echo ""
    echo "Press Ctrl+C to stop the application"
    echo ""
    
    # Start the Streamlit application
    streamlit run app.py
else
    echo "❌ Setup test failed. Please check the errors above."
    exit 1
fi