# Backend Dockerfile for Martian AI
# Uses PyTorch base image with CUDA support for Llama 3.1 8B inference

FROM pytorch/pytorch:2.4.1-cuda12.4-cudnn9-runtime

# Set environment variables for Python optimization and output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Create a non-root user for security
RUN groupadd -r martian && useradd -r -g martian -m martian

# Set working directory
WORKDIR /app

# Install system dependencies for PDF conversion, document processing, and audio
RUN apt-get update && apt-get install -y \
    libreoffice \
    ghostscript \
    libmagic1 \
    curl \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
# Strip torch from requirements since it's already in the base image (CUDA-enabled).
# Re-installing via pip would pull the CPU-only wheel and break GPU inference.
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip "setuptools<70.0.0" wheel && \
    sed '/^torch==/d' requirements.txt > requirements_no_torch.txt && \
    pip install --no-cache-dir -r requirements_no_torch.txt && \
    rm requirements_no_torch.txt

# Copy the rest of the backend code
COPY backend/ .

# Create necessary directories and set permissions for the non-root user
RUN mkdir -p /app/data /app/static/audio /home/martian/.cache/huggingface/hub && \
    chown -R martian:martian /app/data /app/static /home/martian/.cache

# Switch to the non-root user
USER martian

EXPOSE 8000

# Increase start-period to 5 minutes to allow for model download on first launch.
# The Llama 3.1 8B model is ~4.5GB and may take several minutes to download.
HEALTHCHECK --interval=30s --timeout=10s --start-period=300s --retries=5 \
    CMD curl -f http://localhost:8000/ || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
