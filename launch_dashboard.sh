#!/bin/bash

# NK Hajduk 1932 Dashboard Launch Script

echo "🚀 Launching NK Hajduk 1932 Dashboard..."
echo ""

# Activate virtual environment
source venv/bin/activate

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null
then
    echo "❌ Streamlit not found. Installing dependencies..."
    pip install -r requirements.txt
fi

# Launch dashboard
echo "✓ Starting Streamlit server..."
echo "📊 Dashboard will open in your browser at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app.py
