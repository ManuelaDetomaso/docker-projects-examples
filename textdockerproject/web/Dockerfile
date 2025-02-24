FROM python:3.9-slim
WORKDIR /usr/src/app

# Install system dependencies required for spaCy & Thinc
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*  # Clean up to reduce image size

# Upgrade pip before installing dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir spacy \
    && python -m spacy download en_core_web_sm

# Copy the rest of the application
COPY . .

CMD ["python", "app.py"]