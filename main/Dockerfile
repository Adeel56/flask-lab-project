# syntax=docker/dockerfile:1
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
# Install runtime deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/*
# Install Python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# Copy app
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
