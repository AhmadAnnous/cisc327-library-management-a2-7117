# Python base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /services

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port
EXPOSE 5000

# Environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Command that runs the flask server
CMD ["flask", "run", "--host=0.0.0.0"]
