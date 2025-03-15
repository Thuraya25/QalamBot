#!/bin/bash

# Install Java 11 (if not already installed)
sudo apt update
sudo apt install -y openjdk-11-jdk

# Set JAVA_HOME
export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which javac))))
export PATH=$JAVA_HOME/bin:$PATH

# Check if Java is installed
java -version

# Install Python dependencies
pip install -r requirements.txt
