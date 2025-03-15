#!/bin/bash
# Install Java (required for language_tool_python)
sudo apt-get update
sudo apt-get install -y default-jre

# Install Python dependencies
pip install -r requirements.txt