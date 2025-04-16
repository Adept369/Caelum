# Dockerfile for Single-User Caelum ADHD Assistant


FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies for pdfkit and Google TTS
RUN apt-get update && apt-get install -y \
    curl \
    wkhtmltopdf \
    build-essential \
    libssl-dev \
    libffi-dev \
    libxrender1 \
    libxext6 \
    libx11-6 \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .
RUN pip install ngrok

# Expose port 5000
EXPOSE 5000
# Initialize the database and start the Flask app with Gunicorn
CMD ["sh", "-c", "python init_system.py && gunicorn run:app --bind 0.0.0.0:5000 --timeout 120"]


# Dockerfile snippet for production
# CMD ["gunicorn", "run:app", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120"]