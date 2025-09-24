FROM python:3.10-slim

WORKDIR /app

# Install Flask and Prometheus exporter
RUN pip install --no-cache-dir flask prometheus-flask-exporter gunicorn

# Copy application code
COPY . .

# Expose the backend port
EXPOSE 5000

# Start with Gunicorn (adjust app:app if entrypoint is different)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
