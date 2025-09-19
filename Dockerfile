# Use Official Python slim image
FROM python:3.11-slim


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Expose the port
EXPOSE 8000


# Pass CMD arguments to the ENTRYPOINT script
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]