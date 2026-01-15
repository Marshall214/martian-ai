# Backend Dockerfile for Martian AI

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for PDF conversion and document processing
RUN apt-get update && apt-get install -y \
    libreoffice \
    ghostscript \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Create directories for static files
RUN mkdir -p static/audio

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/', timeout=5)"

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
