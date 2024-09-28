# # Base image
# FROM python:3.12.5

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # Set work directory
# WORKDIR /

# # Install dependencies
# COPY requirements.txt /
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of the project
# COPY . /

# # Expose port 8000 (for Django)
# EXPOSE 8000

# # Run migrations and start the server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


# Base image
FROM python:3.12.5

# Set environment variables to avoid writing .pyc files and enable stdout
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /

# Install system dependencies (for PostgreSQL and other system packages)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install Python dependencies
COPY requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the Docker image
COPY . /

# Expose port 80 (for production)
EXPOSE 80

# Default command to run when starting the container (Django bound to port 80)
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
