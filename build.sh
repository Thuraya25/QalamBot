#!/bin/bash

# Install ncurses-utils to ensure tput works
apt-get update
apt-get install -y ncurses-utils

# Install Java 11 if it's not already installed
apt-get install -y openjdk-11-jdk

# Set JAVA_HOME
export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which javac))))
export PATH=$JAVA_HOME/bin:$PATH

# Check if Java is properly installed
java -version

# Install the Python dependencies
pip install -r requirements.txt

