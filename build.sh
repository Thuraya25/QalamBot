#!/bin/bash
# Install Java 11 (required for language_tool_python)
apt-get update
apt-get install -y openjdk-11-jre

# Install Python dependencies
pip install -r requirements.txt