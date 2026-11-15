# Production Dockerfile for Swiggy Support Desk AI
FROM python:3.12-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Install dependencies if present
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || true

# Copy application source
COPY . .

# Expose web server port
EXPOSE 8000

# Run lightweight HTTP application server
CMD ["python", "app.py"]
