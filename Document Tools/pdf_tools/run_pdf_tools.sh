#!/bin/bash
echo "Activating virtual environment..."
source pdf_tools_env/Scripts/activate
echo "Installing any missing dependencies..."
pip install -r requirements.txt
echo "Starting PDF Tools..."
streamlit run pdf_tools/app.py