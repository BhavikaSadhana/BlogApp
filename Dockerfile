FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the backend port
EXPOSE 5000

# Use a production server (e.g. gunicorn) or command that works for the repo
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
