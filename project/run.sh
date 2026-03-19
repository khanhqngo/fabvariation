#!/bin/bash

# FabVariation - Quick Start Script
# This script checks dependencies and runs the Streamlit app

echo "================================================"
echo "  FabVariation - Process Variation Simulator"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.11 or higher."
    exit 1
fi

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Check if streamlit is installed
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo ""
    echo "Streamlit not found. Installing dependencies..."
    pip install -r requirements.txt
fi

# Run the app
echo ""
echo "Starting FabVariation..."
echo "The app will open in your browser at http://localhost:8501"
echo ""
streamlit run app.py
