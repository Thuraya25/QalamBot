# Use the latest stable Python version (e.g., Python 3.12 or 3.13)
FROM python:3.12-slim

# Install Java 11 (required for language_tool_python)
RUN apt-get update && apt-get install -y openjdk-11-jre

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Run the bot
CMD ["python", "QalamBot.py"]