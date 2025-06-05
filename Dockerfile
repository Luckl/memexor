FROM python:3.10-slim

WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy package files
COPY setup.py .
COPY src/ src/

# Install the package in development mode
RUN pip install -e .

# Create required directories
RUN mkdir -p /tmp/memexor/uploads /var/log/memexor

# Run the FastAPI application
CMD ["uvicorn", "src.presentation.api:app", "--host", "0.0.0.0", "--port", "8000"] 