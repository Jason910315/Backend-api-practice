# Build stage
FROM python:3.10-slim AS builder

WORKDIR /app

COPY requirements.txt .

# Install dependencies into a temporary directory
RUN pip install --user --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.10-slim

WORKDIR /app

# Copy only the installed dependencies from builder
COPY --from=builder /root/.local /root/.local

# Helper to ensure scripts in .local/bin are available
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY app ./app
COPY data ./data

# Expose the port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
