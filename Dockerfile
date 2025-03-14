# Use a Python base image
FROM python:3.11-slim

# Install Java (openjdk)
RUN apt-get update && apt-get install -y openjdk-11-jdk

# Set the working directory
WORKDIR /app

# Copy the project files into the container
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Command to run the bot
CMD ["python", "QalamBot.py"]
