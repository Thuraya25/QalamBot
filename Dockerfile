FROM python:3.11-slim

# Install Java 23
RUN apt-get update && apt-get install -y openjdk-23-jre

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Run the bot
CMD ["python", "QalamBot.py"]