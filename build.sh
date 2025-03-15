#!/bin/bash
# Install Java (required for language_tool_python)
apt-get update
apt-get install -y default-jre

# Install Python dependencies
pip install -r requirements.txt