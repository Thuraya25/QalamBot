#!/bin/bash
# Install Java 23 (required for language_tool_python)
apt-get update
apt-get install -y openjdk-23-jre

# Set JAVA_HOME environment variable
export JAVA_HOME=/usr/lib/jvm/java-23-openjdk-amd64

# Install Python dependencies
pip install -r requirements.txt