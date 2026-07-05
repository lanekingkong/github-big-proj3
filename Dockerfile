FROM python:3.12-slim

LABEL org.opencontainers.image.title="BioOmicsBridge"
LABEL org.opencontainers.image.description="AI-Powered Multi-Omics Data Integration and Drug Target Discovery Platform"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.licenses="MIT"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install BioOmicsBridge
RUN pip install --no-cache-dir -e .

# Create non-root user
RUN useradd -m -u 1000 bioomics && chown -R bioomics:bioomics /app
USER bioomics

# Expose dashboard port
EXPOSE 3000

# Default command
ENTRYPOINT ["bioomics-bridge"]
CMD ["--help"]