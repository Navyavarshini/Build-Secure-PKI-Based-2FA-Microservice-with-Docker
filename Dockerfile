# Use Ubuntu base image that we can pull reliably
FROM ubuntu:22.04

# Set working directory
WORKDIR /app

# Prevent interactive prompts in Docker build
ENV DEBIAN_FRONTEND=noninteractive

# Install Python, pip, cron, and timezone data
RUN apt-get update && \
    apt-get install -y python3 python3-pip cron tzdata && \
    ln -fs /usr/share/zoneinfo/UTC /etc/localtime && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install cron job from file
RUN chmod 0644 /app/cron/2fa-cron && \
    crontab /app/cron/2fa-cron && \
    mkdir -p /data /cron

# Expose port 8080
EXPOSE 8080

# Start cron and the FastAPI server
CMD cron && python3 -m uvicorn app:app --host 0.0.0.0 --port 8080

