# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# update pip
RUN pip install --upgrade pip

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

# Create and set a non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "eyouth.wsgi:application"] 
