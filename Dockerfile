# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variable for non-interactive installation (useful for apt-get)
ENV DEBIAN_FRONTEND=noninteractive

# Install Java (required by language_tool_python)
RUN apt-get update && apt-get install -y openjdk-11-jdk && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install the Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Command to run your bot
CMD ["python", "QalamBot.py"]
