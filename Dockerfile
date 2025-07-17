# Use official Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose dashboard port (adjust if needed)
EXPOSE 8080

# Set environment variables (override in production)
ENV FLASK_DEBUG=False

# Default command
CMD ["python", "run.py"]