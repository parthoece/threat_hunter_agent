# syntax=docker/dockerfile:1
FROM python:3.10-slim

# Install required packages
RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Gradio UI port
EXPOSE 7860

# Command to run the app
CMD ["python", "app_agent.py"]
