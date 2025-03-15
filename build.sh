##!/bin/bash
# Install Java 11 (required for language_tool_python)
apt-get update
apt-get install -y openjdk-11-jre

# Set JAVA_HOME environment variable
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

apt-get install -y ncurses-bin

# Install Python dependencies
pip install -r requirements.txt
