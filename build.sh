#!/bin/bash
# Install Java 23 (required for language_tool_python)
apt-get update
apt-get install -y openjdk-23-jre

# Install Python dependencies
pip install -r requirements.txt