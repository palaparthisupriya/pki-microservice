# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Set Timezone and Environment
ENV TZ=UTC
ENV PATH="/root/.local/bin:${PATH}"
ENV PYTHONUNBUFFERED=1

# Install system dependencies: cron and tzdata
RUN apt-get update && apt-get install -y \
    cron \
    tzdata \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

# Copy installed python packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application folders
COPY app/ ./app/
COPY scripts/ ./scripts/
COPY cron/ ./cron/

# Setup Cron Job
# Copy the cron file to the system directory
COPY cron/2fa-cron /etc/cron.d/2fa-cron
# Give execution rights and apply the cron job
RUN chmod 0644 /etc/cron.d/2fa-cron && crontab /etc/cron.d/2fa-cron

# Create persistent storage directories
RUN mkdir -p /data /cron && chmod 755 /data /cron

# Expose API port
EXPOSE 8080

# Start both Cron daemon and the FastAPI server
# Using 'sh -c' to run two processes in one container
CMD ["sh", "-c", "cron && uvicorn app.main:app --host 0.0.0.0 --port 8080"]