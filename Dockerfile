# Use official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependency files (if you had requirements.txt, but here we install directly)
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn pydantic

# Expose port
EXPOSE 8000

# Run the FastAPI app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
