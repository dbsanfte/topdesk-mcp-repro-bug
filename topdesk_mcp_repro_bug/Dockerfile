FROM python:3.12-slim

WORKDIR /app

# Copy requirements file first for better cache utilization
COPY requirements.txt .
COPY zscaler.crt /usr/local/share/ca-certificates/zscaler.crt

RUN apt-get update && \
    apt-get install -y git ca-certificates && \
    update-ca-certificates && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get autoremove -y && \
    apt-get clean

# Copy application code
COPY . /app

# Run the app
CMD ["python", "main.py"]