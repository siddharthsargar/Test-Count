# FROM python:3.9

# WORKDIR /app

# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt

# COPY . .

# CMD ["gunicorn", "catalyst_count.wsgi:application", "--bind", "0.0.0.0:8000"]


FROM python:3.9

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsystemd-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run the application
CMD ["gunicorn", "catalyst_count.wsgi:application", "--bind", "0.0.0.0:8000"]
