#!/bin/bash

# Install necessary utilities like tput
sudo apt update
sudo apt install -y ncurses-utils

# Install Java 11
sudo apt install -y openjdk-11-jdk

# Set JAVA_HOME
export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which javac))))
export PATH=$JAVA_HOME/bin:$PATH

# Check Java version
java -version

# Install Python dependencies
pip install -r requirements.txt
