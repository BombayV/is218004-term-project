# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies including Node.js (needed for Tailwind)
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install Node dependencies
COPY package.json package-lock.json* /app/
RUN npm install

# Copy project files
COPY . /app/

# Expose port 8000
EXPOSE 8000

# The default command runs the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]