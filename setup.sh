#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Create .streamlit config directory
mkdir -p ~/.streamlit

# Write Streamlit config file
echo "\
[server]
headless = true
port = \$PORT
enableCORS = false
\n\
" > ~/.streamlit/config.toml

# Start Streamlit app
streamlit run app.py
