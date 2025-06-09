# Base image with minimal footprint
FROM python:3.12-slim

# Metadata (optional)
LABEL maintainer="your-email@example.com"
LABEL description="EmotIndia - Real-time Emotion Detection using CNN"

# Prevent interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install system-level dependencies & Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libgl1-mesa-glx libglib2.0-0 && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y gcc && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the rest of the app
COPY . .

# Expose the port used by Flask
EXPOSE 5000

# Command to run the app
CMD ["python", "app.py"]
